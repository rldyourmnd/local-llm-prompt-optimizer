# Development Guide

## Prerequisites

- **Python 3.11+** for backend
- **Node.js 20+** for frontend
- **Docker & Docker Compose** for containerized deployment
- **LM Studio** running locally (default: http://127.0.0.1:1234)

## Local Development Setup

### 1. Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp ../.env.example ../.env
# Edit .env with your settings

# Run development server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000
API docs at: http://localhost:8000/api/docs

### 2. Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with API URL

# Run development server
npm run dev
```

Frontend will be available at: http://localhost:5173

### 3. Telegram Bot Development

```bash
cd telegram-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Ensure TELEGRAM_BOT_TOKEN is set in root .env
# Run bot
python src/bot.py
```

## Project Structure

```
local-llm-prompt-optimizer/
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── api/               # API routes and schemas
│   │   ├── application/       # Application services
│   │   ├── domain/            # Domain models and business logic
│   │   │   ├── models/        # Data models
│   │   │   ├── interfaces/    # Abstract interfaces
│   │   │   └── vendors/       # Vendor-specific adapters
│   │   └── infrastructure/    # External integrations
│   │       ├── llm/           # LM Studio client
│   │       └── config/        # Settings management
│   ├── tests/                 # Backend tests
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                  # React + TypeScript frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API client
│   │   └── types/             # TypeScript types
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── telegram-bot/              # Telegram bot integration
│   ├── src/
│   │   └── bot.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docs/                      # Documentation
├── .github/workflows/         # CI/CD pipelines
└── docker-compose.yml         # Container orchestration
```

## Architecture Overview

### Domain-Driven Design (DDD)

The backend follows DDD principles:

- **Domain Layer**: Core business logic, vendor adapters, models
- **Application Layer**: Use cases and services
- **Infrastructure Layer**: External integrations (LM Studio, DB)
- **API Layer**: HTTP endpoints and request/response handling

### Vendor Adapters

Each LLM vendor has a dedicated adapter implementing `IVendorAdapter`:

- `OpenAIAdapter` - Markdown structure, few-shot learning
- `ClaudeAdapter` - XML tags, thinking blocks
- `GrokAdapter` - Conversational tone, real-time context
- `GeminiAdapter` - Structured format, multi-step reasoning
- `QwenAdapter` - Multilingual, mathematical reasoning
- `DeepSeekAdapter` - Code optimization, technical structure

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_vendor_adapters.py -v

# Run specific test
pytest tests/test_health.py::test_health_endpoint_returns_200 -v
```

### Frontend Tests

```bash
cd frontend

# Lint
npm run lint

# Type check
npx tsc --noEmit

# Build test
npm run build
```

## Code Quality

### Backend

```bash
# Format code
black src/ tests/

# Lint
flake8 src/ --max-line-length=127

# Type check
mypy src/ --ignore-missing-imports
```

### Frontend

```bash
# Lint and fix
npm run lint -- --fix

# Type check
npx tsc --noEmit
```

## Docker Development

### Build Images

```bash
# Build backend
docker build -f backend/Dockerfile -t llm-optimizer-backend ./backend

# Build frontend
docker build -f frontend/Dockerfile -t llm-optimizer-frontend ./frontend

# Build telegram bot
docker build -f telegram-bot/Dockerfile -t llm-optimizer-bot ./telegram-bot
```

### Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# Start with telegram bot
docker-compose --profile with-bot up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## Environment Variables

See `.env.example` for all configuration options. Key variables:

### Backend
- `LM_STUDIO_BASE_URL` - LM Studio API endpoint
- `LM_STUDIO_MODEL` - Model name (optional)
- `APP_PORT` - Backend server port
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

### Telegram Bot
- `TELEGRAM_BOT_TOKEN` - Bot token from @BotFather
- `TELEGRAM_ALLOWED_USER_IDS` - Comma-separated user IDs

### Frontend
- `VITE_API_BASE_URL` - Backend API URL

## Adding a New Vendor

1. Create adapter in `backend/src/domain/vendors/`
2. Implement `IVendorAdapter` interface
3. Add vendor to `VendorType` enum
4. Register in `OptimizationService`
5. Add tests in `tests/test_vendor_adapters.py`
6. Update frontend types in `frontend/src/types/`
7. Update README documentation

## Debugging

### Backend

Use Python debugger or add logging:

```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Frontend

Use browser DevTools or add console logs:

```typescript
console.log('Debug:', data)
```

### LM Studio Connection Issues

1. Ensure LM Studio is running
2. Check LM Studio is on correct port (default 1234)
3. Verify "Enable CORS" in LM Studio settings
4. Test with: `curl http://127.0.0.1:1234/v1/models`

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes following code standards
4. Run tests: `pytest` (backend) and `npm run lint` (frontend)
5. Commit using Conventional Commits: `feat: add new vendor`
6. Push and create Pull Request

## Security

- Never commit secrets to git
- Use `.env` for sensitive configuration
- API keys and tokens in environment variables only
- Follow OWASP security best practices
- Run security scans: `docker run --rm aquasec/trivy fs .`

## Performance

- LLM calls are async for better concurrency
- Frontend uses React.memo for optimization
- Docker images use multi-stage builds
- Nginx compression enabled for frontend assets

## Troubleshooting

**Backend won't start**
- Check Python version (3.11+)
- Verify all dependencies installed
- Check `.env` configuration
- Review logs for errors

**Frontend won't build**
- Check Node version (20+)
- Clear node_modules and reinstall
- Check for TypeScript errors
- Verify Vite configuration

**Bot doesn't respond**
- Verify bot token is correct
- Check user ID is in allowed list
- Ensure LM Studio is accessible
- Check bot logs for errors

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [React Documentation](https://react.dev)
- [LM Studio API](https://lmstudio.ai)
- [Python Telegram Bot](https://python-telegram-bot.org)
