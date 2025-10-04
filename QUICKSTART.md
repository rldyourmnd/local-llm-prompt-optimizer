# Quick Start Guide

Get started with Local LLM Prompt Optimizer in 5 minutes.

## Prerequisites

1. **LM Studio** - Download and run: https://lmstudio.ai
   - Start the server (default: http://127.0.0.1:1234)
   - Load a model (e.g., Mistral, Llama, etc.)
   - Enable CORS in settings

2. **Docker** (Recommended) or **Node.js 20+** and **Python 3.11+**

## Option 1: Docker (Recommended)

### Step 1: Clone and Configure

```bash
git clone https://github.com/rldyourmnd/local-llm-prompt-optimizer.git
cd local-llm-prompt-optimizer

# Copy environment file
cp .env.example .env

# Edit .env if needed (defaults work for most cases)
```

### Step 2: Start Services

```bash
# Without Telegram bot
docker-compose up -d

# With Telegram bot (requires TELEGRAM_BOT_TOKEN in .env)
docker-compose --profile with-bot up -d
```

### Step 3: Access

- **Web UI**: http://localhost:3000
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

### Step 4: Test

Open http://localhost:3000 and try optimizing a prompt!

Example:
```
Prompt: "Write a function to sort an array"
Vendor: OpenAI
```

## Option 2: Local Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and configure .env
cp ../.env.example ../.env

# Run
uvicorn src.api.main:app --reload --port 8000
```

Visit: http://localhost:8000/api/docs

### Frontend

```bash
cd frontend
npm install

# Copy and configure .env
cp .env.example .env

# Run
npm run dev
```

Visit: http://localhost:5173

## Quick Test: API

### Test Health

```bash
curl http://localhost:8000/health
```

### Optimize a Prompt

```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain how neural networks work",
    "vendor": "claude"
  }'
```

## Quick Test: Telegram Bot

1. Get bot token from @BotFather
2. Add to `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ```
3. Start bot:
   ```bash
   docker-compose --profile with-bot up -d
   ```
4. Send `/start` to your bot
5. Send any prompt text

## Common Use Cases

### 1. Code Generation (DeepSeek)

**Input:**
```
Create a user authentication system
```

**Optimized for DeepSeek:**
```
## Objective
Create a user authentication system

## Technical Specifications
- Analyze requirements with precision
- Apply engineering best practices
- Consider edge cases and error handling
- Ensure code quality and maintainability
...
```

### 2. Document Analysis (Claude)

**Input:**
```
Analyze this quarterly report
```

**Optimized for Claude:**
```xml
<task>
Analyze this quarterly report
</task>

<instructions>
1. Read the task carefully and understand all requirements
2. Use <thinking> tags to show your reasoning process
3. Break down complex problems into steps
4. Provide thorough, well-structured responses
</instructions>
...
```

### 3. Conversational Query (Grok)

**Input:**
```
What's trending in AI?
```

**Optimized for Grok:**
```
**Your Task:**

What's trending in AI?

**Approach:**
- Use your real-time knowledge and current information
- Be thorough but keep it engaging
- Include relevant context from recent developments if applicable
- Feel free to add personality while staying helpful
...
```

## Vendor Selection Guide

| Task Type | Recommended Vendor | Why |
|-----------|-------------------|-----|
| Code Generation | DeepSeek | Optimized for code, strong technical reasoning |
| Long Documents | Claude | Excellent long-context, XML structure |
| Current Events | Grok | Real-time information access |
| Math/Logic | Qwen | Strong mathematical reasoning |
| Multi-modal | Gemini | Supports images, video, long context |
| General Tasks | OpenAI | Balanced, well-documented |

## Troubleshooting

### "LM Studio not available"

1. Ensure LM Studio is running
2. Check port: http://127.0.0.1:1234
3. Enable CORS in LM Studio settings
4. Test: `curl http://127.0.0.1:1234/v1/models`

### "Docker container fails to start"

```bash
# Check logs
docker-compose logs backend

# Rebuild
docker-compose down
docker-compose up -d --build
```

### "Frontend can't connect to backend"

Check `VITE_API_BASE_URL` in `frontend/.env`:
```
VITE_API_BASE_URL=http://localhost:8000
```

## Next Steps

1. **Read Full Documentation**: [README.md](README.md)
2. **API Usage Guide**: [docs/API_USAGE.md](docs/API_USAGE.md)
3. **Development Guide**: [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)
4. **Contribute**: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

## Example Scripts

### Python

```python
import requests

result = requests.post(
    "http://localhost:8000/api/optimize",
    json={
        "prompt": "Create a REST API",
        "vendor": "openai",
        "context": "Using FastAPI"
    }
).json()

print(result["optimized"])
```

### JavaScript

```javascript
const response = await fetch('http://localhost:8000/api/optimize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'Build a web scraper',
    vendor: 'deepseek',
    context: 'Using Python and BeautifulSoup'
  })
})

const result = await response.json()
console.log(result.optimized)
```

### cURL

```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Optimize database queries",
    "vendor": "gemini",
    "context": "PostgreSQL with 10M records"
  }' | jq '.optimized'
```

## Support

- **Issues**: https://github.com/rldyourmnd/local-llm-prompt-optimizer/issues
- **Discussions**: https://github.com/rldyourmnd/local-llm-prompt-optimizer/discussions
- **Email**: business@nddev.tech
- **Telegram**: @Danil_Silantyev

---

**NDDev OpenNetwork** | Built by Danil Silantyev | https://nddev.tech
