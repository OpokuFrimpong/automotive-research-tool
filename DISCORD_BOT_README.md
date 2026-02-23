# 🎮 Discord Bot with LangChain

A Discord bot powered by LangChain that can have intelligent conversations and remember context per user.

## ✨ Features

- 💬 Natural conversations with AI
- 🧠 Remembers conversation history per user
- 🤖 Two LLM options: Ollama (free) or OpenAI
- ⚡ Responds to mentions and commands
- 🔧 Easy to customize and extend

## 🚀 Setup Instructions

### Step 1: Create Discord Bot

1. **Go to Discord Developer Portal**
   - Visit: https://discord.com/developers/applications
   - Click "New Application"
   - Give it a name (e.g., "LangChain Bot")

2. **Create the Bot**
   - Go to "Bot" tab (left sidebar)
   - Click "Add Bot"
   - Copy the **Token** (you'll need this!)

3. **Enable Intents**
   - In Bot settings, scroll down to "Privileged Gateway Intents"
   - ✅ Enable "Message Content Intent"
   - Save changes

4. **Invite Bot to Your Server**
   - Go to "OAuth2" → "URL Generator"
   - Select scopes: `bot`
   - Select permissions: `Send Messages`, `Read Messages/View Channels`, `Read Message History`
   - Copy the generated URL and open in browser
   - Select your server and authorize

### Step 2: Configure Environment

1. **Copy the example file**
   ```bash
   copy .env.example .env
   ```

2. **Edit `.env` and add your Discord token**
   ```
   DISCORD_BOT_TOKEN=your-token-here
   USE_OLLAMA=true
   ```

### Step 3: Choose Your LLM

**Option A: Ollama (Free, Local)**
1. Install Ollama: https://ollama.ai
2. Run: `ollama pull llama3.2`
3. Make sure `USE_OLLAMA=true` in `.env`

**Option B: OpenAI (Paid)**
1. Get API key from: https://platform.openai.com
2. Add to `.env`: `OPENAI_API_KEY=sk-...`
3. Set `USE_OLLAMA=false` in `.env`

### Step 4: Run the Bot

```bash
python discord_bot.py
```

You should see:
```
✅ YourBotName is now online!
📡 Connected to 1 server(s)
🧠 LLM: Ollama (Local)
```

## 💬 How to Use

### In Discord:

**Mention the bot:**
```
@BotName what's the weather like?
@BotName tell me about BMW
```

**Use commands:**
```
!chat what is LangChain?
!clear (clears your conversation history)
!help_bot (shows help)
```

## 🛠️ Customization Ideas

### Make it Automotive-Focused:

Edit the system prompt in `discord_bot.py`:
```python
("system", """You are an automotive expert assistant on Discord.
You specialize in BMW, Audi, and Bosch products.
Provide technical insights, troubleshooting help, and industry knowledge.
Keep responses concise for Discord.""")
```

### Add More Commands:

```python
@bot.command(name='diagnostics')
async def diagnostics(ctx, *, error_code: str):
    # Look up OBD-II codes
    await ctx.send(f"Looking up error code: {error_code}")
```

## 📚 Next Steps

1. **Add Tools**: Web search, Wikipedia, calculators
2. **Add RAG**: Load automotive PDFs for knowledge base
3. **Add Channels**: Different personalities per channel
4. **Add Reactions**: React to messages based on sentiment
5. **Add Slash Commands**: Modern Discord interactions

## 🐛 Troubleshooting

**Bot doesn't respond:**
- Check if Message Content Intent is enabled
- Make sure bot has permission to read/send messages
- Check bot is online in Discord

**Ollama errors:**
- Make sure Ollama is running
- Check model is installed: `ollama list`

**OpenAI errors:**
- Verify API key is correct
- Check you have credits

## 📖 Resources

- Discord.py Docs: https://discordpy.readthedocs.io
- LangChain Docs: https://python.langchain.com
- Discord Developer Portal: https://discord.com/developers
