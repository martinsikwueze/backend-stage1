import hashlib
import datetime
import re
from collections import Counter
from flask import Flask, request, jsonify

app = Flask(__name__)

string_storage = {}

def analyze_string(value: str):
    """Computes all required properties for a given string."""
    sha256 = hashlib.sha256(value.encode()).hexdigest()
    
    # Normalize for palindrome check (case-insensitive, ignores non-alphanumeric chars)
    normalized = ''.join(filter(str.isalnum, value)).lower()
    
    properties = {
        "length": len(value),
        "is_palindrome": normalized == normalized[::-1],
        "unique_characters": len(set(value)),
        "word_count": len(value.split()),
        "sha256_hash": sha256,
        "character_frequency_map": dict(Counter(value))
    }
    
    return {
        "id": sha256,
        "value": value,
        "properties": properties,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

def parse_natural_language_query(query: str):
    """A simple heuristic-based parser for natural language queries."""
    filters = {}
    lower_query = query.lower()

    if "palindromic" in lower_query or "palindrome" in lower_query:
        filters["is_palindrome"] = True

    if "single word" in lower_query or "one word" in lower_query:
        filters["word_count"] = 1
    
    longer_match = re.search(r'longer than (\d+)', lower_query)
    if longer_match:
        filters["min_length"] = int(longer_match.group(1)) + 1

    shorter_match = re.search(r'shorter than (\d+)', lower_query)
    if shorter_match:
        filters["max_length"] = int(shorter_match.group(1)) - 1
        
    # Check for character containment
    contains_match = re.search(r'contain(?:s|ing) the letter ([a-z])', lower_query)
    if contains_match:
        filters["contains_character"] = contains_match.group(1)
    
    # Heuristic for "first vowel"
    if "first vowel" in lower_query:
        filters["contains_character"] = "a"
        
    if not filters:
        raise ValueError("Unable to parse natural language query into known filters.")
        
    return filters

@app.route('/strings', methods=['POST'])
def create_string():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request body, must be JSON"}), 400
    
    value = data.get('value')
    if value is None:
        return jsonify({"error": "Missing 'value' field in request body"}), 400
    if not isinstance(value, str):
        return jsonify({"error": "Invalid data type for 'value', must be a string"}), 422
        
    if value in string_storage:
        return jsonify({"error": "String already exists in the system"}), 409
        
    analysis = analyze_string(value)
    string_storage[value] = analysis
    
    return jsonify(analysis), 201

@app.route('/strings/<path:string_value>', methods=['GET'])
def get_string(string_value):
    if string_value in string_storage:
        return jsonify(string_storage[string_value]), 200
    else:
        return jsonify({"error": "String does not exist in the system"}), 404

@app.route('/strings', methods=['GET'])
def get_all_strings():
    filters_applied = {}
    results = list(string_storage.values())

    try:
        # Filter by is_palindrome
        is_palindrome_str = request.args.get('is_palindrome')
        if is_palindrome_str:
            is_palindrome = is_palindrome_str.lower() == 'true'
            results = [s for s in results if s['properties']['is_palindrome'] == is_palindrome]
            filters_applied['is_palindrome'] = is_palindrome

        # Filter by min_length
        min_length = request.args.get('min_length', type=int)
        if min_length is not None:
            results = [s for s in results if s['properties']['length'] >= min_length]
            filters_applied['min_length'] = min_length
            
        # Filter by max_length
        max_length = request.args.get('max_length', type=int)
        if max_length is not None:
            results = [s for s in results if s['properties']['length'] <= max_length]
            filters_applied['max_length'] = max_length
            
        # Filter by word_count
        word_count = request.args.get('word_count', type=int)
        if word_count is not None:
            results = [s for s in results if s['properties']['word_count'] == word_count]
            filters_applied['word_count'] = word_count
            
        # Filter by contains_character
        contains_char = request.args.get('contains_character')
        if contains_char:
            results = [s for s in results if contains_char in s['value']]
            filters_applied['contains_character'] = contains_char
            
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid query parameter value or type"}), 400

    return jsonify({
        "data": results,
        "count": len(results),
        "filters_applied": filters_applied
    }), 200

@app.route('/strings/filter-by-natural-language', methods=['GET'])
def filter_by_natural_language():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400
        
    try:
        parsed_filters = parse_natural_language_query(query)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    results = list(string_storage.values())
    
    if parsed_filters.get('is_palindrome'):
        results = [s for s in results if s['properties']['is_palindrome']]
    if 'min_length' in parsed_filters:
        results = [s for s in results if s['properties']['length'] >= parsed_filters['min_length']]
    if 'max_length' in parsed_filters:
         results = [s for s in results if s['properties']['length'] <= parsed_filters['max_length']]
    if 'word_count' in parsed_filters:
        results = [s for s in results if s['properties']['word_count'] == parsed_filters['word_count']]
    if 'contains_character' in parsed_filters:
        char = parsed_filters['contains_character']
        results = [s for s in results if char in s['value']]

    return jsonify({
        "data": results,
        "count": len(results),
        "interpreted_query": {
            "original": query,
            "parsed_filters": parsed_filters
        }
    }), 200

@app.route('/strings/<path:string_value>', methods=['DELETE'])
def delete_string(string_value):
    if string_value in string_storage:
        del string_storage[string_value]
        return '', 204
    else:
        return jsonify({"error": "String does not exist in the system"}), 404


if __name__ == '__main__':
    app.run()