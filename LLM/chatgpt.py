import os
from LLM.config import gpt_model

from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取 API 密钥
api_key = os.getenv("OPENAI_API_KEY")

# 使用获取的 API 密钥初始化
client = OpenAI(api_key=api_key)

def call_gpt(messages):
    # 调用 ChatGPT API
    response = client.chat.completions.create(
        model=gpt_model,
        messages=messages,
        temperature=1,
    )
    return response.choices[0].message.content