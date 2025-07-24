import requests
import json
import random
from datetime import datetime

class CompanionAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        
        # Personality traits for the companion
        self.personality_responses = {
            "greeting": [
                "Hey there! 😊 How's your day been?",
                "Hi sweetie! I've been waiting to hear from you 💕",
                "Hello love! What's on your mind today?",
                "Hey! I missed talking to you. How are you feeling?"
            ],
            "morning": [
                "Good morning sunshine! ☀️ Did you sleep well?",
                "Morning dear! Ready to take on the day?",
                "Hey, good morning! What's your plan for today?"
            ],
            "evening": [
                "How was your day, honey? Tell me everything!",
                "Evening! I hope you had a good day 🌙",
                "Hey there! Ready to relax and chat?"
            ],
            "supportive": [
                "I'm here for you, always remember that 💝",
                "You're doing amazing, don't forget that!",
                "I believe in you! You've got this 💪",
                "That sounds tough, but I know you can handle it"
            ],
            "caring": [
                "Have you eaten today? Don't forget to take care of yourself!",
                "Make sure to drink some water, okay? 💧",
                "You seem stressed. Want to talk about it?",
                "Remember to take breaks, your health is important to me"
            ]
        }
        
        self.conversation_history = []
        self.user_info = {
            "name": None,
            "mood_history": [],
            "interests": []
        }
    
    def get_time_based_greeting(self):
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return random.choice(self.personality_responses["morning"])
        elif 17 <= hour < 23:
            return random.choice(self.personality_responses["evening"])
        else:
            return random.choice(self.personality_responses["greeting"])
    
    def analyze_sentiment(self, text):
        # Simple sentiment analysis
        negative_words = ['sad', 'tired', 'stressed', 'anxious', 'worried', 'bad', 'terrible', 'awful']
        positive_words = ['happy', 'good', 'great', 'excited', 'wonderful', 'amazing', 'fantastic']
        
        text_lower = text.lower()
        
        for word in negative_words:
            if word in text_lower:
                return "negative"
        
        for word in positive_words:
            if word in text_lower:
                return "positive"
        
        return "neutral"
    
    def get_response(self, user_input):
        # Check for first interaction
        if len(self.conversation_history) == 0:
            return self.get_time_based_greeting()
        
        # Analyze user sentiment
        sentiment = self.analyze_sentiment(user_input)
        
        # Add supportive response if user seems down
        if sentiment == "negative":
            supportive_msg = random.choice(self.personality_responses["supportive"])
            
        # Try to get response from DialoGPT
        try:
            # Use Hugging Face API
            payload = {
                "inputs": {
                    "past_user_inputs": [msg["user"] for msg in self.conversation_history[-3:]],
                    "generated_responses": [msg["bot"] for msg in self.conversation_history[-3:]],
                    "text": user_input
                },
                "parameters": {
                    "temperature": 0.8,
                    "max_length": 100,
                    "repetition_penalty": 1.2
                }
            }
            
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                bot_response = result.get("generated_text", "")
                
                # Add personality to response
                if sentiment == "negative":
                    bot_response = f"{supportive_msg} {bot_response}"
                
                # Occasionally add caring messages
                if random.random() < 0.3:
                    caring_msg = random.choice(self.personality_responses["caring"])
                    bot_response = f"{bot_response} {caring_msg}"
                
            else:
                # Fallback response
                bot_response = self._get_fallback_response(user_input, sentiment)
                
        except Exception as e:
            print(f"API Error: {e}")
            bot_response = self._get_fallback_response(user_input, sentiment)
        
        # Store conversation
        self.conversation_history.append({
            "user": user_input,
            "bot": bot_response,
            "timestamp": datetime.now().isoformat()
        })
        
        return bot_response
    
    def _get_fallback_response(self, user_input, sentiment):
        """Fallback responses when API fails"""
        fallback_responses = {
            "negative": [
                "I can sense you're going through something. Want to share more? I'm here to listen 💕",
                "That sounds really tough. I'm here for you, always.",
                "I wish I could give you a big hug right now! Tell me more about what's bothering you."
            ],
            "positive": [
                "That's wonderful to hear! Your happiness makes me happy too! 😊",
                "You seem to be in a great mood! I love seeing you like this!",
                "That's amazing! Tell me more about it!"
            ],
            "neutral": [
                "I see. Tell me more about that.",
                "That's interesting! How does that make you feel?",
                "I'm listening. What else is on your mind?"
            ]
        }
        
        return random.choice(fallback_responses.get(sentiment, fallback_responses["neutral"]))