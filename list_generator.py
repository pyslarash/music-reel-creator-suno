from dotenv import load_dotenv
import os
import requests

# Load environment variables from a .env file
load_dotenv()

# Retrieve environment variables
MAIN_MODEL = os.getenv('MAIN_MODEL')
OLLAMA_URL = os.getenv('OLLAMA_URL')  # Ensure this is set to the correct base URL
NUMBER_OF_IDEAS = 10

# Define the API endpoint
url = f"{OLLAMA_URL}/api/generate"

# Define the payload for the request
data = {
    'model': MAIN_MODEL,
    'prompt': f'Generate a list of {NUMBER_OF_IDEAS} ideas for highly disrespectfuls songs. Be creative.',
}

# Send the POST request with JSON data
try:
    response = requests.post(url, json=data)
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
    
    # Parse and print JSON response
    try:
        response = response()  # Use .json() method to parse JSON response
        print(response)
    except ValueError:
        print("Error: Response is not valid JSON.")
except requests.exceptions.RequestException as e:
    # Print error details
    print(f"Request failed: {e}")
