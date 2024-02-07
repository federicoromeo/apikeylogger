# apikeylogger

Track your *OpenAI* api usage **by key**, without any code change.

#### Installation

```bash
pip install apikeylogger
```

#### Setup
Create a *.env* file with your OpenAI api_key and organization_id ([find yours here](https://platform.openai.com/account/organization)), like this:
```bash
OPENAI_API_KEY = ""
OPENAI_ORG_ID = ""
```
Fastest way to do this is to copy the example file:


#### Usage
```python
# This call will transparently log your API usage by key in a local json file *logs.json*
from apikeylogger import decorate_openai
decorate_openai()

# Your normal code that uses openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    messages = [
        {
            "role": "user",
            "content": "What is the meaning of life?",
        }
    ],
    model = "gpt-3.5-turbo-16k" # any model
)
```
# REMOVE:
## PyPi

```bash
python setup.py sdist bdist_wheel
```

If you don't have one, create an account on PyPI.

Use twine to upload your distribution packages to PyPI:

```bash
twine upload dist/*
```