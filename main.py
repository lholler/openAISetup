from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai_api_key = os.getenv('openai')  # Get your OpenAI API key from an environment variable

@app.route('/openai', methods=['POST'])
def openai_endpoint():
    print(openai_api_key)
    data = request.get_json()
    # Extract necessary data from the request
    prompt = data.get('prompt')
    model = data.get('model', 'gpt-3.5-turbo')
    max_tokens = data.get('maxTokens', 1000)
    temperature = data.get('temperature', 1)

    openai.api_key = openai_api_key
    try:
        response = openai.ChatCompletion.create(engine=model, prompt=prompt, max_tokens=max_tokens, temperature=temperature)
        return jsonify(response['choices'][0]['text'].strip())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
