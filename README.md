# Promptflow101

A simple project demonstrating how to use Azure Prompt Flow with OpenAI-compatible APIs.

## Project Structure

```
Promptflow101/
├── main.py                 # Main entry point with chat function
├── pf-test-01.prompty     # Prompt flow template
├── test_env.py            # Environment variable test script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
└── README.md              # This file
```

## Features

- 🤖 Chat functionality using Prompt Flow
- 🔧 Environment-based configuration
- 🔄 Support for OpenAI-compatible APIs
- 📝 Prompty template for easy prompt management

## Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

## Setup

1. **Clone or download this project**

2. **Create and activate a virtual environment**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root with your API credentials:

   ```env
   OPENAI_API_KEY=your_api_key_here
   OPENAI_BASE_URL=https://api.openai.com/v1
   OPENAI_MODEL_ID=gpt-3.5-turbo
   ```

   Or use any OpenAI-compatible API (like the example uses Synthetic API or DeepSeek).

## Usage

### Method 1: Run Python Script Directly

```powershell
python main.py
```

The script will automatically load environment variables from `.env` and execute the chat function.

### Method 2: Use Prompt Flow CLI

To use the Prompt Flow CLI, you need to load environment variables first:

```powershell
# Load environment variables
$env:OPENAI_API_KEY = (Get-Content .env | Select-String 'OPENAI_API_KEY=' | ForEach-Object { $_ -replace 'OPENAI_API_KEY=', '' })
$env:OPENAI_BASE_URL = (Get-Content .env | Select-String 'OPENAI_BASE_URL=' | ForEach-Object { $_ -replace 'OPENAI_BASE_URL=', '' })
$env:OPENAI_MODEL_ID = (Get-Content .env | Select-String 'OPENAI_MODEL_ID=' | ForEach-Object { $_ -replace 'OPENAI_MODEL_ID=', '' })

# Run the flow
pf flow test --flow pf-test-01.prompty --inputs question="What's the capital of USA?"
```

### Method 3: Test Environment Variables

```powershell
python test_env.py
```

This will display the loaded environment variables to verify your configuration.

## Configuration

### Prompty File (`pf-test-01.prompty`)

The prompty file uses YAML frontmatter to define the model configuration:

```yaml
---
name: Minimal Chat
model:
  api: chat
  configuration:
    type: openai
    api_key: ${env:OPENAI_API_KEY}
    base_url: ${env:OPENAI_BASE_URL}
    model: ${env:OPENAI_MODEL_ID}
  parameters:
    temperature: 0.2
    max_tokens: 1024
inputs:
  question:
    type: string
---
```

The configuration automatically reads from environment variables using the `${env:VARIABLE_NAME}` syntax.

### Modifying the Chat Function

Edit `main.py` to customize the chat behavior:

```python
@trace
def chat(question: str = "What's the capital of France?") -> str:
    """Flow entry function."""
    
    if "OPENAI_API_KEY" not in os.environ and "AZURE_OPENAI_API_KEY" not in os.environ:
        load_dotenv()
    
    prompty = Prompty.load(source=BASE_DIR / "pf-test-01.prompty")
    output = prompty(question=question)
    return output
```

## Troubleshooting

### Issue: Connection Error with `pf flow test`

**Problem:** Getting `APIConnectionError: Connection error`

**Solution:** The Prompt Flow CLI doesn't automatically load `.env` files. Load environment variables manually before running the command (see Method 2 above).

### Issue: Invalid Choice 'main' Error

**Problem:** `pf flow: error: argument {init,save,test,serve,build,validate}: invalid choice: 'main'`

**Solution:** Use `pf flow test` instead of `pf flow main`.

### Issue: API Key Not Found

**Problem:** Environment variables not loading

**Solution:** 
1. Verify `.env` file exists in the project root
2. Check that `.env` file has correct variable names
3. Try running `python test_env.py` to verify

## Dependencies

Key dependencies (see `requirements.txt` for full list):

- `promptflow` - Azure Prompt Flow SDK
- `python-dotenv` - Environment variable management
- `openai` - OpenAI API client

## Security Notes

- ⚠️ Never commit your `.env` file to version control
- ⚠️ Keep your API keys secure
- ✅ Add `.env` to your `.gitignore` file

## License

This project is for educational purposes.

## Contributing

Feel free to submit issues and enhancement requests!

---

**Happy Prompting! 🚀**

