from assertions import assert_logs_update
from dotenv import load_dotenv
import openai
import json
import sys
import os
current_script_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.abspath(os.path.join(current_script_directory, ".."))
sys.path.append(project_directory)

from apikeylogger import decorate_openai
decorate_openai()

# Load the old token log
with open("logs.json", "r") as file:
    old_logs = json.load(file)

load_dotenv()

# Create the client as usual
client = openai.OpenAI()

model = "gpt-3.5-turbo-16k"

# Call the function as usual
response = client.chat.completions.create(
    messages = [
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model = model
)

# Assertion
assert_logs_update(
    OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID"),
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY"),
    model = model,
    old_logs = old_logs,
    prompt_tokens = response.usage.prompt_tokens,
    completion_tokens = response.usage.completion_tokens
)