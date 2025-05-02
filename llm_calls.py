from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "http://localhost:11434/v1"
API_KEY = "ollama"
def get_feedback(code: str, model_name: str) -> str:
    """
    This function receives a Python code snippet and a model name as input,
    invokes the ChatOpenAI API for feedback on the code quality, efficiency,
    and adherence to best practices. It returns both the feedback message
    and any exception that occurred during the process.

    :param code: str - The Python code snippet to be reviewed.
    :param model_name: str - The name of the OpenAI language model for feedback.
    :return: Tuple[str, Exception] - A tuple containing the feedback message
                                    and an optional exception object if one occurred.
    """
    logging.info(f"*****************************get_feedback START with input: {code} and {model_name}")
    feedback = ""
    try:
        llm = ChatOpenAI(model=model_name, temperature=0, base_url=BASE_URL, api_key=API_KEY)
        messages = [
            SystemMessage(
                content="""Assume the role of an experienced Senior Software Engineer. You are tasked with reviewing
                 a Python code snippet written by a junior developer. Provide constructive, detailed feedback, highlighting 
                 areas of strength as well as suggesting improvements for better code quality, efficiency, and adherence 
                 to best practices in Python programming. DO NOT PROVIDE AN IMPROVED VERSION OF THE CODE.
                 YOU MUST ONLY RETURNS A FEEDBACK NO CODE."""
            ),
            HumanMessage(
                content=f"Please check this {code} and provide a constructive feedback"
            )
        ]

        feedback = llm.invoke(messages).content.strip()
        logging.info(f"*****************************get_feedback END with output: {feedback}")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise ValueError(f"Failed to generate feedback: {str(e)}")

    return feedback


def generate_improved_code(original_code: str, model_to_use: str, revision_feedback: str) -> str:
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
        llm = ChatOpenAI(model=model_to_use, temperature=0, base_url=BASE_URL, api_key=API_KEY)

        messages = [
            SystemMessage(
                content="""Embrace the role of an accomplished Senior Software Engineer with a deep understanding of 
                Python development. Your assignment involves revising a Python code segment authored by a junior developer. 
                After thoroughly reviewing the detailed feedback, enact your extensive coding expertise to refine the code,
                 addressing the specific issues outlined. Deliver an updated version that represents a clear enhancement
                  upon the initial code, leveraging Python's best practices and your seasoned development experience. 
                  """
            ),
            HumanMessage(
                content=f"Given the following {original_code} and {revision_feedback}. Use the feedback to rewrite it"
            )
        ]

        new_code = llm.invoke(messages).content.rstrip()  # Remove trailing whitespace

        return new_code

    except Exception as e:
        logging.error(f"An error occurred while generating improved code: {e}")
        raise ValueError(f"Failed to generate improved code: {str(e)}")


def get_unit_test_feedback(code: str, unit_test: str, model_to_use: str) -> str:
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

        llm = ChatOpenAI(
            model=model_to_use,
            temperature=0,
            base_url=BASE_URL,
            api_key=API_KEY
        )

        messages = [
            SystemMessage(
                content="""Embrace the role of an accomplished Senior Software Engineer with a deep understanding of 
                Python development and unit testing. Your assignment involves revising unit tests authored by a junior developer.
                Review the provided Python unit tests and provide detailed feedback on their quality, effectiveness, 
                and adherence to best practices. Highlight strengths, such as well-covered scenarios or robust assertions,
                and suggest improvements for areas like test organization, edge case coverage, and test maintainability. 
                Focus on providing actionable feedback that would help the developer enhance their testing skills and code quality. 
                Return feedback in a clear and concise manner, without including any code snippets.
                DO NOT PROVIDE AN IMPROVED VERSION OF THE CODE.YOU MUST ONLY RETURNS A FEEDBACK NO CODE.
                     """
            ),
            HumanMessage(
                content=f"Given the following python function: {code} and its {unit_test}. Provide a constructive feedback"
            )
        ]

        feedback = llm.invoke(messages).content.rstrip()  # Remove trailing whitespace

        return feedback

    except Exception as e:
        logging.error(f"An error occurred while generating unit tests feedback: {e}")
        raise ValueError(f"Failed to generate unit tests feedback: {str(e)}")


def generate_unit_test(code: str, model_to_use: str) -> str:
    """Generate unit tests for the given Python function.

        Args:
            code (str): The Python function to be tested.

        Returns:
            Tuple[str, List[Dict]]: A string containing the updated code with unit tests and a list of test cases.
        """
    try:
        llm = ChatOpenAI(model=model_to_use, temperature=0, base_url=BASE_URL, api_key=BASE_URL)

        messages = [
            SystemMessage(
                content="""Write comprehensive unit tests for the given Python function.
                     Ensure that your tests cover all edge cases, including valid and invalid inputs, boundary values, 
                     and potential exceptions. Provide your tests in a format compatible with the unittest framework.
                      Before providing your response, verify that your tests are syntactically correct and would run successfully
                        """
            ),
            HumanMessage(
                content=f"Given the following python function: {code}. Provide unit tests. Ensure you cover all edge cases"
            )
        ]

        new_code = llm.invoke(messages).content.rstrip()  # Remove trailing whitespace

        return new_code

    except Exception as e:
        logging.error(f"An error occurred while generating unit tests: {e}", exc_info=True)
        raise ValueError(f"Failed to generate unit tests: {str(e)}")


def generate_improved_unit_tests(unit_tests: str, model_to_use: str, revision_feedback: str) -> str:
    """
    Generates improved unit tests using a given language model.

    Args:
        unit_tests (str): The unit tests to be generated.
        model_to_use (str): The language model to use for generating improved unit tests.

    Returns:
        str: The improved unit tests.
    """
    try:

        llm = ChatOpenAI(model=model_to_use, temperature=0, base_url=BASE_URL, api_key=BASE_URL)

        messages = [
            SystemMessage(
                content="""
                           """
            ),
            HumanMessage(
                content=f"Given the following {unit_tests} and {revision_feedback}. Use the feedback to rewrite them"
            )
        ]

        new_code = llm.invoke(messages).content.rstrip()  # Remove trailing whitespace

        return new_code

    except Exception as e:
        logging.error(f"An error occurred while generating improved unit tests: {e}")
        raise ValueError(f"Failed to generate improved unit tests: {str(e)}")
