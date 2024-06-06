# Ragification Agents
In today's digital landscape, misinformation can spread rapidly, making it crucial to validate online sources. This repository aims to empower users with an AI Agents-powered tool to assess the trustworthiness of information found on the web.
## Multi-AI Agent Conversation Framework
**_Techstack used:_** streamlit, langchain, autogen
**_Description:_** the system contains two agents: researcher and questioner. The first one is programmed to extract key insights from the loaded documents, the second one uses those insights as an input to perform a validation framework, using a search_tool (Tavily) and ReAct prompt engineering.
____________________________________________________________________________________
![framework](https://github.com/phamkinhquoc2002/Ragification/blob/main/presentation.png)
____________________________________________________________________________________
### Run it locally
```
streamlit run app.py
```
