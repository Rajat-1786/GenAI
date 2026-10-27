from dotenv import load_dotenv
from anthropic import Anthropic
import config

load_dotenv()
class execute_query:
    def __init__(self):
          
        self.client = Anthropic()

    def execute(self,user_input):
        try:
            message = self.client.messages.create(
                model=config.model,
                max_tokens=config.max_tokens,
                messages=[
                    {
                        "role":"user",
                        "content": user_input
                    }
                ]
            )
            print(f"Message: {message}")
            return message.content[0].text
        except Exception as e:
            print(f"Error executing query: {e}")
            return None








