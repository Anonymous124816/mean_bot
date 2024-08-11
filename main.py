from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API keys and tokens from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    return "The chatbot server is running!"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')
    
    try:
        # Use OpenAI GPT to generate a sarcastic/mean response
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can use other engines like "gpt-3.5-turbo"
            prompt=f"{incoming_msg}. Reply sarcastically.",
            max_tokens=50
        )
        response_msg = response.choices[0].text.strip()
    except Exception as e:
        # Fallback to a default response if GPT is unavailable
        response_msg = random.choice(default_responses)
    
    # Create a Twilio response
    resp = MessagingResponse()
    resp.message(response_msg)
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
