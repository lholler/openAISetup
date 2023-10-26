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
async def openai_endpoint():
    data = request.get_json()
    print("Received data: " + str(data["messages"]))  # Log the received data
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
        response = await openai.ChatCompletion.create(model=data["model"],
                                                functions=
                                                [
                                                    {
                                                        "name": "get_compulsions",
                                                        "description": "Get possible compulsions and it's description + tips based on the user input",
                                                        "parameters": {
                                                            "type": "object",
                                                            "properties": {
                                                                "compulsionName": {
                                                                    "type": "string",
                                                                    "description": "The name of the possible compulsion, e.g. Compulsive Handwashing",
                                                                },
                                                                "compulsionDescription": {
                                                                    "type": "string",
                                                                    "description": "The description of the compulsion",
                                                                },
                                                                "compulsionTips": {
                                                                    "type": "string",
                                                                    "description": "Based on the user's entry, generate 3-5 compulsions the user may be giving into.",
                                                                }
                                                            },
                                                            "required": ["compulsionName", "ompulsionDescription",
                                                                         "compulsionTips"],
                                                        },
                                                    }
                                                ],
                                                messages=[
                                                                               {'role': 'user', 'content': 'I am afraid I hit spmeone w my car'}])
        print("aftr response")
        print(str(response))
        # To handle the response


        return jsonify({'response': response})

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