.PHONY: run install clean help

# Default target - setup and start the application
run: install
	@echo "🌟 Starting FastAPI server..."
	@echo "🌐 Open http://localhost:8000 in your browser to chat!"
	@. .venv/bin/activate && uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Install dependencies and setup virtual environment
install:
	@echo "🚀 Setting up chat app..."
	@if [ ! -f ".env" ]; then \
		echo "❌ Error: .env file not found"; \
		echo "Please copy .env.example to .env and add your OPENAI_API_KEY"; \
		echo "  cp .env.example .env"; \
		echo "  # Edit .env and add your API key"; \
		exit 1; \
	fi
	@if [ ! -d ".venv" ]; then \
		echo "📦 Creating virtual environment..."; \
		python -m venv .venv; \
	fi
	@echo "📥 Installing dependencies..."
	@. .venv/bin/activate && pip install -r requirements.txt

# Clean up virtual environment
clean:
	@echo "🧹 Cleaning up..."
	@rm -rf .venv
	@echo "✅ Virtual environment removed"

# Show help
help:
	@echo "Simple AskCR Demo - Available Commands:"
	@echo ""
	@echo "  make run     - Setup and start the chat app"
	@echo "  make install - Setup virtual environment and install dependencies"
	@echo "  make clean   - Remove virtual environment"
	@echo "  make help    - Show this help message"
	@echo ""
	@echo "First time setup:"
	@echo "  1. cp .env.example .env"
	@echo "  2. Edit .env and add your OPENAI_API_KEY"
	@echo "  3. make run"