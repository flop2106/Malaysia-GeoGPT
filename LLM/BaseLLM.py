#main abstract for Chat and Embedding
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import requests
import os
import utils.LoggerBaseUtil as LoggerBaseUtil

logger = LoggerBaseUtil.setup()

class BaseLLM(ABC):
    def __init__(self):
        #create main_config and env code
        self.env_path = ".env"
        load_dotenv(dotenv_path = self.env_path)
        self.API_KEY = os.getenv('openai')
    
    def post_request(self, api_url: str, request_body:dict):

        try:
            headers = {
                "Authorization": f"Bearer {self.API_KEY}",
                "Content-Type": "application/json"
            }
            response = requests.post(api_url, headers=headers, json=request_body)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Error communicating with OpenAI: {str(e)}"
    
    @abstractmethod
    def execute(self):
        pass

if __name__  == "__main__":
    BaseLLM()