import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def translate(message, recipient_language='French'):
    # if message == None:
    #     return ""
    prompt: str
    prompt = "Translate this text: '" + message + "' to" + recipient_language
    # print(prompt)
    response = model.generate_content(prompt)
    # print(response.text)
    return response.text

# print(translate(message='The backpack is blue.', recipient_language='Japanese4ee'))