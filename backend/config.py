import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
    MODEL_NAME = "microsoft/DialoGPT-medium"
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')