# 🔍 AI-Powered Search Tool with LangChain

An intelligent web search tool that searches the internet and provides AI-summarized answers. Built with LangChain, FastAPI, and supports both local (Ollama) and cloud (OpenAI) LLMs.

Perfect for automotive industry research - BMW, Audi, Bosch, and more!

## 🌟 Features

- ✅ **AI-Powered Search**: Searches web and generates intelligent summaries
- ✅ **Dual LLM Support**: Choose between Ollama (free, local) or OpenAI (cloud)
- ✅ **Beautiful Web UI**: Modern, responsive interface
- ✅ **FastAPI Backend**: RESTful API with automatic documentation
- ✅ **LangChain Integration**: Built on industry-standard AI framework
- ✅ **Easy to Deploy**: Simple setup and deployment

## 📁 Project Structure

```
LangChain/
├── client/              # Frontend
│   └── static/
│       └── index.html   # Web UI
├── server/              # Backend
│   ├── api.py          # FastAPI backend (main app)
│   ├── chatbot.py      # CLI chatbot
│   ├── discord_bot.py  # Discord integration
│   └── search_tool.py  # Search tool CLI
├── .env.example        # Environment template
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Ollama (for local LLM) OR OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd LangChain
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or: source .venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install langchain langchain-community langchain-openai langchain-ollama fastapi uvicorn python-dotenv duckduckgo-search ddgs
   ```

4. **Set up environment**
   ```bash
   copy .env.example .env
   ```
   Edit `.env` and configure your LLM choice

### Option 1: Using Ollama (Free, Local)

1. **Install Ollama**: https://ollama.ai
2. **Download a model**:
   ```bash
   ollama pull gemma:2b
   ```
3. **Update `.env`**:
   ```
   USE_OLLAMA=true
   ```

### Option 2: Using OpenAI (Cloud)

1. **Get API key**: https://platform.openai.com/api-keys
2. **Update `.env`**:
   ```
   OPENAI_API_KEY=sk-your-key-here
   USE_OLLAMA=false
   ```

### Run the App

```bash
cd server
python api.py
```

Open your browser: **http://localhost:8000**

## 💬 Usage Examples

### Web Interface

1. Open http://localhost:8000
2. Select your LLM (Ollama or OpenAI)
3. Enter your query:
   - "Latest BMW electric vehicles 2026"
   - "Bosch automotive innovations"
   - "Audi Q5 technical specifications"
4. Get AI-summarized results!

### CLI Chatbot

```bash
cd server
python chatbot.py
```

### Discord Bot

See [DISCORD_BOT_README.md](DISCORD_BOT_README.md) for Discord integration.

## 🔧 API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### API Endpoints

**POST /api/search**
```json
{
  "question": "Latest BMW innovations",
  "use_ollama": true
}
```

Response:
```json
{
  "answer": "AI-generated summary...",
  "error": null
}
```

## 🛠️ Development

### Project Components

- **client/**: Frontend HTML/CSS/JS
- **server/api.py**: Main FastAPI application
- **server/chatbot.py**: Standalone CLI chatbot
- **server/discord_bot.py**: Discord bot integration
- **server/search_tool.py**: Command-line search tool

### Customize for Your Industry

Edit the system prompt in `server/api.py`:
```python
("system", """You are a helpful research assistant specialized in automotive technology.
Analyze the search results and provide a clear, concise answer.
Focus on BMW, Audi, and Bosch when relevant.""")
```

## 📚 Tech Stack

- **LangChain**: AI application framework
- **FastAPI**: Modern Python web framework
- **Ollama/OpenAI**: LLM providers
- **DuckDuckGo**: Web search API
- **Uvicorn**: ASGI server

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - feel free to use for personal or commercial projects!

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Ollama Models](https://ollama.ai/library)
- [OpenAI API](https://platform.openai.com)

---

Built with ❤️ for the automotive industry
