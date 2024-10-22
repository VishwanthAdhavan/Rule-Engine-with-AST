import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = None
db = None
rules_collection = None

def connect_to_mongodb():
    global client, db, rules_collection
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.admin.command('ismaster')
        db = client['rule_engine']
        rules_collection = db['rules']
        logger.info("Successfully connected to MongoDB")
        return True
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB. Error: {e}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred while connecting to MongoDB: {e}")
        return False

def get_rules_collection():
    global rules_collection
    if rules_collection is None:
        connect_to_mongodb()
    return rules_collection

# Sample rule document
sample_rule = {
    "name": "Sales and Marketing Rule",
    "description": "Eligibility rule for Sales and Marketing departments",
    "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
}

# Only insert the sample rule if the connection was successful
if rules_collection:
    # Check if the rule already exists to avoid duplicate insertions
    existing_rule = rules_collection.find_one({"name": sample_rule["name"]})
    if not existing_rule:
        rules_collection.insert_one(sample_rule)
        print("Sample rule inserted")
    else:
        print("Sample rule already exists")
