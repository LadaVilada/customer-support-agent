# Thoughtful AI Customer Support Agent

A modular customer support chatbot with FastAPI backend and Streamlit frontend.

## 🏗️ Architecture

This project uses a **client-server architecture**:

- **FastAPI Backend** (`app/api.py`): REST API serving `/chat` endpoint
- **Streamlit Frontend** (`streamlit_app.py`): Web UI that calls the FastAPI backend
- **Core Logic** (`app/chatbot.py`, `app/llm_client.py`, `app/matcher.py`): Shared business logic

### How Streamlit Communicates with FastAPI

1. **User Input**: User types a question in the Streamlit UI
2. **HTTP Request**: Streamlit sends a POST request to `http://localhost:8000/chat`
3. **Backend Processing**: FastAPI processes the request using the chatbot logic
4. **Response**: FastAPI returns a JSON response with the bot's answer
5. **UI Update**: Streamlit displays the response in the chat interface

## 🚀 Quick Start

### Option 1: Run Both Servers (Recommended for Development)

```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY=sk-your-api-key

# Run both FastAPI and Streamlit concurrently
python run_dev.py

```

This will start:
- **FastAPI Backend**: http://localhost:8000
- **Streamlit Frontend**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs

### Option 2: Run Servers Separately

**Terminal 1 - FastAPI Backend:**
```bash
uvicorn main:app --reload
```

**Terminal 2 - Streamlit Frontend:**
```bash
streamlit run streamlit_app.py
```

## 📁 Project Structure

```
customer-support-agent/
├── app/
│   ├── api.py              # FastAPI routes and endpoints
│   ├── chatbot.py          # Core chatbot logic
│   ├── config.py           # Configuration (URLs, thresholds, etc.)
│   ├── llm_client.py       # OpenAI client abstraction
│   ├── matcher.py          # FAQ matching logic
│   ├── qa_data.py          # Hardcoded Q&A dataset
│   └── utils.py            # Utility functions
├── tests/
│   ├── test_api.py         # API endpoint tests
│   └── test_chatbot.py     # Chatbot logic tests
├── main.py                 # FastAPI entrypoint
├── streamlit_app.py        # Streamlit frontend entrypoint
├── run_dev.py              # Development script (runs both servers)
└── requirements.txt        # Python dependencies
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_api.py
pytest tests/test_chatbot.py

# Run with coverage
pytest --cov=app
```

## 🔧 Configuration

All configuration is centralized in `app/config.py`:

- **FastAPI Settings**: Host, port, base URL
- **Streamlit Settings**: Port
- **Chatbot Settings**: Similarity threshold, OpenAI model
- **System Prompt**: Bot personality and instructions

## 🌐 API Endpoints

### POST `/chat`
Send a message to the chatbot.

**Request:**
```json
{
  "message": "What does CAM do?"
}
```

**Response:**
```json
{
  "response": "CAM streamlines the submission and management of claims..."
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

### GET `/`
API information and available endpoints.

## 🔄 Development Workflow

1. **Backend Changes**: Modify `app/api.py`, `app/chatbot.py`, etc.
2. **Frontend Changes**: Modify `streamlit_app.py`
3. **Test**: Run `pytest` to ensure everything works
4. **Run**: Use `python run_dev.py` for development

## 🚀 Production Deployment

For production, consider:

1. **Separate Frontend/Backend**: Deploy FastAPI and Streamlit on different servers
2. **Environment Variables**: Use proper environment management
3. **CORS Configuration**: Restrict CORS origins to your domain
4. **Load Balancing**: Use nginx or similar for the FastAPI backend
5. **Monitoring**: Add logging and health checks

## 📝 Notes

- No data is stored or logged
- For local demo/testing only
- Uses OpenAI GPT-3.5-turbo for fallback responses
- FAQ matching uses fuzzy string matching with configurable threshold 
