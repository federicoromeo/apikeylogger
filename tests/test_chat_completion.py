from dotenv import load_dotenv
from openai import OpenAI
import json
import sys
import os
current_script_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.abspath(os.path.join(current_script_directory, ".."))
sys.path.append(project_directory)

from test_helpers import assert_logs_update
from apikeylogger.tiktoken_count import num_tokens_from_string, num_tokens_from_messages
from apikeylogger import track_openai
track_openai()


def test_chat_completion():

    # Load the old token logs
    try:
        with open("apikeylogs.json", "r") as file:
            old_logs = json.load(file)
    except:
        old_logs = {}
        
    load_dotenv()

    # Create the client as usual
    client = OpenAI()

    model = 'gpt-3.5-turbo-16k-0613'

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


def test_chat_completions_with_stream():

    # Load the old token logs
    try:
        with open("apikeylogs.json", "r") as file:
            old_logs = json.load(file)
    except:
        old_logs = {}
    
    load_dotenv()

    # Create the client as usual
    client = OpenAI()

    model = "gpt-3.5-turbo-0613"
    message = "Say this is a test"

    # Call the function as usual
    response = client.chat.completions.create(
        messages = [
            {
                "role": "user",
                "content": message,
            }
        ],
        model = model,
        stream = True
    )
        
    resp = ""
    for chunk in response.response:
        if chunk.choices[0].delta.content:
            resp += chunk.choices[0].delta.content
    
    prompt_tokens = num_tokens_from_messages(
        messages = [
            {
                "role": "user",
                "content": message,
            }
        ], 
        model = model
    )
    completion_tokens = num_tokens_from_string(resp, model)
    
    # Assertion
    assert_logs_update(
        OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID"),
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY"),
        model = model,
        old_logs = old_logs,
        prompt_tokens = prompt_tokens,
        completion_tokens = completion_tokens
    )
    

def test_chat_completion_with_raw_response():

    # Load the old token logs
    try:
        with open("apikeylogs.json", "r") as file:
            old_logs = json.load(file)
    except:
        old_logs = {}

    load_dotenv()

    # Create the client as usual
    client = OpenAI()

    model = 'gpt-3.5-turbo-16k-0613'

    # Call the function as usual
    response = client.chat.completions.with_raw_response.create(
        messages = [
            {
                "role": "user",
                "content": "Say this is a test!",
            }
        ],
        model = model
    )

    assert_logs_update(
        OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID"),
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY"),
        model = model,
        old_logs = old_logs,
        prompt_tokens = json.loads(response.text)["usage"]["prompt_tokens"],
        completion_tokens = json.loads(response.text)["usage"]["completion_tokens"]
    )
    
    
def test_chat_completion_with_options():

    # Load the old token logs
    try:
        with open("apikeylogs.json", "r") as file:
            old_logs = json.load(file)
    except:
        old_logs = {}

    load_dotenv()

    # Create the client as usual
    client = OpenAI()

    model = 'gpt-3.5-turbo-16k-0613'

    # Call the function as usual
    #response = client.with_options(timeout=5 * 1000).chat.completions.create(
    response = client.with_options(max_retries=5).chat.completions.create(
        messages = [
            {
                "role": "user",
                "content": "Say this is a test!",
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


# test_chat_completion()
# test_chat_completions_with_stream()
# test_chat_completion_with_raw_response()
# test_chat_completion_with_options()