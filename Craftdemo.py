from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

API_URL = "https://www.travel-advisory.info/api"
DATA_FILE = "data.json"

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/diag_check', methods=['GET'])
def diag_check():
    try:
        response = requests.get(API_URL)
        api_status = response.json()['api_status']
        return jsonify({"api_status": api_status})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error checking API status: {e}"}), 500

@app.route('/convert/<country_name>', methods=['GET'])
def convert(country_name):
    country_data = read_data_from_file()
    country_code = get_country_code(country_name, country_data)
    return jsonify({"country_code": country_code})

def get_country_code(country_name, data):
    for code, info in data.items():
        if info['name'].lower() == country_name.lower():
            return code
    return "Country not found"

def fetch_data():
    try:
        response = requests.get(API_URL)
        data = response.json()

        if 'data' in data:
            with open(DATA_FILE, 'w') as file:
                json.dump(data['data'], file, indent=2)
            return data['data']
        else:
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}

def read_data_from_file():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File {DATA_FILE} not found. Fetching data from the API.")
        return fetch_data()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file: {e}")
        return {}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

