import requests


class BenoitBrain:

    def __init__(self, model="qwen3:latest"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"

    def ask(self, messages, tools=None):

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        if tools:
            payload["tools"] = tools

        response = requests.post(
            self.url,
            json=payload,
            timeout=600
        )

        response.raise_for_status()

        return response.json()["message"]