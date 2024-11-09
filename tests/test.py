import requests
import json
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from core.utils import get_config

def send_payload_example():
    # Load config and override with environment variables if set
    config = get_config(os.path.join(project_root, 'config.yml'))
    protocol = os.getenv('API_PROTOCOL', config['API']['protocol'])
    host = os.getenv('API_HOST', config['API']['host'])
    port = int(os.getenv('API_PORT', config['API']['port']))
    endpoint = os.getenv('API_ENDPOINT', config['API']['endpoint'])

    # Load test payload
    path = os.path.join(project_root, 'example_payloads', 'payload3.json')
    with open(path, 'r') as file:
        payload = json.load(file)

    # Send request
    url = f"{protocol}://{host}:{port}/{endpoint}"
    try:
        req = requests.post(url, json=payload)
        req.raise_for_status()
        print(f"Success! Response: {req.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response text: {e.response.text}")

if __name__ == '__main__':
    send_payload_example()