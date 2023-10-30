import os
from langchain.llms import OpenAI

llm = OpenAI(
    openai_api_key=os.getenv('OPENAI_API_KEY'),
    openai_organization=os.getenv('OPENAI_ORG_ID'),
)
