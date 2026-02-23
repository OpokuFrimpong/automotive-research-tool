"""
Test the API directly to debug search issues
"""

import requests
import json

# Test the API
url = "http://localhost:8000/api/search"
data = {
    "question": "Future of autonomous driving",
    "use_ollama": True
}

print("Testing API with query:", data["question"])
print("=" * 60)

try:
    response = requests.post(url, json=data, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    result = response.json()
    print(json.dumps(result, indent=2))
    
except Exception as e:
    print(f"Error: {e}")
