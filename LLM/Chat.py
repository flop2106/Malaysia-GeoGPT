#main constructor to chat with GPT
from LLM.BaseLLM import BaseLLM

class Chat(BaseLLM):
    def __init__(self):
        super().__init__()
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4o-mini"
        self.history = []

    def execute(self, message:str, role:str = ""):
        messages = []
        if len(self.history) != 0:
            messages = self.history[-1]
        
        new_messages = [
            {
                "role": "system",
                "content": role
            }
            ,
            {
                "role": "user",
                "content": message
            }
        ]
        messages.extend(new_messages)
        request_body = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }
        data = self.post_request(self.api_url, request_body)
        return data["choices"][0]["message"]["content"]
    
if __name__ == "__main__":
    test = Chat()
    print(test.execute("hello GPT"))


        