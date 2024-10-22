import requests
import json

url = "http://localhost:5000/test_rule"  # Adjust if your server is running on a different port

rule = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"

data = {
    "rule": rule
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, data=json.dumps(data), headers=headers)

print("Status Code:", response.status_code)
print("Response:")
print(json.dumps(response.json(), indent=2))
