import json
from dotenv import load_dotenv
from anthropic import AsyncAnthropic

import config

load_dotenv()
class execute_query:
    def __init__(self):
        self.client = AsyncAnthropic()

    async def chat(self, messages, system_prompt= None):
        params ={
            "model": config.model,
            "max_tokens": config.max_tokens,
            "messages": messages,
            "temperature": 0.0
            # "stream": config.stream uncomment it if we need to use create method
        }

        if system_prompt:
            params["system"] = system_prompt
        try:
            message =await self.client.messages.create(**params)
            print(f"Message: {message}")
            return {"message": message.content[0].text, "input_tokens": message.usage.input_tokens, "output_tokens": message.usage.output_tokens} 
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    async def stream(self,messages, system_prompt= None):
        params = {
            "model": config.model,
            "max_tokens": config.max_tokens,
            "messages": messages,
            "temperature": 0.0
        }

        if system_prompt:
            params["system"] = system_prompt

        async with self.client.messages.stream(**params) as stream:
            async for text in stream.text_stream:
                yield text
            message = await stream.get_final_message()

        print({
            "input_tokens": message.usage.input_tokens, 
            "output_tokens": message.usage.output_tokens
            })


    async def generate_policy(self, description, system_prompt=None):
        params ={
            "model": config.model,
            "max_tokens": config.max_tokens,
            "messages":[
                {
                    "role": "user",
                    "content": description
                },
                {
                    "role": "assistant",
                    "content": "```json"
                }
            ],
            "stop_sequences": ["```"]
        }

        if system_prompt:
            params["system"] = system_prompt

        try:
            message =await self.client.messages.create(**params)
            print(f"Message: {message}")
            return json.loads(message.content[0].text)
        except Exception as e:
            print(f"Error generating policy: {e}")
            return None









