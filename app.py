from flask import Flask, request, jsonify, render_template
from rule_engine.api import create_rule, evaluate_rule, tokenize, NodeType, Operator, rule_to_string, check_parentheses
from rule_engine.database import connect_to_mongodb, get_rules_collection
import logging
import sys
import os
from bson import ObjectId
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Disable debug logging for werkzeug
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# Disable debug logging for pymongo
logging.getLogger('pymongo').setLevel(logging.ERROR)

app = Flask(__name__)

# Connect to MongoDB
db_connected = connect_to_mongodb()
logger.info(f"MongoDB connection status: {'Connected' if db_connected else 'Not Connected'}")

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

@app.after_request
def log_response_info(response):
    app.logger.debug('Response: %s', response.get_data())
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Test route is working", "db_connected": db_connected})

@app.route('/create_rule', methods=['POST'])
def api_create_rule():
    if not db_connected:
        logger.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500
    
    rule_string = request.json.get('rule')
    logger.debug(f"Received rule: {rule_string}")
    try:
        tokens = tokenize(rule_string)
        logger.debug(f"Tokenized rule: {tokens}")
        
        # Add this debug information
        for i, token in enumerate(tokens):
            logger.debug(f"Token {i}: '{token}'")
        
        check_parentheses(tokens)
        logger.debug("Parentheses check passed")
        
        rule = create_rule(rule_string)
        logger.debug(f"Parsed rule: {rule_to_string(rule)}")
        rules_collection = get_rules_collection()
        if rules_collection is None:
            raise Exception("Failed to get rules collection")
        rule_id = rules_collection.insert_one({"rule_string": rule_string}).inserted_id
        logger.info(f"Rule created successfully. ID: {rule_id}")
        return jsonify({"message": "Rule created successfully", "rule_id": str(rule_id), "rule_string": rule_string}), 201
    except ValueError as e:
        logger.error(f"Error parsing rule: {str(e)}", exc_info=True)
        return jsonify({"error": f"Error parsing rule: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"Unexpected error creating rule: {str(e)}", exc_info=True)
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/evaluate_rule', methods=['POST'])
def api_evaluate_rule():
    if not db_connected:
        logger.error("Database connection failed")
        return jsonify({"error": "Database connection failed"}), 500
    
    rule_id = request.json.get('rule_id')
    data = request.json.get('data')
    
    try:
        rules_collection = get_rules_collection()
        if rules_collection is None:
            raise Exception("Failed to get rules collection")
        rule_doc = rules_collection.find_one({"_id": ObjectId(rule_id)})
        if not rule_doc:
            return jsonify({"error": "Rule not found"}), 404
        
        rule = create_rule(rule_doc['rule_string'])
        result = evaluate_rule(rule, data)
        return jsonify({"result": result}), 200
    except Exception as e:
        logger.error(f"Error evaluating rule: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/test_rules', methods=['GET'])
def test_rules():
    test_rules = [
        "(age > 30 AND department = 'Sales')",
        "(age < 25 AND department = 'Marketing')",
        "(salary > 50000 OR experience > 5)",
        "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing'))",
        "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    ]
    
    results = []
    for rule in test_rules:
        try:
            create_rule(rule)
            results.append({"rule": rule, "result": "Success"})
        except Exception as e:
            results.append({"rule": rule, "result": f"Error: {str(e)}"})
    
    return jsonify(results)

@app.route('/test_rule', methods=['POST'])
def test_rule():
    try:
        data = request.get_json(force=True)
        rule_string = data.get('rule')
        if not rule_string:
            return jsonify({"error": "No rule provided in the request"}), 400
        
        logger.debug(f"Testing rule: {rule_string}")
        rule = create_rule(rule_string)
        logger.debug(f"Parsed rule: {rule_to_string(rule)}")
        return jsonify({"message": "Rule parsed successfully", "parsed_rule": rule_to_string(rule)}), 200
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in request: {str(e)}")
        return jsonify({"error": f"Invalid JSON in request: {str(e)}"}), 400
    except ValueError as e:
        logger.error(f"Error parsing rule: {str(e)}", exc_info=True)
        return jsonify({"error": f"Error parsing rule: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    port = 5000
    logger.info(f"Starting Flask application on http://localhost:{port}")
    print(f"\n* Running on http://localhost:{port}")
    print("* Press CTRL+C to quit")
    app.run(debug=True, host='localhost', port=port)

BASE_URL = 'http://192.168.0.124:5000'

def create_rule(rule_string):
    url = f'{BASE_URL}/create_rule'
    data = {'rule': rule_string}
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if hasattr(e, 'response'):
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.content}")
        return None

# Test create_rule
rule = "age > 30 AND department = 'Sales'"
print("Attempting to create rule...")
create_response = create_rule(rule)
print("Create Rule Response:", create_response)

if create_response and 'rule_id' in create_response:
    print("Rule created successfully")
else:
    print("Failed to create rule")

def test_post():
    url = f'{BASE_URL}/test'
    data = {'test': 'data'}
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if hasattr(e, 'response'):
            print(f"Response status code: {e.response.status_code}")
            print(f"Response content: {e.response.content}")
        return None

print("Testing POST request...")
test_response = test_post()
print("Test Response:", test_response)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
