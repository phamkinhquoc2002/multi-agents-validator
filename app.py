import streamlit as st
import os
from dotenv import load_dotenv
from utils import search_tool, youtube_transcript_loader, content_retrieval, reflection_message
from agents import Agents
from autogen.coding import LocalCommandLineCodeExecutor


load_dotenv()
tavily_api_key=os.environ['TAVILY_API_KEY']
openai_api_key=os.environ['OPENAI_API_KEY']


code_executor=LocalCommandLineCodeExecutor(work_dir='./coding')

st.set_page_config(page_title="Ragification Agents", page_icon=":robot:")

st.markdown(
    """<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');
    </style>""", unsafe_allow_html=True
)

st.header("RAGIFICATION: THE TRUTH SEEKER")
col1, col2 = st.columns(2)

with col1:
    st.markdown(
    """
        <div style="text-align: justify;
        font-family: 'Space Mono', monospace;">
        
        Dear all my conspiracy theory debunkers, video essay youtubers, internet busiest redditors, academic researchers as well as passionate debaters,"
        the internet is flooded with misinformation, ambiguous arguments and potential biases. For that very reason, this web app was created with a view to assisting you all to find the absolute truth
        and paving the way for a more skeptical attitude on curating and using different sources of information. Every piece of content, in the format of video or text can be validated with my AI Agents. Have fun while using the tool :knife_fork_plate:</div>
    """, unsafe_allow_html=True
    )
    
with col2:
    st.image(
        image='logo.png',
        width=400,
        caption='The logo represents a concept called Kata in Japanese, which means method, imply the importance of choosing the right way to do things'
    )
    
topic = st.text_input(label="Topic of your documents", placeholder="Ex:Politic, Meme, Culture, Philosophy,...", key="topic")
youtube_url = st.text_input(label="Youtube URL", placeholder="Link to the video you want to validate", key="youtube-video")
article=st.text_input(label="Article", placeholder="Link to the articles, piece of content you want to validate", key="article")

button=st.button("Assess the information", type="secondary", help="Click to validate your information")

agents=Agents(model_names={"researcher":"gpt-3.5-turbo", "questioner":"gpt-4o"}, code_executor=code_executor, api_key=openai_api_key)
agents.register_function(tool=search_tool)
agents.register_nested_chat(reflection_message=reflection_message)

if button:
    if not (topic or youtube_url or article):
        st.warning('Please provide links to your content', icon="⚠️")
        st.stop()
        
    elif not (youtube_url):
        article_content=content_retrieval(article)
        docs = article_content
    elif not (article):
        youtube_content=youtube_transcript_loader(youtube_url)
        docs=youtube_content
    elif (article and youtube_url):
        youtube_content=youtube_transcript_loader(youtube_url)
        article_content=content_retrieval(article)
        docs=f"from youtube: {youtube_content} \n, from article: {article_content}" 
    
    prompt=f"Here is the content about {topic} that I'm skeptical about: \n {docs}"
    
    output=agents.validate(task=prompt)
    st.write("Sending information to the agents...")
    st.write(output)
    