from flask import Flask, request, jsonify
from flask_cors import CORS
from companion_ai_gemini import CompanionAI
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize AI companion
try:
    companion = CompanionAI()
    logging.info("✅ Gemini AI Companion initialized successfully!")
except Exception as e:
    logging.error(f"❌ Error initializing Gemini: {e}")
    companion = None

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles chat requests from the user.
    
    Returns:
        A JSON response with the AI's message or an error.
    """
    if not companion:
        return jsonify({'error': 'AI companion not initialized'}), 503

    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid request. "message" is required.'}), 400

        user_message = data['message']
        session_id = data.get('session_id', 'default_session')
        
        logging.info(f"Received message from {session_id}: {user_message}")

        # Get response from Gemini companion AI
        response = companion.get_response(user_message, session_id)
        logging.info(f"AI Response for {session_id}: {response}")
        
        return jsonify({
            'response': response,
            'session_id': session_id
        })
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint for the application.
    
    Returns:
        A JSON response with the health status.
    """
    return jsonify({
        'status': 'healthy',
        'ai_ready': companion is not None
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
