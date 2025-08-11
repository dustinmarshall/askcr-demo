# Simple AskCR Demo

A minimal version of the AskCR app built with FastAPI and vanilla JavaScript. Features streaming responses, conversation history, and a minimal Web UI interface.

## 🛠️ Prerequisites

- **Python 3.10+**
- **OpenAI API Key** - Get yours from [OpenAI Platform](https://platform.openai.com/)

## 🚀 Quick Start

1. **Setup environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

2. **Run the application:**
   ```bash
   make run
   ```

3. **Open your browser:**
   Navigate to `http://localhost:8000` and start chatting!

## 📋 Available Commands

```bash
make run      # Setup and start the chat app
make install  # Setup environment and dependencies only  
make clean    # Remove virtual environment
make help     # Show all available commands
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serve the web interface |
| `GET` | `/health` | Health check endpoint |
| `POST` | `/chat` | Chat with streaming response |

### Chat API Example
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

## 🏗️ Architecture

- **Backend**: FastAPI with OpenAI integration
- **Frontend**: Vanilla HTML/CSS/JavaScript 
- **Streaming**: Server-Sent Events (SSE) for real-time responses
- **State**: Client-side conversation history management

## 📝 Development Notes

- CORS is configured for local development
- Virtual environment is automatically managed
- No frontend build process required
- Conversation context is maintained in browser memory
- Error handling for API failures and network issues
