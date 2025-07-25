from flask import Flask, request, jsonify
from flask_cors import CORS
from companion_ai_gemini import CompanionAI  # Import the Gemini version
import json
import os

app = Flask(__name__)
CORS(app)

# Initialize AI companion with Gemini
try:
    companion = CompanionAI()
    print("✅ Gemini AI Companion initialized successfully!")
except Exception as e:
    print(f"❌ Error initializing Gemini: {e}")
    companion = None

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        print(f"Received message: {user_message}")  # Debug
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        if not companion:
            return jsonify({'error': 'AI companion not initialized'}), 500
        
        # Get response from Gemini companion AI
        response = companion.get_response(user_message)
        print(f"AI Response: {response}")  # Debug
        
        return jsonify({
            'response': response,
            'session_id': session_id
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Something went wrong'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'ai_ready': companion is not None
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)