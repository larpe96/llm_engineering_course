import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Load environment variables in a file called .env
# Print the key prefixes to help with any debugging

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize
openai = OpenAI()
MODEL = 'gpt-4.1-mini'

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    raise RuntimeError("OpenAI API Key not set")


system_message = """You are my assitance, helping with my work and encurage me to continue.
I want you to be clear and short in response and tell me if you don't know an answer. 
I am a robotics engineer and work with code in python, c++ and using the vue framework.
"""

def chat(message, history):
    history = [{"role":h["role"], "content":h["content"]} for h in history]
    
    
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]

    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response



gr.ChatInterface(fn=chat, type="messages").launch()


