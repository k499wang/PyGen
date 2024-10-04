import google.generativeai as genai
import os

try:
    genai.configure(api_key=os.environ["API_KEY"])
except KeyError:
    print("API_KEY not found in environment variables. Please set the API_KEY variable")

model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

prompt = "Paraphrase the following paragraph. Give only one response"

def paraphrase(text):
    response = chat.send_message(prompt+ ": "+ text)
    return response.text



    

