import json  #module for working on json data
import requests #module for making http requests
import argparse #module for parsing cli

DATA_FILE = "data.json"  #file for storing data from api
API_URL = "https://www.travel-advisory.info/api"    #url for api


def get_country_name(country_code, data):
    #Function to get name of the country using country code
    if country_code.upper() in data:
        country_name = data[country_code.upper()]['name']
        return country_name
    else:
        return "Country not found"

def fetch_data():
    #Function to fetch data from the API and save it to a file
    try:
        response = requests.get(API_URL)   #making a GET request to API
        data = response.json()     #parse the json response
        
        if 'data' in data:
            with open(DATA_FILE, 'w') as file:
                json.dump(data['data'], file, indent=2)   #save the data to the file
            return data['data']
        else:
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}

def read_data_from_file():
    #Function to read data from the file
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
    parser = argparse.ArgumentParser(description="Country Lookup Service")  #creating an argument named parser
    parser.add_argument("--countryCodes", type=str, help="Country codes to lookup (comma-separated)", required=True)
    args = parser.parse_args()   #parse cli argumnets

    country_codes = [code.strip() for code in args.countryCodes.split(',')]   #extract country code from input
    
    # Try to read data from the file, fetch from API if file not found or data is invalid
    country_data = read_data_from_file()

    for country_code in country_codes:
        country_name = get_country_name(country_code, country_data)  #gets the country name based on the code inputed
        print(f"{country_code}: {country_name}")   #print the country name
