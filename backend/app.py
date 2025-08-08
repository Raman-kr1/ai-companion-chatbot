# backend/app.py (Updated)

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

from config import Config
from extensions import db, bcrypt # Changed: import from extensions
from companion_ai_gemini import CompanionAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

from models import User, Persona, ChatMessage # This import now works

# Initialize AI companion
try:
    companion = CompanionAI()
    logging.info("✅ Gemini AI Companion initialized successfully!")
except Exception as e:
    logging.error(f"❌ Error initializing Gemini: {e}")
    companion = None

# --- Auth Routes ---
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 409

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    default_persona = Persona(user=new_user)
    db.session.add(default_persona)
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()

    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, email=user.email)
        
    return jsonify({"msg": "Bad email or password"}), 401

# --- Persona Routes ---
@app.route('/persona', methods=['GET', 'POST'])
@jwt_required()
def manage_persona():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if request.method == 'POST':
        data = request.get_json()
        persona = user.persona
        persona.name = data.get('name', persona.name)
        persona.relationship = data.get('relationship', persona.relationship)
        persona.personality = data.get('personality', persona.personality)
        db.session.commit()
        return jsonify({"msg": "Persona updated successfully"}), 200

    persona = user.persona
    return jsonify({
        "name": persona.name,
        "relationship": persona.relationship,
        "personality": persona.personality
    })

# --- Chat Routes ---
@app.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    if not companion:
        return jsonify({'error': 'AI companion not initialized'}), 503
        
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    data = request.get_json()
    user_message = data['message']

    db.session.add(ChatMessage(user_id=user.id, sender='user', message=user_message))
    db.session.commit()

    history = ChatMessage.query.filter_by(user_id=user.id).order_by(ChatMessage.timestamp.asc()).all()
    response_text = companion.get_response(user_message, user, history)

    db.session.add(ChatMessage(user_id=user.id, sender='ai', message=response_text))
    db.session.commit()

    return jsonify({'response': response_text})

@app.route('/chat/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    current_user_id = get_jwt_identity()
    messages = ChatMessage.query.filter_by(user_id=current_user_id).order_by(ChatMessage.timestamp.asc()).all()
    history = [{"sender": msg.sender, "message": msg.message} for msg in messages]
    return jsonify(history)

# --- Health Check ---
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'ai_ready': companion is not None})

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Ensure tables are created
    app.run(debug=True, port=5000)