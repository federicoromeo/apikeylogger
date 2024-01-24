"""import openai
import apikeylogger
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

apikeylogger.decorate_openai()

load_dotenv()

# Create the client as usual. Both methods work
client = OpenAI() #openai.OpenAI()

# Upload the file as usual
client.files.create(
    file = Path("input.jsonl"),
    purpose = "fine-tune",
)

# Creare a fine tuning job
try:
    response = client.fine_tuning.jobs.create(
        model = "gpt-3.5-turbo",
        training_file = "file-abc123",
        hyperparameters = {
            "n_epochs": 15,
            "batch_size": 3,
            "learning_rate_multiplier": 0.3
        }
    )
    job_id = response.id
    status = response.status

    print(f'Fine-tunning model with jobID: {job_id}.')
    print(f"Training Response: {response}")
    print(f"Training Status: {status}")
    
except openai.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except openai.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except openai.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)"""