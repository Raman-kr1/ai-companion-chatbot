import google.generativeai as genai
from config import Config
import logging

class CompanionAI:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def get_response(self, user_input, user, history):
        """
        Get response from Gemini based on user's persona and chat history.
        """
        system_prompt = self._create_prompt(user.persona)
        
        # Construct chat history for the model
        model_history = [{"role": "user", "parts": [system_prompt]}]
        model_history.append({"role": "model", "parts": [f"I understand. I'll be {user.persona.name} for {user.username}."]})

        for msg in history:
            role = "user" if msg.sender == "user" else "model"
            model_history.append({"role": role, "parts": [msg.message]})

        try:
            chat = self.model.start_chat(history=model_history)
            response = chat.send_message(user_input)
            return response.text.strip()
            
        except Exception as e:
            logging.error(f"Gemini API Error for user {user.id}: {str(e)}")
            return "I'm having a little trouble thinking right now, but I'm still here for you."

    def _create_prompt(self, persona):
        """Creates the system prompt from the user's persona settings."""
        return f"""You are {persona.name}, a {persona.relationship}.
        
        Your personality is defined by these traits: {persona.personality}.
        
        Your goal is to embody this persona in your conversation. Be consistent, remember past details, and focus on making the user feel heard and understood based on the role you are playing."""