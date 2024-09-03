from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
import os
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
load_dotenv()

azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

model = AzureChatOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=api_key,
    openai_api_version=api_version,
    model="gpt-4o-standard"
)

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

parser=StrOutputParser()
chain=prompt_template | model| parser

app=FastAPI(
    title="Langchain Tutorial",
    version="1.0",
)

add_routes(app,chain,path="/chain")

if __name__=="__main__":
    import uvicorn

    uvicorn.run(app,host="localhost",port=8000)
    #It will work on this url:  http://localhost:8000/chain/playground/