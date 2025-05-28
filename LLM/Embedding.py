#Create Embedding Call To API
#Subscribe From scraper topic reingest to kafka with additional embedding

from LLM.BaseLLM import BaseLLM

class Embedding(BaseLLM):
    def __init__(self):
        super().__init__()
        self.api_url = "https://api.openai.com/v1/embeddings"
        self.model = "text-embedding-3-small"
    
    def execute(self, input: str):

        request_body = {
            "model": self.model,
            "input": input.replace("\n", " "),
        }

        response = self.post_request(self.api_url, request_body)

        return response['data'][0]['embedding']


if __name__ == "__main__":
    test = Embedding()
    print(test.execute("Hello Vector!"))
        