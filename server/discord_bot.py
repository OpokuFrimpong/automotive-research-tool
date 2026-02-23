"""
Discord Bot powered by LangChain
Responds to messages with AI and remembers conversations per user
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Store chat histories per user
chat_histories = {}

def get_chat_history(user_id: str):
    """Get or create chat history for a user"""
    if user_id not in chat_histories:
        chat_histories[user_id] = InMemoryChatMessageHistory()
    return chat_histories[user_id]

def create_langchain_bot(use_ollama=True):
    """Create LangChain chatbot"""
    
    if use_ollama:
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model="llama3.2", temperature=0.7)
        print("🤖 Using Ollama (Local)")
    else:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        print("🤖 Using OpenAI")
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful Discord bot assistant. 
        Be friendly, concise (Discord messages should be short), and helpful.
        Keep responses under 2000 characters."""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = prompt | llm
    
    # Create chatbot with memory
    chatbot = RunnableWithMessageHistory(
        chain,
        get_chat_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    
    return chatbot

# Initialize LangChain bot
USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"
langchain_bot = create_langchain_bot(use_ollama=USE_OLLAMA)

@bot.event
async def on_ready():
    """When bot connects to Discord"""
    print(f'✅ {bot.user} is now online!')
    print(f'📡 Connected to {len(bot.guilds)} server(s)')
    print(f'🧠 LLM: {"Ollama (Local)" if USE_OLLAMA else "OpenAI"}')
    print('\nBot is ready to chat! Mention the bot or use !chat command')

@bot.event
async def on_message(message):
    """Handle incoming messages"""
    
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Process commands first
    await bot.process_commands(message)
    
    # Respond if bot is mentioned
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        # Remove bot mention from message
        content = message.content.replace(f'<@{bot.user.id}>', '').strip()
        
        if not content:
            await message.channel.send("Hi! How can I help you? 😊")
            return
        
        # Show typing indicator
        async with message.channel.typing():
            try:
                # Get response from LangChain
                response = langchain_bot.invoke(
                    {"input": content},
                    config={"configurable": {"session_id": str(message.author.id)}}
                )
                
                # Send response (split if too long)
                response_text = response.content
                if len(response_text) > 2000:
                    # Split into chunks
                    chunks = [response_text[i:i+2000] for i in range(0, len(response_text), 2000)]
                    for chunk in chunks:
                        await message.channel.send(chunk)
                else:
                    await message.channel.send(response_text)
                    
            except Exception as e:
                await message.channel.send(f"❌ Sorry, I encountered an error: {str(e)}")
                print(f"Error: {e}")

@bot.command(name='chat')
async def chat_command(ctx, *, question: str):
    """Chat with the bot using !chat <message>"""
    async with ctx.typing():
        try:
            response = langchain_bot.invoke(
                {"input": question},
                config={"configurable": {"session_id": str(ctx.author.id)}}
            )
            
            await ctx.reply(response.content[:2000])
            
        except Exception as e:
            await ctx.reply(f"❌ Error: {str(e)}")

@bot.command(name='clear')
async def clear_history(ctx):
    """Clear your conversation history"""
    user_id = str(ctx.author.id)
    if user_id in chat_histories:
        chat_histories[user_id].clear()
        await ctx.reply("✅ Your conversation history has been cleared!")
    else:
        await ctx.reply("You don't have any conversation history yet!")

@bot.command(name='help_bot')
async def help_command(ctx):
    """Show bot help"""
    help_text = """
**🤖 Discord LangChain Bot Commands**

**Ways to chat:**
• Mention me: `@BotName your question`
• Use command: `!chat your question`

**Commands:**
• `!chat <message>` - Chat with the bot
• `!clear` - Clear your conversation history
• `!help_bot` - Show this help message

**Features:**
✅ Remembers your conversation
✅ Powered by LangChain
✅ Natural language understanding
    """
    await ctx.send(help_text)

def main():
    """Start the Discord bot"""
    # Get Discord token
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    
    if not discord_token:
        print("❌ Error: DISCORD_BOT_TOKEN not found in .env file")
        print("\nTo set up your Discord bot:")
        print("1. Go to: https://discord.com/developers/applications")
        print("2. Create a New Application")
        print("3. Go to 'Bot' tab and create a bot")
        print("4. Copy the token and add to .env file")
        print("5. Enable 'Message Content Intent' in Bot settings")
        print("6. Invite bot using OAuth2 URL Generator")
        return
    
    # Check LLM setup
    if USE_OLLAMA:
        print("\n⚠️  Make sure Ollama is running and llama3.2 is installed!")
        print("   Install: https://ollama.ai")
        print("   Run: ollama pull llama3.2\n")
    else:
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ Error: OPENAI_API_KEY not found in .env file")
            return
    
    # Run bot
    try:
        bot.run(discord_token)
    except discord.LoginFailure:
        print("❌ Invalid Discord token! Check your .env file")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if __name__ == "__main__":
    main()
