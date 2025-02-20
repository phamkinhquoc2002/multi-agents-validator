from typing import Annotated
from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tavily import TavilyClient
import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
from dotenv import load_dotenv

load_dotenv()
tavily_api_key=os.environ['TAVILY_API_KEY']
tavily=TavilyClient(api_key=tavily_api_key)

def search_tool(query: Annotated[str, "Search query"]) -> Annotated[str, "The search results"]:
    return tavily.get_search_context(query=query, search_depth="advanced")

def get_llm_config(model_name: str,
                   api_key: str) -> List[Dict[str, str]]:
    llm_config=[{"model":model_name, "api_key":api_key}]
    return llm_config

def content_retrieval(url: str):
    try:
        responses=requests.get(url)
    except:
        print("There are certain errors in the pipeline")
    soup=BeautifulSoup(responses.text, 'html.parser')
    docs=soup.get_text()
    return markdownify(docs)

def youtube_transcript_loader(url: str) -> str:
    loader = YoutubeLoader.from_youtube_url(url)
    docs = loader.load()
    docs= ' '.join([doc.page_content for doc in docs])
    return docs

def text_splitter(docs):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    docs=text_splitter.create_documents(docs)
    return docs

def reflection_message(recipient, messages, sender, config):
    print("Reflecting...", "yellow")
    return f"Validate all important information. \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"
