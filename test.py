from openai import OpenAI #import openai
from dotenv import load_dotenv
import keylogger

keylogger.decorate_openai()

load_dotenv()

# Create the client as usual. Both methods work
client = OpenAI() #openai.OpenAI()

# Call the function as usual
response = client.chat.completions.create(
    messages = [
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model = "gpt-3.5-turbo-16k"
)

print(response.choices[0].message.content)
