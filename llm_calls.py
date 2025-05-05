from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
import logging
from agent_factory import create_new_agent
from prompts import (get_feedback_sys_prompt, get_improved_sys_prompt, get_unit_test_sys_fd_prompt,
                     get_unit_test_sys_prompt, get_unit_test_sys_improved_prompt)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def get_feedback(code: str, model_to_use: str) -> str:
    """
    This function receives a Python code snippet and a model name as input,
    invokes the ChatOpenAI API for feedback on the code quality, efficiency,
    and adherence to best practices. It returns both the feedback message
    and any exception that occurred during the process.

    :param code: str - The Python code snippet to be reviewed.
    :param model_to_use: str - The name of the OpenAI language model for feedback.
    :return: Tuple[str, Exception] - A tuple containing the feedback message
                                    and an optional exception object if one occurred.
    """
    if not code or not model_to_use:
        raise ValueError("All parameters (code, model_to_use, and revision_feedback) must be provided.")

    logging.info(f"*****************************get_feedback START with input: {code} and {model_to_use}")
    feedback = ""
    try:
        reviewer_agent = create_new_agent(model_to_use)
        logging.info("agent created *************************************")
        messages = [
            SystemMessage(
                content=get_feedback_sys_prompt()
            ),
            HumanMessage(
                content=f"Please check this {code} and provide a constructive feedback"
            )
        ]
        result = await reviewer_agent.ainvoke({'messages': messages})
        feedback = result["messages"][-1].content
        logging.info(f"*****************************get_feedback END with output: {feedback}")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise ValueError(f"Failed to generate feedback: {str(e)}")

    return feedback


async def generate_improved_code(original_code: str, model_to_use: str, revision_feedback: str) -> str:
    """
    Generates an improved version of the given code based on provided feedback.

    :param original_code: The initial Python code to be revised.
    :param model_to_use: The name of the language model to use for code improvement (e.g., 'text-davinci-06-30').
    :param revision_feedback: A detailed description of the desired changes in the code.
    :return: An improved version of the original code based on the feedback.
    """

    # Set up logging
    if not model_to_use or not original_code or not revision_feedback:
        raise ValueError("All parameters (original_code, model_to_use, and revision_feedback) must be provided.")

    try:
        coder_agent = create_new_agent(model_to_use)
        logging.info("agent created *************************************")
        messages = [
            SystemMessage(
                content=get_improved_sys_prompt()
            ),
            HumanMessage(
                content=f"Given the following {original_code} and {revision_feedback}. Use the feedback to rewrite it"
            )
        ]
        result = await coder_agent.ainvoke({'messages': messages})
        new_code = result["messages"][-1].content
        return new_code

    except Exception as e:
        logging.error(f"An error occurred while generating improved code: {e}")
        raise ValueError(f"Failed to generate improved code: {str(e)}")


async def get_unit_test_feedback(code: str, unit_test: str, model_to_use: str) -> str:
    """
    Generates feedback on the provided Python code and unit test based on the specified model.

    Args:
        code (str): The Python function to be tested.
        unit_test (str): The corresponding unit test for the code snippet.
        model_to_use (str): The OpenAI model to use for generating feedback.

    Returns:
         The generated feedback.
    """

    logging.info(f"*****************************get_unit_test_feedback START with input: {code} and {model_to_use}")

    try:
        # Validate input parameters
        assert isinstance(code, str), "Code must be a string."
        assert isinstance(unit_test, str), "Unit test must be a string."
        assert isinstance(model_to_use, str), "Model to use must be a string."
        coder_agent = create_new_agent(model_to_use)
        logging.info("agent created *************************************")
        messages = [
            SystemMessage(
                content=get_unit_test_sys_fd_prompt()
            ),
            HumanMessage(
                content=f"Given the following python function: {code} and its {unit_test}. Provide a constructive feedback"
            )
        ]
        result = await coder_agent.ainvoke({'messages': messages})
        new_code = result["messages"][-1].content
        return new_code


    except Exception as e:
        logging.error(f"An error occurred while generating unit tests feedback: {e}")
        raise ValueError(f"Failed to generate unit tests feedback: {str(e)}")


async def generate_unit_test(code: str, model_to_use: str) -> str:
    """Generate unit tests for the given Python function.

        Args:
            code (str): The Python function to be tested.

        Returns:
            Tuple[str, List[Dict]]: A string containing the updated code with unit tests and a list of test cases.
        """
    try:
        coder_agent = create_new_agent(model_to_use)
        logging.info("agent created *************************************")
        messages = [
            SystemMessage(
                content=get_unit_test_sys_prompt()
            ),
            HumanMessage(
                content=f"Given the following python function: {code}. Provide unit tests. Ensure you cover all edge cases"
            )
        ]
        result = await coder_agent.ainvoke({'messages': messages})
        new_code = result["messages"][-1].content
        return new_code

    except Exception as e:
        logging.error(f"An error occurred while generating unit tests: {e}", exc_info=True)
        raise ValueError(f"Failed to generate unit tests: {str(e)}")


async def generate_improved_unit_tests(unit_tests: str, model_to_use: str, revision_feedback: str) -> str:
    """
    Generates improved unit tests using a given language model.

    Args:
        unit_tests (str): The unit tests to be generated.
        model_to_use (str): The language model to use for generating improved unit tests.

    Returns:
        str: The improved unit tests.
    """
    try:
        coder_agent = create_new_agent(model_to_use)
        logging.info("agent created *************************************")
        messages = [
            SystemMessage(
                content=get_unit_test_sys_improved_prompt()
            ),
            HumanMessage(
                content=f"Given the following {unit_tests} and {revision_feedback}. Use the feedback to rewrite them"
            )
        ]
        result = await coder_agent.ainvoke({'messages': messages})
        new_code = result["messages"][-1].content
        return new_code

    except Exception as e:
        logging.error(f"An error occurred while generating improved unit tests: {e}")
        raise ValueError(f"Failed to generate improved unit tests: {str(e)}")


async def process_prompt(prompt: str, model_to_use: str) -> str:
    logging.info(f"*****************************process_prompt START with input: {prompt} and {model_to_use}")
    if not prompt or not model_to_use:
        raise ValueError("All parameters (prompt, model_to_use) must be provided.")

    messages = [
        SystemMessage(content="You are a helpful AI assistant"),
        HumanMessage(content=prompt)
    ]
    llm = ChatOllama(
        model=model_to_use,
        temperature=0,
    )
    logging.info("LLM created")
    result = await llm.ainvoke(messages)

    logging.info(f"*****************************process_prompt END with output: {result.content} ")
    return result.content
