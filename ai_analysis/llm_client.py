import os
from openai import OpenAI


class LLMClient:

    # 创建与AI大模型交互的客户端
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

    # 与AI大模型交互的函数
    def chat(self, messages, model="deepseek-chat"):

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False
        )

        return response.choices[0].message.content



if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ]
    answer = LLMClient().chat(messages, model="deepseek-chat")
    print(answer)