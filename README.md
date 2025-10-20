# Backend Stage 1

A RESTful API built with Python and Flask that analyzes string data, stores the results, and provides flexible filtering capabilities, including natural language queries.

## Features

* **String Analysis**: Computes properties like length, palindrome status, word count, character frequency, and a unique SHA-256 hash.
* **Data Persistence**: Uses an in-memory store for fast, demonstration-ready data handling.
* **CRUD Operations**: Full support for creating, retrieving, and deleting string analyses.
* **Advanced Filtering**: Filter results based on specific properties (`is_palindrome`, `min_length`, etc.).
* **Natural Language Queries**: A smart endpoint that interprets plain English queries to apply filters (e.g., "all single word palindromic strings").

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

* Python 3.8+
* `pip` (Python package installer)
* Git

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/martinsikwueze/backend-stage1.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd backend-stage1
    ```

3. **Install the required dependencies:**
    It's recommended to use a virtual environment.

    ```bash
    # Create and activate a virtual environment (optional but recommended)
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    # Install dependencies from requirements.txt
    pip install -r requirements.txt
    ```

---

## Running the Application Locally

Once the dependencies are installed, you can start the Flask server with a single command:

```bash
python app.py
```

## API Endpoints and Testing

You can use command-line tools like `curl` to test the functionality

1. **Create/Analyze String**

    Analyzes a new string and stores its properties.

    * **URL**: /stings
    * **Method**: POST
    * **Request Body**:

    ```json
    {
        "value": "your string here"
    }
    ```

    * **Success Response (210 Created)**: Returns the full analysis object.
    * **Error Responses**: 400 Bad Request, 409 Conflict, 422 Unprocessable Entity.

    Example curl Request:

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"value": "A new test string"}' http://127.0.0.1:5000/strings
    ```

2. **Get Specific String**

    Retrieves the analysis for a specific string by its value.

    * **URL**: /strings/<string_value>
    * **Method**: GET
    * **Success Response (200 OK)**: Returns the stored analysis object.
    * **Error Responses**: 404 Not Found.

    Example curl Request:

    ```bash
    curl http://127.0.0.1:5000/strings/hello%20world
    ```

3. **Get All Strings with Filtering**

    Retrieves a list of all stored strings, with optional query parameters for filtering.

    * **URL**: /strings
    * **Method**: GET
    * **Query Parameters**:
        * is_palindrome (boolean): true or false
        * min_length (integer)
        * max_length (integer)
        * word_count (integer)
        * contains_character (string)
    * **Success Response (200 OK)**: Returns a list of matching strings and applied filters.
    * **Error Responses**: 400 Bad Request for invalid parameter values.

    Example curl Request:

    ```bash
    Find all palindromes with a length of at least 5
    curl "http://127.0.0.1:5000/strings?is_palindrome=true&min_length=5"
    ```

4. **Natural Language Filtering**

    Retrieves a list of strings by interpreting a natural language query.

    * **URL**: /strings/filter-by-natural-language
    * **Method**: GET
    * **Query Parameters**:
        * query (string): The natural language query.
    * **Success Response (200 OK)**: Returns the matching strings and the interpreted filters.
    * **Error Responses**: 400 Bad Request, 422 Unprocessable Entity.

    Example curl Request:

    ```bash
    Query: "all single word palindromic strings"
    curl "http://127.0.0.1:5000/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings"

    Query: "strings containing the letter z"
    curl "http://127.0.0.1:5000/strings/filter-by-natural-language?query=strings%20containing%20the%20letter%20z"
    ```

5. **Delete String**

    Deletes a stored string analysis by its value.

    * **URL**: /strings/<string_value>
    * **Method**: DELETE
    * **Success Response (204 No Content)**: Returns an empty response body.
    * **Error Responses**: 404 Not Found.

    Example curl Request:

    ```bash
    curl -X DELETE http://127.0.0.1:5001/strings/python
    ```
