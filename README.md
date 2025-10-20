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
