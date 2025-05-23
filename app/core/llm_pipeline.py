# import openai
# import os

# openai.api_key = os.getenv("OPENAI_API_KEY")

# def llm_pipeline(prompt: str) -> str:
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "你是一個繁體中文助手"},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.7
#     )
#     return response['choices'][0]['message']['content']

import google.generativeai as genai
import os

# 讀取 API 金鑰
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 建立 Gemini 模型 client
model = genai.GenerativeModel("gemini-1.5-flash-8b") # small & stable 小型模型，專為較低智慧程度的任務而設計

def llm_pipeline(prompt: str) -> str:
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.7,
            "top_p": 0.95,
            "max_output_tokens": 1024
        }
    )
    return response.text