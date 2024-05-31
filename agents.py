from autogen import UserProxyAgent, AssistantAgent, register_function
from autogen.coding import LocalCommandLineCodeExecutor
from utils import get_llm_config

class Agents():
    
    def __init__(self, model_names:dict, code_executor, api_key):
        self.researcher=AssistantAgent(
            name="researcher",
            system_message="You are a researcher tasked with summarizing notable information from a given context. Your role is to analyze the provided research content related to a topic. You should concisely summarize the 5 most relevant insights, facts, in bullet points while remaining unbiased. Your goal is to provide notable pơints of the content to facilitate further validation.",
            llm_config={"config_list":get_llm_config(model_name=model_names['researcher'], api_key=api_key)}
        )
        self.user_proxy=UserProxyAgent(
             name="SearchTool",
             is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
             human_input_mode="NEVER",
             max_consecutive_auto_reply=10,
             code_execution_config={"executor": code_executor},
        )
        self.questioner= AssistantAgent(
            name="questioner",
            llm_config={"config_list":get_llm_config(model_name=model_names['researcher'], api_key=api_key)},
            system_message="You are a critical thinker tasked for assessing the credibility of information from various angles."
            "Your role is to carefully analyze the information summarized by the Researcher, and validate the quality as well as trustworthiness of that information."
            "You should assess every piece of insight by questioning its logic, accuracy and biases."
            "You have access to tools provided. Use the following format:"
            "Information: the insights that need to be assessed"
            "Thought: you should always think about what to do"
            "Action: the action to take"
            "Action Input: the input to the action"
            "Observation: the result of the action"
            "... (this process can repeat multiple times)"
            "Thought: I now know the final argument"
            "Final Answer: return the trustworthiness score, quality score of that information and reasons for that")
    
    def register_function(self, tool):
        register_function(
            tool,
            caller=self.questioner,
            executor=self.user_proxy,
            name="search_tool",
            description="Search the web for the given query"
        )   
        
    def register_nested_chat(self, reflection_message):
        self.user_proxy.register_nested_chats(
            [{
                "recipient":self.questioner,
                "message":reflection_message,
                "summary_method":"last_msg",
                "max_turns":2
            }],
            trigger=self.researcher
        )
        
    def validate(self, task):
        res=self.user_proxy.initiate_chat(
            recipient=self.researcher,
            message=task,
            max_turns=2, 
            summary_method="last_msg"
        )
        return res.chat_history