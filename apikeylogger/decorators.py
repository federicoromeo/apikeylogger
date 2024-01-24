import os
import json
import logging
from .tiktoken_count import num_tokens_from_string, num_tokens_from_messages


def client_decorator(func):
    """
    Decorator that forces the client to have the organization in kwargs
    
    :param func: The function to decorate
    
    :return: The decorated function
    """
    
    def wrapper(*args, **kwargs):
        
        logging.warning(" Decorating the client")

        if 'organization' not in kwargs.keys():
            if not 'OPENAI_ORG_ID' in os.environ.keys():
                raise Exception("Please specify the 'organization' when instantiating the OpenAI client, or insert it in the environment variable as 'OPENAI_ORG_ID'. Find yours at 'https://platform.openai.com/account/organization'")
        
        response = func(*args, **kwargs)
        
        return response
    
    return wrapper


def chat_completion_raw_response_decorator(func):
    """
    Decorator that logs the tokens used for the request and the response
    for the raw response endpoint
    
    :param func: The function to decorate
    
    :return: The decorated function
    """
    
    def wrapper(*args, **kwargs):
        
        logging.warning(" Decorating the chat completion function for the raw response")

        def get_model(args, kwargs):
            if 'model' in kwargs.keys():
                return kwargs['model']
            elif len(args) > 0:
                # The model is the second argument
                return args[1]
            else:
                raise Exception("No model specified")
        
        def get_logger_dict():
            if os.path.exists('logs.json'):
                with open('logs.json', 'r') as f:
                    d = json.load(f)
                return d
            return {}
        
        def log_tokens(model, prompt_tokens, completion_tokens):

            log_dict = get_logger_dict()           

            organization_id = os.environ.get('OPENAI_ORG_ID')
            api_key = os.environ.get('OPENAI_API_KEY')

            # Create the nested dictionary structure
            log_dict.setdefault(organization_id, {}).setdefault(api_key, {}).setdefault(model, {}).setdefault('prompt_tokens', 0)
            log_dict.setdefault(organization_id, {}).setdefault(api_key, {}).setdefault(model, {}).setdefault('completion_tokens', 0)

            # Update token counts
            log_dict[organization_id][api_key][model]['prompt_tokens'] += prompt_tokens
            log_dict[organization_id][api_key][model]['completion_tokens'] += completion_tokens

            with open('logs.json', 'w') as f:
                json.dump(log_dict, f)
        
            print()
            print(log_dict)
        
        response = func(*args, **kwargs)
        
        # Get the tokens from the response
        response_copy = json.loads(response.text)
        completion_tokens = response_copy['usage']['completion_tokens']
        prompt_tokens = response_copy['usage']['prompt_tokens']
        
        # Get the model used for the request
        model = get_model(args, kwargs)
        
        log_tokens(model, prompt_tokens, completion_tokens)

        return response
    
    return wrapper


def chat_completion_decorator(func):
    """
    Decorator that logs the tokens used for the request and the response
    
    :param func: The function to decorate
    
    :return: The decorated function
    """
    
    def wrapper(*args, **kwargs):
        
        logging.warning(" Decorating the chat completion function")

        def get_model(args, kwargs):
            if 'model' in kwargs.keys():
                return kwargs['model']
            elif len(args) > 0:
                # The model is the second argument
                return args[1]
            else:
                raise Exception("No model specified")
        
        def get_logger_dict():
            if os.path.exists('logs.json'):
                with open('logs.json', 'r') as f:
                    d = json.load(f)
                return d
            return {}
        
        def log_tokens(model, prompt_tokens, completion_tokens):

            log_dict = get_logger_dict()           

            organization_id = os.environ.get('OPENAI_ORG_ID')
            api_key = os.environ.get('OPENAI_API_KEY')

            # Create the nested dictionary structure
            log_dict.setdefault(organization_id, {}).setdefault(api_key, {}).setdefault(model, {}).setdefault('prompt_tokens', 0)
            log_dict.setdefault(organization_id, {}).setdefault(api_key, {}).setdefault(model, {}).setdefault('completion_tokens', 0)

            # Update token counts
            log_dict[organization_id][api_key][model]['prompt_tokens'] += prompt_tokens
            log_dict[organization_id][api_key][model]['completion_tokens'] += completion_tokens

            with open('logs.json', 'w') as f:
                json.dump(log_dict, f)
        
            print()
            print(log_dict)
        
        response = func(*args, **kwargs)
        
        if "stream" in kwargs.keys() and kwargs["stream"] == True:
                                
            
            if not "messages" in kwargs.keys():
                if len(args) > 0:
                    # The messages are the first argument
                    messages = args[0]
                else:
                    raise Exception("No messages specified in chat completion with stream")
            else:
                messages = kwargs["messages"]
            
            prompt_tokens = num_tokens_from_messages(messages, model)

            completion_tokens = num_tokens_from_string(response.choices[0].message.content, model)

        else:
        
            # Get the tokens from the response
            completion_tokens = response.usage.completion_tokens
            prompt_tokens = response.usage.prompt_tokens
        
        # Get the model used for the request
        model = get_model(args, kwargs)
        
        log_tokens(model, prompt_tokens, completion_tokens)

        return response
    
    return wrapper
