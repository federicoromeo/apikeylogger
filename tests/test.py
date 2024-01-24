from dotenv import load_dotenv
import openai
import os

load_dotenv()

# Create the client as usual.
client = openai.OpenAI()


model = "gpt-3.5-turbo-16k",
messages = [
    {
        "role": "user", 
        "content": "make a sum with 1 and 2."
    }
]


# Call the function as usual
completion = client.chat.completions.create(
    messages = messages,
    model = model,
)


print("completion 1:")
print(completion.usage)
print()

# append the model output to the messages list

messages.append(
    {
        "role": "assistant",
        "content": completion.choices[0].message.text
    }
)

messages.append(
    {
        "role": "user", 
        "content": "now make a subtraction with those numbers."
    }
)

completion = client.chat.completions.create(
    messages = messages,
    model = model
)

print("completion 2:")
print(completion.usage)
print()


