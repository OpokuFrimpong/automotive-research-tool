"""
Simple LangChain Chatbot with Memory
Supports both Ollama (local) and OpenAI
"""

import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Load environment variables
load_dotenv()

def create_chatbot(use_ollama=True):
    """Create a chatbot with conversation memory"""
    
    if use_ollama:
        # Use Ollama (local, free)
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model="llama3.2", temperature=0.7)
        print("🤖 Using Ollama (Local) - Make sure Ollama is installed and running!")
        print("   Install: https://ollama.ai")
        print("   Then run: ollama pull llama3.2\n")
    else:
        # Use OpenAI (requires API key)
        from langchain_openai import ChatOpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        print("🤖 Using OpenAI GPT-3.5\n")
    
    # Create prompt template with memory
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Be friendly, concise, and helpful."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    # Create chain
    chain = prompt | llm
    
    # Add memory
    chat_history = InMemoryChatMessageHistory()
    
    chatbot = RunnableWithMessageHistory(
        chain,
        lambda session_id: chat_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    
    return chatbot

def main():
    print("=" * 60)
    print("🚗 LangChain Chatbot")
    print("=" * 60)
    
    # Choose your LLM provider
    print("\nChoose your LLM:")
    print("1. Ollama (Local - Free, requires Ollama installed)")
    print("2. OpenAI (Cloud - Requires API key)")
    
    choice = input("\nEnter choice (1 or 2, default=1): ").strip() or "1"
    
    use_ollama = choice == "1"
    
    try:
        chatbot = create_chatbot(use_ollama=use_ollama)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nIf using Ollama, make sure:")
        print("1. Ollama is installed: https://ollama.ai")
        print("2. Run: ollama pull llama3.2")
        print("3. Ollama is running")
        return
    
    print("\n✅ Chatbot ready! Type your messages below.")
    print("   (Type 'quit', 'exit', or 'q' to stop)\n")
    
    session_id = "default_session"
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            # Get response
            response = chatbot.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}}
            )
            
            print(f"\nBot: {response.content}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()
