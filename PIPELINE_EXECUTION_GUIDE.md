# Chat Flow Pipeline Execution Guide

## Overview
This guide explains how to execute the `chat-flow-02` pipeline locally using Promptflow.

## Implementation Details

### File: `run-chat-flow-02.py`

The implementation includes:

1. **Flow Component Loading**: Uses `load_component()` to load the flow definition from `flow.dag.yaml`
2. **Pipeline Definition**: Defines a `@pipeline()` decorated function for Azure ML pipeline execution
3. **Local Execution**: Implements `run_pipeline_locally()` for testing flows locally

## Running the Pipeline Locally

### Prerequisites
1. Environment variables loaded from `.env` file
2. Required packages installed (see `requirements.txt`)
3. Valid OpenAI API credentials

### Execution Command
```bash
python run-chat-flow-02.py
```

### How It Works

1. **PFClient Initialization**: Creates a Promptflow client
2. **Flow Testing**: Uses `pf.test()` method with inline inputs:
   - `flow`: Path to the flow directory (`./chat-flow-02`)
   - `inputs`: Dictionary containing `question` and `chat_history`
3. **Result Processing**: Extracts and consumes the generator to get the actual answer

### Example Output
```
Running chat pipeline locally...
Question: What's the capital of India? Only provide the city name.

Prompt flow service has started...
2025-11-23 23:04:26 -0500   53080 execution.flow     INFO     Start executing nodes in thread pool mode.
2025-11-23 23:04:26 -0500   53080 execution.flow     INFO     Start to run 1 nodes with concurrency level 16.
2025-11-23 23:04:26 -0500   53080 execution.flow     INFO     Executing node chat. node run id: 5dede06e-1c23-42d6-8e6f-f19cab27196c_chat_0
2025-11-23 23:04:27 -0500   53080 execution.flow     INFO     Node chat completes.
==================================================
Answer:
==================================================
New Delhi
```

## Key Components

### Flow Structure
```
chat-flow-02/
├── flow.dag.yaml       # Flow definition
├── chat.jinja2         # Prompt template
├── openai.yaml         # OpenAI connection config
├── azure_openai.yaml   # Azure OpenAI connection config
└── requirements.txt    # Flow dependencies
```

### Pipeline Function
```python
@pipeline()
def chat_pipeline(pipeline_question: str = "What's the capital of France?"):
    """Pipeline function with chat flow component."""
    chat_node = flow_component(
        question=pipeline_question,
        chat_history=[],
        connections={
            "chat": {
                "connection": "synthetic_cnn",
            }
        },
    )
    return {"answer": chat_node.outputs.answer}
```

### Local Execution Function
```python
@trace
def run_pipeline_locally(question: str = "What's the capital of France?"):
    """Run the flow locally using promptflow."""
    pf = PFClient()
    
    result = pf.test(
        flow="./chat-flow-02",
        inputs={
            "question": question,
            "chat_history": []
        }
    )
    
    return result
```

## Testing Different Questions

To test with different questions, simply modify the question in `__main__`:

```python
if __name__ == "__main__":
    question = "Your question here"
    result = run_pipeline_locally(question)
    # Process result...
```

## Troubleshooting

### Common Issues

1. **"Source must be a file with .prompty extension"**
   - Solution: Use `pf.test()` instead of `Prompty.load()` for flows with `flow.dag.yaml`

2. **"'flow' is required to create a run"**
   - Solution: Use `pf.test()` for single invocations, not `pf.run()`

3. **Generator object in result**
   - Solution: Consume the generator with `''.join(str(chunk) for chunk in answer)`

4. **Connection errors**
   - Solution: Ensure `.env` file has valid `OPENAI_API_KEY` and `OPENAI_BASE_URL`

## Next Steps

1. **Azure Execution**: Configure Azure ML workspace credentials to run on Azure
2. **Batch Processing**: Use `pf.run()` with a data file for batch processing
3. **Interactive Mode**: Use `pf flow test --flow chat-flow-02 --interactive` for CLI interaction
4. **Monitoring**: Check `.promptflow` folder for execution logs and traces

## References

- [Promptflow Documentation](https://microsoft.github.io/promptflow/)
- [Azure ML Pipeline Documentation](https://learn.microsoft.com/en-us/azure/machine-learning/concept-ml-pipelines)
- [Chat Flow Tutorial](https://github.com/microsoft/promptflow/tree/main/examples/flows/chat)

