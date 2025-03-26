# AI-Powered Automation API

A FastAPI-based REST API that provides intelligent automation using Google's Gemini LLM (Large Language Model) and RAG (Retrieval Augmented Generation) for natural language processing and dynamic function execution.

## Features

- Natural language processing using Gemini AI
- Dynamic function retrieval using RAG
- Intelligent command interpretation and execution
- Open applications (Chrome, Calculator, Notepad)
- Get system metrics (CPU and RAM usage)
- Execute shell commands
- RESTful API interface
- Support for custom user-defined functions
- Comprehensive logging system

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd automation_api
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.template .env
```
Edit .env and add your Google Gemini API key:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

To get a Gemini API key:
1. Visit Google AI Studio (https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and paste it in your .env file

## Running the API

Start the FastAPI server:
```bash
python app.py
```

The server will start at `http://localhost:8000`. You can access:
- API endpoint: `http://localhost:8000/execute`
- Interactive API documentation: `http://localhost:8000/docs`
- OpenAPI specification: `http://localhost:8000/openapi.json`

## AI Features

### LLM Integration
The API uses Google's Gemini AI to:
- Understand natural language prompts
- Generate executable Python code
- Extract parameters from user requests
- Provide intelligent error messages

### RAG Implementation
The API uses RAG with HuggingFace embeddings to:
- Store function descriptions and metadata
- Retrieve the most relevant function based on user prompts
- Support dynamic addition of custom functions
- Provide semantic search capabilities

## API Usage

### 1. Execute Commands Using Natural Language

Send natural language prompts to execute functions:

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"prompt": "what is the current cpu usage"}'
```

The API will:
1. Process the natural language using Gemini
2. Find the most relevant function using RAG
3. Execute the function and return results

Example Response:
```json
{
    "success": true,
    "action": "get_cpu_usage",
    "result": "CPU Usage: 45.2%",
    "error": null
}
```

### 2. Register Custom Functions

Register new functions with natural language descriptions:

```bash
curl -X POST http://localhost:8000/register-function \
  -H "Content-Type: application/json" \
  -d '{
    "name": "greet_user",
    "code": "def greet_user(name=\"World\"):\n    return f\"Hello, {name}!\"",
    "description": "Greet a user with a customizable welcome message"
  }'
```

The function is:
- Added to the vector store with its description
- Made available for natural language queries
- Automatically considered during prompt processing

### 3. List Available Functions

View all registered functions with their descriptions:

```bash
curl http://localhost:8000/list-functions
```

Example Response:
```json
{
    "functions": [
        {
            "name": "get_cpu_usage",
            "type": "system",
            "description": "Get current CPU usage percentage"
        },
        {
            "name": "greet_user",
            "type": "custom",
            "description": "Greet a user with a customizable welcome message"
        }
    ]
}
```

## Project Structure

```
automation_api/
├── README.md
├── requirements.txt
├── .env.template
├── app.py                 # FastAPI application
├── ai_engine.py          # Gemini and RAG implementation
├── automation_functions.py # Core automation functions
└── automation_api.log     # Application logs
```

## Technology Stack

- FastAPI: Web framework
- Google Gemini: Language model integration
- LangChain: RAG implementation
- HuggingFace: Embeddings generation
- FAISS: Vector store for function embeddings
- Pydantic: Data validation
- Python-dotenv: Environment management

## Error Handling and Logging

The API includes comprehensive error handling and logging:
- LLM processing errors
- Function retrieval issues
- Execution failures
- All operations are logged with timestamps
- Detailed error messages for debugging

Example Error Response:
```json
{
    "success": false,
    "action": "unknown",
    "error": "No relevant function found for the given prompt"
}
```

## Development

The project follows these best practices:
- Modular code structure
- Type hints and Pydantic models
- Comprehensive error handling
- Detailed logging
- AI-powered function discovery
- Clear separation of concerns
- Custom function support