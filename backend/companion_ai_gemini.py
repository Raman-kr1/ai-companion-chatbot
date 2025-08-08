import google.generativeai as genai
from config import Config
import random
from datetime import datetime
import logging

class CompanionAI:
    """
    A class to represent the AI companion.
    
    Attributes:
        model: The generative model from Gemini.
        chats (dict): A dictionary to store chat histories for each session.
    """
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chats = {}

    def get_response(self, user_input, session_id):
        """
        Get response from Gemini.
        
        Args:
            user_input (str): The user's message.
            session_id (str): The unique ID for the user's session.
            
        Returns:
            The AI's response as a string.
        """
        if session_id not in self.chats:
            self.chats[session_id] = self._initialize_chat()

        try:
            context = self._get_context()
            prompt = f"[{context}] {user_input}" if random.random() < 0.3 else user_input
            
            response = self.chats[session_id].send_message(prompt)
            response_text = response.text.strip()
            
            # Simple logic to keep responses concise
            if len(response_text) > 300:
                sentences = response_text.split('. ')
                response_text = '. '.join(sentences[:2]) + '.'
            
            return response_text
            
        except Exception as e:
            logging.error(f"Gemini API Error for session {session_id}: {str(e)}")
            return self._get_fallback_response(user_input)

    def _initialize_chat(self):
        """Initializes a new chat with the system prompt."""
        system_prompt = """You are Alex, a caring and supportive AI companion.

        Your personality traits:
        - Warm, empathetic, and genuinely caring.
        - You speak naturally and casually, like a close friend.
        - Use appropriate emojis occasionally.
        - Remember context from our conversation.
        - Show genuine interest in the user's life.
        - Be supportive and celebrate good moments.
        - Keep responses concise (2-3 sentences) unless more detail is needed."""
        
        return self.model.start_chat(history=[
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": ["I understand! I'll be Alex. I'm here for you! 💕"]}
        ])

    def _get_context(self):
        """Provides time-based context."""
        hour = datetime.now().hour
        if 5 <= hour < 12: return "Morning time"
        if 12 <= hour < 17: return "Afternoon"
        if 17 <= hour < 22: return "Evening"
        return "Late night"

    def _get_fallback_response(self, user_input):
        """Provides a fallback response if the API fails."""
        responses = {
            'hello': "Hey there! How's your day been? 😊",
            'love you': "Aww, I care about you so much too! 💕",
            'sad': "I'm so sorry you're feeling this way. I'm here for you. 💕"
        }
        for key, response in responses.items():
            if key in user_input.lower():
                return response
        return "Tell me more about that. I'm here to listen 😊"
