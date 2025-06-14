import os
import requests
from logger import logging

GENAI_API_KEY = os.getenv('GENAI_API_KEY', 'Google API')
MODEL = 'gemini-2.0-flash'
API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GENAI_API_KEY}"
)
HEADERS = {'Content-Type': 'application/json'}

def generate_learning_plan(topic, level, weeks, language='English'):
    prompt = (
        f"Create a {weeks}-week personalized learning plan for someone "
        f"who wants to learn '{topic}'. Skill level: {level}. "
        f"Respond in {language}. Include weekly goals, key concepts as bullet points, and free resources."
    )
    payload = {'contents': [{'parts': [{'text': prompt}]}]}
    try:
        resp = requests.post(API_URL, headers=HEADERS, json=payload)
        resp.raise_for_status()
        return resp.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        logging.error(f"Plan generation error: {e}")
        return None

def generate_chat_response(message, language='English'):
    prompt = (
        f"Act as a friendly learning coach who motivates and teaches in {language}. "
        f"User says: {message}"
    )
    payload = {'contents': [{'parts': [{'text': prompt}]}]}
    try:
        resp = requests.post(API_URL, headers=HEADERS, json=payload)
        resp.raise_for_status()
        return resp.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        logging.error(f"Chat response error: {e}")
        return "Sorry, I can't respond right now."
