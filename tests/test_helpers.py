import json

def assert_logs_update(OPENAI_ORG_ID, OPENAI_API_KEY, model, prompt_tokens, completion_tokens, old_logs):
    
    """
    This function asserts that the logs have been updated correctly, 
    by checking the prompt tokens and completion tokens before and after the request,
    knowing the amount of prompt tokens and completion tokens used for the request.
    
    :param OPENAI_ORG_ID: The OpenAI organization ID
    :param OPENAI_API_KEY: The OpenAI API key
    :param model: The model used for the request
    :param prompt_tokens: The number of prompt tokens used for the request
    :param completion_tokens: The number of completion tokens used for the request
    :param old_logs: The logs before the request was made
    """
    
    try:
        if old_logs == {}:
            previous_prompt_tokens = 0
            previous_completion_tokens = 0
        else:
            previous_prompt_tokens = old_logs[OPENAI_ORG_ID][OPENAI_API_KEY][model]['prompt_tokens']
            previous_completion_tokens = old_logs[OPENAI_ORG_ID][OPENAI_API_KEY][model]['completion_tokens']
    except Exception as e:
        print("Exception in assert_logs_update():",e)
        previous_prompt_tokens = 0
        previous_completion_tokens = 0
        
    with open("apikeylogs.json", "r") as file:
        new_logs = json.load(file)
    
    #print(f"{previous_prompt_tokens} + {prompt_tokens} =? {new_logs[OPENAI_ORG_ID][OPENAI_API_KEY][model]['prompt_tokens']}")
    #print(f"{previous_completion_tokens} + {completion_tokens} =? {new_logs[OPENAI_ORG_ID][OPENAI_API_KEY][model]['completion_tokens']}")
    
    assert previous_prompt_tokens + prompt_tokens == new_logs[OPENAI_ORG_ID][OPENAI_API_KEY][model]['prompt_tokens']
    assert previous_completion_tokens + completion_tokens == new_logs[OPENAI_ORG_ID][OPENAI_API_KEY][model]['completion_tokens']