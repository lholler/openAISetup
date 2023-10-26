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
        openai.api_key=openai_api_key
        #response = requests.post(url=completions_endpoint, headers=headers, json=data)
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ])
        print("aftr response")
        print(str(response))
        # To handle the response
        if response.status_code == 200:
            response_json = response.json()
        else:
            print(f'Failed to get response, status code: {response.status_code}')
        return jsonify({'response': response_json})

    except requests.exceptions.RequestException as e:  # This will catch any Requests-related exceptions
        print(f'Request error: {e}')
        traceback.print_exc()  # This will print the traceback

    except requests.exceptions.RequestException as e:  # This will catch any Requests-related exceptions
        logging.error(f'Request error: {e}')
        traceback.print_exc()  # This will print the traceback

    except Exception as e:
        logging.error(f'An error occurred: {e}')
        traceback.print_exc()  # This will print the traceback

    except Exception as e:
        print(f'An error occurred: {e}')
        traceback.print_exc()  #


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Enable debug mode