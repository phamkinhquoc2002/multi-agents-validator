# Multi-agentic Information Validator 🤖
An experiment using autogen AI Conversation Framework to create a team of AI Agents to assess quality and trustworthiness of any types of content from the internet.

## Multi-AI Agent Conversation Framework
**_Techstack used:_** streamlit, langchain, autogen.

**_Description:_** the system contains two agents: researcher and questioner. The first one is programmed to extract key insights from the loaded documents, the second one uses those insights as an input to perform a validation framework, using a search_tool (Tavily) and ReAct prompt engineering.

### Run it locally
```
streamlit run app.py
```
