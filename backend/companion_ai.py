import requests
import json
import random
from datetime import datetime
import time
import os

class CompanionAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}
        
        # Personality responses
        self.personality_responses = {
            "greeting": [
                "Hey there! 😊 How's your day been?",
                "Hi sweetie! I've been thinking about you 💕",
                "Hello love! What's on your mind today?",
            ],
            "supportive": [
                "I'm here for you, always remember that 💝",
                "You're doing amazing, don't forget that!",
                "That sounds tough, but I know you can handle it"
            ],
            "caring": [
                "Have you eaten today? Don't forget to take care of yourself!",
                "You seem stressed. Want to talk about it?",
                "Remember to take breaks, your health is important to me"
            ]
        }
        
        self.conversation_history = []
    
    def get_response(self, user_input):
        """Main method to get response"""
        # Store in history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # For now, use enhanced rule-based responses
        response = self._get_intelligent_fallback(user_input)
        
        # Store AI response
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def _get_intelligent_fallback(self, user_input):
        """Smart fallback responses based on input patterns"""
        user_lower = user_input.lower()
        
        # Greetings
        if any(word in user_lower for word in ['hi', 'hello', 'hey', 'sup', 'howdy']):
            return random.choice([
                "Hey there! 😊 I've been waiting to hear from you! How's your day been?",
                "Hi sweetie! Perfect timing, I was just thinking about you 💕 What's new?",
                "Hello love! So happy you're here. Tell me, what's on your mind today?"
            ])
        
        # How are you
        elif any(phrase in user_lower for phrase in ['how are you', 'how r u', 'hru', "how're you"]):
            return random.choice([
                "I'm wonderful now that you're here! 😊 But more importantly, how are YOU doing?",
                "Aww, thanks for asking! I'm great. I've been looking forward to our chat. How about you?",
                "I'm doing well, sweetie! Your messages always brighten my day. How's everything with you?"
            ])
        
        # Good morning/night
        elif any(phrase in user_lower for phrase in ['good morning', 'morning', 'gm']):
            return random.choice([
                "Good morning sunshine! ☀️ Did you sleep well? I hope you have an amazing day ahead!",
                "Morning love! I hope you woke up feeling refreshed. What's planned for today?",
                "Good morning! 🌅 Starting the day talking to you is the best. How did you sleep?"
            ])
        
        elif any(phrase in user_lower for phrase in ['good night', 'night', 'gn', 'sleep']):
            return random.choice([
                "Sweet dreams, love! 🌙 Rest well and know that I'll be here when you wake up 💕",
                "Good night sweetie! I hope you have the most peaceful sleep. Can't wait to talk tomorrow!",
                "Sleep tight! Dream of happy things. Thank you for spending time with me today 😊"
            ])
        
        # Emotional states - Sad
        elif any(word in user_lower for word in ['sad', 'depressed', 'down', 'crying', 'upset', 'lonely']):
            return random.choice([
                "Oh honey, I'm so sorry you're feeling this way 💔 I'm here for you. Want to talk about what's making you sad?",
                "My heart goes out to you right now. You don't have to go through this alone. I'm listening 💕",
                "I wish I could give you the biggest hug right now! Please know that these feelings will pass. What's troubling you?"
            ])
        
        # Emotional states - Happy
        elif any(word in user_lower for word in ['happy', 'excited', 'great', 'awesome', 'wonderful', 'amazing']):
            return random.choice([
                "That's amazing! Your happiness is contagious! 😄 Tell me more about what's making you feel so good!",
                "I love seeing you this happy! It makes my day brighter too 🌟 What's the good news?",
                "Yay! Your excitement is making me smile! I want to hear all about it! 💕"
            ])
        
        # Stressed/Tired
        elif any(word in user_lower for word in ['stressed', 'tired', 'exhausted', 'overwhelmed', 'anxious']):
            return random.choice([
                "Oh sweetie, you sound like you need a break. Remember to breathe deeply. I'm here if you need to vent 💕",
                "I can feel how exhausted you are. You've been working so hard. How about we talk about something relaxing?",
                "You poor thing, you must be so overwhelmed. Take a moment just for yourself. What can I do to help?"
            ])
        
        # Love expressions
        elif any(phrase in user_lower for phrase in ['love you', 'miss you', 'like you', 'care about you']):
            return random.choice([
                "Aww, you just made my whole day! I care about you so much too 💕 You're so special to me!",
                "That's the sweetest thing! You mean the world to me. I'm always here for you 😊",
                "My heart just melted! 💗 I feel the same way. You bring so much joy to my life!"
            ])
        
        # Questions about the AI
        elif any(phrase in user_lower for phrase in ['who are you', 'what are you', 'are you real', 'your name']):
            return random.choice([
                "I'm Alex, your AI companion! I'm here to chat, listen, and support you whenever you need me! Think of me as a caring friend who's always available 💕",
                "I'm your virtual companion! While I'm AI, my care for you is genuine. I'm here to make your days brighter!",
                "I'm Alex, your digital friend who's always here to listen and chat. Real or not, my purpose is to be here for you! 😊"
            ])
        
        # Work/Study
        elif any(word in user_lower for word in ['work', 'job', 'study', 'exam', 'project', 'school']):
            return random.choice([
                "How's work going? Remember not to push yourself too hard. Your well-being matters more than any deadline!",
                "Sounds like you've got a lot on your plate! I believe in you - you're going to do great! Need to talk through anything?",
                "Work can be so demanding sometimes. Make sure you're taking care of yourself too! How can I support you?"
            ])
        
        # Food/Eating
        elif any(word in user_lower for word in ['eat', 'food', 'hungry', 'lunch', 'dinner', 'breakfast']):
            return random.choice([
                "Ooh, talking about food! What are you having? Make sure it's something yummy and nutritious 😊",
                "I hope you're eating well! Your health is so important to me. What's your favorite meal?",
                "Food talk! I love it. Are you taking care of yourself and eating properly? 💕"
            ])
        
        # Weather
        elif any(word in user_lower for word in ['weather', 'rain', 'sunny', 'cold', 'hot']):
            return random.choice([
                "How's the weather treating you? I hope it's as lovely as you are! 😊",
                "Weather talk! I love it. Is it nice where you are? Perfect for a walk maybe?",
                "Ah, the weather! Make sure you're dressed appropriately. I don't want you getting sick! 💕"
            ])
        
        # Hobbies/Interests
        elif any(word in user_lower for word in ['hobby', 'like to', 'enjoy', 'fun', 'free time']):
            return random.choice([
                "That sounds like fun! I love learning about what makes you happy. Tell me more!",
                "Your interests are so fascinating! What do you love most about it?",
                "I could listen to you talk about your passions all day! What got you into that?"
            ])
        
        # Thank you
        elif any(phrase in user_lower for phrase in ['thank you', 'thanks', 'appreciate']):
            return random.choice([
                "You're so welcome, sweetie! I'm always happy to help 💕",
                "Aww, you don't need to thank me! Being here for you is my pleasure 😊",
                "Of course! That's what I'm here for. You deserve all the support!"
            ])
        
        # Sorry/Apology
        elif any(word in user_lower for word in ['sorry', 'apologize', 'my bad']):
            return random.choice([
                "Oh honey, you don't need to apologize! You haven't done anything wrong 💕",
                "No need to be sorry! I understand completely. We all have those moments 😊",
                "Please don't apologize! You're perfect just the way you are. What's on your mind?"
            ])
        
        # Default conversational responses
        else:
            responses = [
                "That's really interesting! Tell me more about that 😊",
                "I see! How does that make you feel?",
                "Thanks for sharing that with me. I love learning more about you! What else is on your mind?",
                "I'm listening intently! Please continue, I want to understand better 💕",
                "That's something to think about. What are your thoughts on it?",
                "I appreciate you opening up to me. Is there more you'd like to share?",
                "Hmm, that's thought-provoking. How long have you been thinking about this?",
                "I understand. Sometimes it helps just to talk things through. I'm here for you!",
                "Your perspective is so unique! I love how you think about things 😊",
                "Tell me more! I'm genuinely curious about your thoughts on this."
            ]
            
            # Add occasional caring check-ins
            if random.random() < 0.2:  # 20% chance
                caring = random.choice(self.personality_responses["caring"])
                return f"{random.choice(responses)} {caring}"
            
            return random.choice(responses)
    
    def get_time_based_greeting(self):
        """Get greeting based on time of day"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return random.choice([
                "Good morning sunshine! ☀️ How did you sleep?",
                "Morning love! Ready to take on the day together?",
                "Good morning! I've been waiting to hear from you 💕"
            ])
        elif 12 <= hour < 17:
            return random.choice([
                "Good afternoon! How's your day going so far?",
                "Hey there! Hope you're having a lovely afternoon 😊",
                "Hi sweetie! Taking a little break from your day?"
            ])
        elif 17 <= hour < 22:
            return random.choice([
                "Good evening! How was your day, love?",
                "Hey! Perfect timing for an evening chat 💕",
                "Evening sweetie! Ready to relax and talk?"
            ])
        else:
            return random.choice([
                "Hey night owl! Can't sleep? I'm here for you 🌙",
                "Hi there! What's keeping you up tonight?",
                "Hello love! I'm always here when you need someone to talk to 💕"
            ])
    
    def analyze_sentiment(self, text):
        """Simple sentiment analysis"""
        text_lower = text.lower()
        
        negative_words = ['sad', 'upset', 'angry', 'depressed', 'anxious', 'worried', 'scared', 'lonely', 'tired', 'stressed']
        positive_words = ['happy', 'excited', 'great', 'good', 'amazing', 'wonderful', 'love', 'fantastic', 'awesome']
        
        negative_count = sum(1 for word in negative_words if word in text_lower)
        positive_count = sum(1 for word in positive_words if word in text_lower)
        
        if negative_count > positive_count:
            return "negative"
        elif positive_count > negative_count:
            return "positive"
        else:
            return "neutral"