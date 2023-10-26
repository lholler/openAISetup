import openai
import requests
from flask import Flask, request, jsonify
import os
import traceback
import logging

from werkzeug.debug import console

# Configure logging

app = Flask(__name__)


@app.route('/openai', methods=['POST'])
def openai_endpoint():
    data = request.get_json()
    print("Received data: " + str(data))  # Log the received data

    openai_api_key = os.getenv('openai')

    print("Key: " + openai_api_key)

    try:

        completions_endpoint = 'https://api.openai.com/v1/chat/completions'
        print('Here')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_api_key}',
        }
        print("after here")

        response = requests.post(url=completions_endpoint, headers=headers, json=data)
        print("aftr response")
        print(f'Response: {response.text}')

        # To handle the response
        if response.status_code == 200:
            response_json = response.json()
        else:
            print(f'Failed to get response, status code: {response.status_code}')
        return jsonify({'response': response_json})
    except Exception as e:
        print('An error occurred: %s', e)  # Log exceptions with stack trace
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
