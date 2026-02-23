"""
AI-Powered Search Tool using LangChain
Searches the web and provides AI-summarized answers
"""

import os
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

def create_search_tool(use_ollama=True):
    """Create AI search assistant"""
    
    # Initialize LLM
    if use_ollama:
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model="llama3.2", temperature=0.7)
        print("Using Ollama (Local)\n")
    else:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        print(" Using OpenAI\n")
    
    # Initialize search tool
    search = DuckDuckGoSearchResults(num_results=5)
    
    # Create prompt for summarizing search results
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful research assistant. 
        Analyze the search results and provide a clear, concise answer to the user's question.
        Use the search results as your source of truth.
        If the results don't contain enough information, say so.
        Format your response in a clear, readable way with bullet points when appropriate."""),
        ("user", """Question: {question}
        
Search Results:
{search_results}

Please provide a comprehensive answer based on these search results.""")
    ])
    
    # Create chain
    chain = prompt | llm | StrOutputParser()
    
    return search, chain

def search_and_answer(question, search_tool, chain):
    """Search web and generate AI answer"""
    
    print(f"🔍 Searching for: {question}")
    print("⏳ Fetching results...\n")
    
    # Get search results
    try:
        search_results = search_tool.invoke(question)
    except Exception as e:
        return f"❌ Search error: {e}"
    
    if not search_results:
        return "❌ No results found. Try a different query."
    
    print("✅ Results found! Generating AI summary...\n")
    
    # Generate AI answer
    try:
        answer = chain.invoke({
            "question": question,
            "search_results": search_results
        })
        return answer
    except Exception as e:
        return f"❌ AI error: {e}"

def main():
    print("=" * 70)
    print("🔍 AI-Powered Search Tool (LangChain)")
    print("=" * 70)
    
    # Choose LLM
    print("\nChoose your LLM:")
    print("1. Ollama (Local - Free, requires Ollama installed)")
    print("2. OpenAI (Cloud - Requires API key)")
    
    choice = input("\nEnter choice (1 or 2, default=1): ").strip() or "1"
    use_ollama = choice == "1"
    
    print()
    
    try:
        search_tool, chain = create_search_tool(use_ollama=use_ollama)
    except Exception as e:
        print(f"❌ Setup error: {e}")
        if use_ollama:
            print("\n⚠️  Make sure Ollama is installed and running:")
            print("   1. Install: https://ollama.ai")
            print("   2. Run: ollama pull llama3.2")
        return
    
    print("✅ Search tool ready!")
    print("\nExamples:")
    print("  • Latest BMW electric vehicles 2026")
    print("  • Bosch automotive innovations")
    print("  • Audi Q5 technical specifications")
    print("\nType 'quit' or 'exit' to stop\n")
    print("-" * 70)
    
    while True:
        try:
            question = input("\n🔎 Your question: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            print()
            answer = search_and_answer(question, search_tool, chain)
            
            print("=" * 70)
            print("📝 AI Answer:")
            print("=" * 70)
            print(answer)
            print("=" * 70)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
