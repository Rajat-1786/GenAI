from dotenv import load_dotenv
from anthropic import Anthropic
from data import messages

import config

load_dotenv()
class execute_query:
    def __init__(self):
        self.client = Anthropic()

    def execute(self,messages, system_prompt= None):
        params = {
            "model": config.model,
            "max_tokens": config.max_tokens,
            "messages": messages,
            "temperature": 0.0,
            # "stream": config.stream uncomment it if we need to use create method
        }

        if system_prompt:
            params["system"] = system_prompt

        try:
            with self.client.messages.stream(**params) as stream:
                for text in stream.text_stream:
                    print(text, end="", flush=True)

                message = stream.get_final_message()

            print(f"Message: {message}")
            return {"message": message.content[0].text, "input_tokens": message.usage.input_tokens, "output_tokens": message.usage.output_tokens}
        
        except Exception as e:
            print(f"Error executing query: {e}")
            return None








