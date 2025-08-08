import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class for the application.
    
    Attributes:
        GEMINI_API_KEY (str): The API key for the Gemini service.
        SECRET_KEY (str): The secret key for the Flask application.
    """
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')

    if not GEMINI_API_KEY:
        raise ValueError("No GEMINI_API_KEY set for Gemini service")

    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")
        