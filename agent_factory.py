from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_experimental.utilities import PythonREPL
from langchain.agents import Tool
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_new_agent(model_to_use: str):
    logging.info(f"create_new_agent START with input {model_to_use}")
    python_repl = PythonREPL()
    repl_tool = Tool(
        name="python_repl",
        description="""A Python shell. Use this to execute python commands. Input should be a valid python command. 
        If you want to see the output of a value, you should print it out with `print(...)`.""",
        func=python_repl.run,
    )

    llm = ChatOllama(
        model=model_to_use,
        temperature=0,
    )
    agent = create_react_agent(
        llm,
        [repl_tool],

    )
    logging.info(f"*******************create_new_agent END Agent created")
    return agent
