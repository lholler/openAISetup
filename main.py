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
    print("Received data: " + str(data["messages"]))  # Log the received data
    print(type(data["messages"]))
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
        response = openai.ChatCompletion.create(model=data["model"], messages=[{'role': 'system', 'content': "You are an OCD therapist helping a user with Response Prevention (resisting/stopping a compulsion). Based on the user's input, identify THREE compulsions at play. For each compulsion, provide 1) the name of the compulsion (MUST be a behavior, NOT a fear), 2) TWO-sentence description of how it affects the user in this current moment and fits into their specific OCD cycle, 3) a encouraging guide to fully stop the compulsion, with focus on helping them redirect attention to valued activities, and 4) TWO relevant IN-THE-MOMENT baby steps if full response prevention is too difficult.For the baby step, use the most relevant one from this list: delay or postpone the compulsion; set a time limit for the compulsion; gradual reduction of total number of rituals.Remember, the response prevention guide and baby step must be applicable to the user RIGHT NOW. They should be able to implement what you say RIGHT NOW.DON'T provide cognitive or non-actionable tips such as 'remind yourself it'll be okay', 'remember it's just OCD', or' challenge the belief that...Other guidelines:DON'T use any causal language (i.e 'the uncertainty brings up anxiety' instead of 'the uncertainty causes anxiety').DON'T use any language that gives certainty; instead use phrases like 'you SEEM', 'it's POSSIBLE that...', 'OCD LIKELY is...'.DON'T treat the OCD as something external or 'happening' to the user; instead, treat the user's 'self' as a context where ALL experiences occur (OCD, feelings, thoughts, anxiety, etc). Ex: 'feelings happen IN you' instead of 'feelings happen TO you'.DO maintain user's agency in their OCD experience. The OCD DOES NOT create the obsessions, anxiety, or compulsive urges; it only creates the overreaction/misappraisal of intrusive thoughts; everything else is normal experiences for user.DON'T use 'I' or 'the user', instead use 'you.DON'T mention exposures, breathing exercises, mindful techniques, or seeking a therapist/medical professionals."}, {'role': 'user', 'content': 'I am afraid I hit spmeone w my car'}])
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