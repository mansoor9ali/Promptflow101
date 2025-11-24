from pathlib import Path

from azure.ai.ml import load_component
from azure.ai.ml.dsl import pipeline
from dotenv import load_dotenv
from promptflow.client import PFClient
from promptflow.tracing import trace

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).absolute().parent

# Load the flow component
flow_component = load_component(source="./chat-flow-02/flow.dag.yaml")

@pipeline()
def chat_pipeline(
    pipeline_question: str = "What's the capital of France?",
):
    """Pipeline function with chat flow component."""

    # Declare pipeline step 'chat_node' by using flow component
    chat_node = flow_component(
        # Map the pipeline input to flow inputs
        question=pipeline_question,
        chat_history=[],
        # Provide the connection values - using OpenAI connection
        connections={
            "chat": {
                "connection": "synthetic_cnn",  # This should match your connection name
            }
        },
    )

    # Return pipeline output
    # return {"answer": chat_node.outputs.answer}


@trace
def run_pipeline_locally(question: str = "What's the capital of France?"):
    """Run the flow locally using promptflow."""
    pf = PFClient()

    # Test the flow with inline inputs
    return pf.test(
        flow="./chat-flow-02",
        inputs={
            "question": question,
            "chat_history": []
        }
    )


if __name__ == "__main__":
    question = "What's the capital of India? Only provide the city name."
    print("Running chat pipeline locally...")
    print(f"Question: {question}\n")

    # Use the simpler method for single invocation
    result = run_pipeline_locally(question)

    print("="*50)
    print("Answer:")
    print("="*50)

    # Extract the answer from the result
    if isinstance(result, dict) and 'answer' in result:
        answer = result['answer']
        # If it's a generator, consume it
        if hasattr(answer, '__iter__') and not isinstance(answer, str):
            answer = ''.join(str(chunk) for chunk in answer)
        print(answer)
    else:
        print(result)
