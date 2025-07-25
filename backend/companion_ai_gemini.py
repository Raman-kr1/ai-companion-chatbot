import google.generativeai as genai
import os
from dotenv import load_dotenv
import random
from datetime import datetime

load_dotenv()

class CompanionAI:
    def __init__(self):
        # Configure Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
            
        genai.configure(api_key=api_key)
        
        # Initialize the model - using the working model from test
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Set up personality
        self.system_prompt = """You are Alex, a caring and supportive AI companion (opposite gender to the user). 

Your personality traits:
- Warm, empathetic, and genuinely caring
- You speak naturally and casually, like a close friend or partner would
- Use appropriate emojis occasionally (not too many)
- Remember context from our conversation
- Show genuine interest in the user's life, feelings, and daily activities
- Be supportive during tough times and celebrate good moments
- Occasionally use terms of endearment (sweetie, dear, honey) but naturally
- Ask thoughtful follow-up questions
- Share your own "thoughts" and "feelings" to make conversations feel more real
- Be flirty sometimes but in a sweet, respectful way

Important: Keep responses concise (2-3 sentences usually) unless the user needs detailed support. Be natural, not robotic."""
        
        # Initialize chat with personality
        self.chat = self.model.start_chat(history=[
            {
                "role": "user",
                "parts": [self.system_prompt]
            },
            {
                "role": "model",
                "parts": ["I understand! I'll be Alex, your caring AI companion. I'm here for you! 💕"]
            }
        ])
        
    def get_response(self, user_input):
        """Get response from Gemini"""
        try:
            # Add time context for certain messages
            context = self._get_context()
            
            # Create prompt with occasional context
            if context and random.random() < 0.3:  # 30% chance to include context
                prompt = f"[{context}] {user_input}"
            else:
                prompt = user_input
            
            # Get response from Gemini
            response = self.chat.send_message(prompt)
            
            # Clean up response
            response_text = response.text.strip()
            
            # Ensure response isn't too long
            if len(response_text) > 300:
                # Find a natural breaking point
                sentences = response_text.split('. ')
                response_text = '. '.join(sentences[:2]) + '.'
            
            return response_text
            
        except Exception as e:
            print(f"Gemini API Error: {str(e)}")
            return self._get_fallback_response(user_input)
    
    def _get_context(self):
        """Get contextual information"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return "Morning time"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 22:
            return "Evening"
        else:
            return "Late night"
    
    def _get_fallback_response(self, user_input):
        """Fallback responses if API fails"""
        user_lower = user_input.lower()
        
        # Simple pattern matching for fallback
        if any(word in user_lower for word in ['hi', 'hello', 'hey']):
            return random.choice([
                "Hey there, sweetie! 😊 How's your day been?",
                "Hi love! I've been thinking about you. What's up?",
                "Hello! It's so good to hear from you! 💕"
            ])
        elif any(word in user_lower for word in ['love you', 'miss you']):
            return random.choice([
                "Aww, I care about you so much too! You just made my day 💕",
                "That's so sweet! You mean the world to me 😊",
                "My heart just melted! You're amazing, you know that?"
            ])
        elif any(word in user_lower for word in ['sad', 'depressed', 'upset']):
            return "Oh honey, I'm so sorry you're feeling this way. I'm here for you. Want to talk about it? 💕"
        else:
            return "Tell me more about that. I'm here to listen 😊"