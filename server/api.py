"""
FastAPI Backend for AI Search Tool
Powered by LangChain
"""

import os
import asyncio
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from ddgs import DDGS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="AI Search Tool", version="1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class SearchRequest(BaseModel):
    question: str
    use_ollama: bool = True

# Response model
class SearchResponse(BaseModel):
    answer: str
    error: Optional[str] = None

# Cache chains to avoid re-initializing LLM on every request
_chains = {}

def get_chain(use_ollama: bool = True):
    """Get LangChain search chain (cached)"""
    key = "ollama" if use_ollama else "openai"
    if key in _chains:
        return _chains[key]

    # Initialize LLM
    if use_ollama:
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model="gemma:2b", temperature=0.7)
    else:
        from langchain_openai import ChatOpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful research assistant specialized in automotive technology.
        Analyze the search results and provide a clear, concise answer.
        Use bullet points for clarity.
        Focus on BMW, Audi, and Bosch when relevant."""),
        ("user", """Question: {question}

Search Results:
{search_results}

Provide a comprehensive answer based on these results.""")
    ])
    
    # Create chain and cache it
    chain = prompt | llm | StrOutputParser()
    _chains[key] = chain
    return chain

def run_search(query: str, max_results: int = 3) -> str:
    """Run a DuckDuckGo search and return formatted results"""
    try:
        with DDGS(timeout=10) as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return ""
        # Format results into a readable string
        formatted = []
        for r in results:
            formatted.append(f"Title: {r.get('title', 'N/A')}\nURL: {r.get('href', 'N/A')}\nSummary: {r.get('body', 'N/A')}")
        return "\n\n".join(formatted)
    except Exception as e:
        raise Exception(f"Search failed: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the frontend"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, "client", "static", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Search and generate AI answer"""
    
    try:
        # Validate input
        if not request.question or len(request.question.strip()) < 3:
            raise HTTPException(status_code=400, detail="Question too short")
        
        # Search web with error handling (run in thread to avoid blocking event loop)
        try:
            search_results = await asyncio.to_thread(run_search, request.question)
            print(f"DEBUG: Search results: {search_results[:500] if search_results else 'EMPTY'}")
        except Exception as search_error:
            # If search fails, return a helpful error message
            error_msg = str(search_error)
            print(f"DEBUG: Search error: {error_msg}")
            if "timeout" in error_msg.lower():
                return SearchResponse(
                    answer="Search request timed out. This might be due to network issues or firewall settings. Please check your internet connection and try again.",
                    error=f"Timeout error: {error_msg}"
                )
            else:
                return SearchResponse(
                    answer="Unable to perform web search. Please check your network connection.",
                    error=f"Search error: {error_msg}"
                )
        
        if not search_results or search_results.strip() == "":
            return SearchResponse(
                answer="No search results found. Try a different query.",
                error=None
            )
        
        # Get LangChain chain
        chain = get_chain(use_ollama=request.use_ollama)
        
        # Generate answer (run in thread to avoid blocking event loop)
        answer = await asyncio.to_thread(chain.invoke, {
            "question": request.question,
            "search_results": search_results
        })
        
        return SearchResponse(answer=answer, error=None)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "AI Search Tool is running"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI server...")
    print("📍 Frontend: http://localhost:8000")
    print("📍 API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
