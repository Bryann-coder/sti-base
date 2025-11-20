import google.generativeai as genai

import os
from dotenv import load_dotenv # Import nécessaire

load_dotenv() # Charge les variables du fichier .env

api_key = os.getenv("GEMINI_API_KEY")

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        genai.configure(api_key=api_key)
        
        # CORRECTION ICI : Utilisation du nom de modèle standard
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_response(self, prompt):
        try:
            generation_config = genai.types.GenerationConfig(
                candidate_count=1,
                temperature=0.7,
            )
            
            # Note : Ces réglages désactivent tous les filtres de sécurité.
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]

            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "Je suis désolé, je rencontre un problème technique pour vous répondre."