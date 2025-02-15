# import openai
# import os

# def call_llm(prompt, image=None):
#     """Calls GPT-4o-Mini via OpenAI."""
#     headers = {"Authorization": f"Bearer {os.getenv('AIPROXY_TOKEN')}"}
#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
#         headers=headers
#     )
#     return response["choices"][0]["message"]["content"]

# import openai
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# api_key = os.getenv("AIPROXY_TOKEN")

# if not api_key:
#     raise ValueError("AIPROXY_TOKEN is not set. Please check your environment variables.")

# openai.api_key = api_key

# def call_llm(prompt, image_path=None):
#     """Calls GPT-4o-Mini for text, or GPT-4 Turbo Vision if an image is provided."""
#     messages = [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": prompt},
#     ]
    
#     if image_path:
#         messages.append({"role": "user", "content": {"image_url": f"file://{image_path}"}})
    
#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini" if not image_path else "gpt-4-turbo",
#         messages=messages
#     )
    
#     return response.choices[0].message["content"]

import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API key
api_key = os.getenv("AIPROXY_TOKEN")

if not api_key:
    raise ValueError("AIPROXY_TOKEN is not set. Please check your environment variables.")

client = openai.OpenAI(api_key=api_key,
                       base_url="https://aiproxy.sanand.workers.dev/openai/v1")  # ✅ New API format

def call_llm(prompt, image_path=None):
    """Calls GPT-4o-Mini for text, or GPT-4 Turbo Vision if an image is provided."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    
    if image_path:
        messages.append({"role": "user", "content": {"image_url": f"file://{image_path}"}})
    
    response = client.chat.completions.create(  # ✅ Updated method
        model="gpt-4o-mini" if not image_path else "gpt-4-turbo",
        messages=messages
    )
    
    return response.choices[0].message.content
