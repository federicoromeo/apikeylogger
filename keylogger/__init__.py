from .decorators import chat_completion_decorator
from .decorators import client_decorator


def decorate_openai():
    """
    The function `decorate_openai` decorates the OpenAI client to add
    additional functionalities.
    """
    
    try:
        
        import openai
        #from openai import OpenAI
        
        # Force OpenAI to track the tokens usage separately for each key
        original_init = openai.OpenAI.__init__
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self.chat.completions.create = chat_completion_decorator(self.chat.completions.create)
        openai.OpenAI.__init__ = new_init
        
        # Force parameter organization to be specified, either as argument or as env variable
        openai.OpenAI.__init__ = client_decorator(openai.OpenAI.__init__)
        
    except ImportError:

        print("OpenAI not installed. Please install it with 'pip install openai'")
        


# Usage:

# import keylogger
# keylogger.decorate_openai()