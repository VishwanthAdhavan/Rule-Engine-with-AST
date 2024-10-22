# Rule Engine API

## Description

This Rule Engine API is a Flask-based web service that allows users to create, store, and evaluate complex logical rules. It provides a flexible and powerful way to define business rules that can be applied to various data sets.

## Features

- Create complex rules using logical operators (AND, OR) and comparisons
- Store rules in MongoDB for persistence
- Evaluate data against stored rules
- RESTful API for easy integration
- Parentheses support for complex rule grouping
- Detailed error reporting and logging

## Technologies Used

- Python 3.8+
- Flask 2.3.2
- MongoDB
- PyMongo 4.3.3
- Requests 2.31.0 (for testing)

## Project Structure

rule-engine/
│

├── app.py

├── rule_engine/
│ ├── init.py
│ ├── api.py
│ └── database.py
├── templates/
│ └── index.html
├── requirements.txt
├── .env
├── .gitignore
└── README.md


## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/rule-engine.git
   cd rule-engine
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your MongoDB database and update the `.env` file with your database URI:
   ```
   MONGODB_URI=your_mongodb_uri_here
   ```

5. Run the Flask application:
   ```
   python app.py
   ```

The server should now be running on `http://localhost:5000`.

## API Endpoints

### 1. Create a Rule

- **URL:** `/create_rule`
- **Method:** POST
- **Body:**
  ```json
  {
    "rule": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
  }
  ```
- **Success Response:**
  - **Code:** 201
  - **Content:** `{ "message": "Rule created successfully", "rule_id": "12345", "rule_string": "..." }`

### 2. Evaluate a Rule

- **URL:** `/evaluate_rule`
- **Method:** POST
- **Body:**
  ```json
  {
    "rule_id": "12345",
    "data": {
      "age": 35,
      "department": "Sales",
      "salary": 60000,
      "experience": 7
    }
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:** `{ "result": true }`

## Testing

You can use the provided `test_rule.py` script to test the API:


## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/rule-engine.git
   cd rule-engine
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your MongoDB database and update the `.env` file with your database URI:
   ```
   MONGODB_URI=your_mongodb_uri_here
   ```

5. Run the Flask application:
   ```
   python app.py
   ```

The server should now be running on `http://localhost:5000`.

## API Endpoints

### 1. Create a Rule

- **URL:** `/create_rule`
- **Method:** POST
- **Body:**
  ```json
  {
    "rule": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
  }
  ```
- **Success Response:**
  - **Code:** 201
  - **Content:** `{ "message": "Rule created successfully", "rule_id": "12345", "rule_string": "..." }`

### 2. Evaluate a Rule

- **URL:** `/evaluate_rule`
- **Method:** POST
- **Body:**
  ```json
  {
    "rule_id": "12345",
    "data": {
      "age": 35,
      "department": "Sales",
      "salary": 60000,
      "experience": 7
    }
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:** `{ "result": true }`

## Testing

You can use the provided `test_rule.py` script to test the API:

```
## Advantages of this Implementation

1. **Flexibility:** The rule engine can handle complex logical expressions with nested conditions.
2. **Scalability:** Using MongoDB allows for efficient storage and retrieval of rules, making it suitable for large-scale applications.
3. **Separation of Concerns:** The project structure separates the API handling (app.py) from the rule engine logic (rule_engine/api.py) and database operations (rule_engine/database.py).
4. **Error Handling:** Comprehensive error checking and reporting make debugging and usage easier.
5. **RESTful Design:** The API follows RESTful principles, making it easy to integrate with other services.
6. **Extensibility:** The modular design allows for easy addition of new features or rule types.

## Future Improvements

- Add user authentication and authorization
- Implement rule versioning
- Create a web interface for rule management
- Add support for more complex rule types (e.g., regex matching, date comparisons)
- Implement caching for frequently used rules

