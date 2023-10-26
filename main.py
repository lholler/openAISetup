import requests
from flask import Flask, request, jsonify
import openai
import os
import logging

from werkzeug.debug import console

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/openai', methods=['POST'])
def openai_endpoint():
    data = request.get_json()
    console.log('Received data: %s', data)  # Log the received data

    # Extract necessary data from the request
    prompt = data.get('prompt')
    model = data.get('model', 'gpt-3.5-turbo')
    max_tokens = data.get('maxTokens', 1000)
    temperature = data.get('temperature', 1)

    console.log(('Using model: %s, max_tokens: %d, temperature: %.1f', model, max_tokens, temperature))  # Log the extracted values

    openai_api_key = os.getenv('openai')

    console.log("Key: "+openai_api_key)

    try:

        completions_endpoint = 'https://api.openai.com/v1/chat/completions'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_api_key}',
        }


        response = requests.post(completions_endpoint, headers=headers, json=data)

        # To handle the response
        if response.status_code == 200:
            response_json = response.json()
        else:
            console.log((f'Failed to get response, status code: {response.status_code}'))
        return jsonify({'response': response_json})
    except Exception as e:
        logging.exception('An error occurred: %s', e)  # Log exceptions with stack trace
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
