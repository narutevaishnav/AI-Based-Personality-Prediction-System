import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

try:
    user = client.get_user(username="OpenAI")

    if user.data:
        print("✅ API Connected Successfully")
        print("User:", user.data.username)
    else:
        print("❌ User not found")

except Exception as e:
    print("❌ Error:", e)