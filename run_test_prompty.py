import os

from dotenv import load_dotenv
from pathlib import Path
from promptflow.tracing import trace
from promptflow.core import Prompty

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# print("Environment Variables:")
# print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")
# print(f"OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL')}")
# print(f"OPENAI_MODEL_ID: {os.getenv('OPENAI_MODEL_ID')}")

BASE_DIR = Path(__file__).absolute().parent

@trace
def chat(question: str = "What's the capital of France?") -> str:
    """Flow entry function."""

    if "OPENAI_API_KEY" not in os.environ and "AZURE_OPENAI_API_KEY" not in os.environ:
        # load environment variables from .env file
        load_dotenv()

    prompty = Prompty.load(source=BASE_DIR / "prompties/pf-test-01.prompty")
    # trigger a llm call with the prompty obj
    output = prompty(question=question)
    return output

if __name__ == "__main__":
    response = chat("What's the capital of India? Only provide the city name.")
    print(response)