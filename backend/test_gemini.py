from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Safety check
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY not found in .env")

print("Testing Gemini API key validation...")

start_time = time.time()

try:
    # Make a test call to Gemini
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ],
        max_tokens=50,
        temperature=0.7
    )

    end_time = time.time()
    response_time = round(end_time - start_time, 2)

    print("\nGEMINI API KEY VALIDATION RESULT")
    print("----------------------------------------")
    print("Status: SUCCESS")
    print(f"Details: {response.choices[0].message.content}")
    print(f"Key used: {os.getenv('GEMINI_API_KEY')[:10]}...")
    print("Model used: gemini-2.5-flash")
    print(f"Response time: ~{response_time} seconds")

except Exception as e:
    end_time = time.time()
    response_time = round(end_time - start_time, 2)

    print("\nGEMINI API KEY VALIDATION RESULT")
    print("----------------------------------------")
    print("Status: FAILED")
    print(f"Details: {str(e)}")
    print(f"Key used: {os.getenv('GEMINI_API_KEY')[:10] if os.getenv('GEMINI_API_KEY') else 'NOT FOUND'}...")
    print("Model used: gemini-2.5-flash")
    print(f"Response time: ~{response_time} seconds")