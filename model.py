import requests
from pydantic import BaseModel, Field
from langchain.llms import BaseLLM

class CustomModelConfig(BaseModel):
    api_url: str
    api_key: str
    user_name: str
    bot_name: str
    memory: str

class CustomModelLLM(BaseLLM):
    api_url: str = Field(...)
    api_key: str = Field(...)
    user_name: str = Field(...)
    bot_name: str = Field(...)
    memory: str = Field(...)

    def __init__(self, config: CustomModelConfig):
        super().__init__(api_url=config.api_url, api_key=config.api_key)
        self.api_url = config.api_url
        self.api_key = config.api_key
        self.user_name = config.user_name
        self.bot_name = config.bot_name
        self.memory = config.memory

    @property
    def _llm_type(self) -> str:
        return "custom_model"

    def _generate(self, prompt: str, stop: list = None):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        payload = {
            "memory": self.memory,
            "prompt": prompt,
            "bot_name": self.bot_name,
            "user_name": self.user_name,
            "chat_history": []
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        response_data = response.json()
        return {
            "choices": [
                {
                    "text": response_data.get('model_output', '')
                }
            ]
        }

    def _call(self, prompt: str, stop: list = None) -> str:
        return self._generate(prompt, stop)['choices'][0]['text']
