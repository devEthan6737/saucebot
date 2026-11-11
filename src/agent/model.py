from langchain_deepseek import ChatDeepSeek

from src.config import DEEPSEEK_API_KEY

model = ChatDeepSeek(model="deepseek-chat", api_key=DEEPSEEK_API_KEY)
