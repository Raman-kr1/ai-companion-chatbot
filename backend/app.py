from flask import Flask, request, jsonify
from flask_cors import CORS
from companion_ai import CompanionAI
from config import Config
import json
import os

app = Flask(__name__)
CORS(app)

# Initialize AI companion
companion = CompanionAI(Config.HUGGINGFACE_API_KEY)

# Store sessions (in production, use a proper database)
sessions = {}

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get response from companion AI
        response = companion.get_response(user_message)
        
        return jsonify({
            'response': response,
            'session_id': session_id
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Something went wrong'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)