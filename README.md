# Local LLM Prompt Optimizer

**[English](#english) | [Русский](#russian)**

---

**Part of NDDev OpenNetwork**
**Author:** Danil Silantyev ([@rldyourmnd](https://github.com/rldyourmnd))
**Contact:** business@nddev.tech | https://nddev.tech

---

## English

### Overview

Local LLM Prompt Optimizer is a privacy-focused tool for optimizing prompts across multiple LLM vendors using local AI processing. All computations run through LM Studio on your machine—no external API calls or data transmission.

**License:** MIT
**Version:** 1.0.0
**Language:** Python 3.11+, TypeScript
**Architecture:** Domain-Driven Design with microservices

### Features

- **Local-first processing**: All AI operations via LM Studio
- **Multi-vendor support**: OpenAI, Claude, Grok, Gemini, Qwen, DeepSeek
- **Think Mode**: AI-generated clarifying questions for precision optimization
- **Multiple interfaces**: Web UI, REST API, Telegram bot
- **Clean architecture**: DDD principles with vendor adapters
- **Docker support**: Full containerization with docker-compose
- **Environment-driven**: All configuration via environment variables
- **Multilingual**: Auto-detection for question generation

### Supported LLM Vendors

| Vendor | Models | Optimization Strategy |
|--------|--------|----------------------|
| OpenAI | GPT-4o, o1, o3-mini, o4-mini | Structured instructions, few-shot learning, chain-of-thought |
| Claude | 3.7 Sonnet, 3.5 Haiku | XML tags, thinking blocks, document structure |
| Grok | Grok 4, Grok 4 Fast, Code Fast 1 | Conversational tone, real-time context |
| Gemini | 2.5 Pro, 2.5 Flash | Multi-step reasoning, structured formats, long-context |
| Qwen | Qwen3-235B, Qwen3-30B, QwQ-32B | Multilingual, mathematical reasoning, technical precision |
| DeepSeek | V3.2-Exp, R1-0528 | Code generation, system design, technical documentation |

### Architecture

```
┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│   React UI   │────▶│   FastAPI   │────▶│  LM Studio   │
│   (Port 3000)│     │  (Port 8000)│     │   (Local)    │
└──────────────┘     └──────┬──────┘     └──────────────┘
                            │
                     ┌──────▼──────┐
                     │  Telegram   │
                     │     Bot     │
                     └─────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
   ┌──────▼──────┐   ┌──────▼──────┐  ┌──────▼──────┐
   │  PostgreSQL │   │    Redis    │  │   Vendor    │
   │             │   │    Cache    │  │   Adapters  │
   └─────────────┘   └─────────────┘  └─────────────┘
```

### Prerequisites

- Docker & Docker Compose
- LM Studio running at `http://127.0.0.1:1234` ([download](https://lmstudio.ai/))
- Any local model loaded in LM Studio (e.g., Qwen 2.5, Llama 3, Mistral)
- (Optional) Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### Quick Start

```bash
# Clone repository
git clone https://github.com/rldyourmnd/local-llm-prompt-optimizer.git
cd local-llm-prompt-optimizer

# Configure environment
cp .env.example .env
# Edit .env with your LM Studio URL and optional Telegram Bot Token

# Start services
docker-compose --profile with-bot up -d --build

# Access
# Web UI: http://localhost:3000
# API Docs: http://localhost:8000/docs
# Health Check: http://localhost:8000/health
```

### Configuration

All settings via `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `LM_STUDIO_BASE_URL` | LM Studio API endpoint | `http://host.docker.internal:1234/v1` |
| `LM_STUDIO_MODEL` | Model name (empty for auto-detection) | - |
| `LM_STUDIO_MAX_TOKENS` | Maximum tokens per request | `2048` |
| `LM_STUDIO_TEMPERATURE` | Generation temperature | `0.7` |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token (optional) | - |
| `TELEGRAM_ALLOWED_USER_IDS` | Comma-separated user IDs for access control | - |
| `DATABASE_URL` | PostgreSQL connection string | Auto-configured |
| `REDIS_URL` | Redis connection string | Auto-configured |
| `APP_PORT` | Backend API port | `8000` |
| `FRONTEND_PORT` | Frontend UI port | `3000` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000,http://localhost:5173` |
| `LOG_LEVEL` | Logging level | `INFO` |

See [`.env.example`](.env.example) for complete configuration reference.

### Usage

#### Web Interface

1. Navigate to http://localhost:3000
2. Enter prompt text
3. Select target LLM vendor
4. (Optional) Enable Think Mode (5/10/25 questions)
5. Submit and copy optimized result

#### REST API

**Quick optimization:**
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a function to calculate fibonacci",
    "vendor": "openai"
  }'
```

**Think Mode - Generate questions:**
```bash
curl -X POST http://localhost:8000/api/think/generate-questions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "vendor": "claude",
    "num_questions": 5
  }'
```

**Think Mode - Optimize with answers:**
```bash
curl -X POST http://localhost:8000/api/think/optimize-with-answers \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "vendor": "claude",
    "questions": ["What is your knowledge level?"],
    "answers": ["Beginner"]
  }'
```

#### Telegram Bot

```
/start - Initialize bot
/help - Show help message

Send any text prompt → Choose vendor → (Optional) Choose Think Mode → Receive optimized prompt
```

### Development

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

#### Telegram Bot

```bash
cd telegram-bot
pip install -r requirements.txt
python src/bot.py
```

#### Testing

```bash
cd backend
pytest
pytest -v  # Verbose output
pytest tests/test_health.py  # Specific test
```

### Docker Commands

```bash
# Build all services
docker-compose --profile with-bot build

# Start all services
docker-compose --profile with-bot up -d

# Start without Telegram bot
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f telegram-bot

# Stop all services
docker-compose down

# Clean up (including volumes)
docker-compose down -v
```

### Project Structure

```
local-llm-prompt-optimizer/
├── backend/
│   ├── src/
│   │   ├── api/                  # API routes and schemas
│   │   ├── application/          # Business logic and services
│   │   ├── domain/               # Domain models and interfaces
│   │   └── infrastructure/       # LM Studio client, database, config
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/                      # React + TypeScript components
│   ├── public/                   # Static assets
│   └── package.json
├── telegram-bot/
│   ├── src/
│   │   └── bot.py
│   └── requirements.txt
├── docs/
│   ├── API_USAGE.md             # API reference
│   └── DEVELOPMENT.md           # Development guide
├── .env.example
├── docker-compose.yml
├── CLAUDE.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── README.md
```

### Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Commit message format:** Conventional Commits
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `test:` test additions or modifications
- `refactor:` code refactoring
- `chore:` maintenance tasks

### License

MIT License. See [LICENSE](LICENSE) for details.

**Copyright (c) 2025 NDDev OpenNetwork. Danil Silantyev**

### Security

Report security vulnerabilities to business@nddev.tech

See [SECURITY.md](SECURITY.md) for complete security policy.

### Commercial Support

NDDev OpenNetwork provides:
- Enterprise deployment and customization
- Custom vendor integrations
- Technical consulting and training
- Feature development and prioritization
- Extended support agreements

**Contact:** business@nddev.tech | https://nddev.tech

### Community

- Telegram: [@DevsOpenNetwork](https://t.me/DevsOpenNetwork)
- GitHub: [github.com/rldyourmnd](https://github.com/rldyourmnd)
- Website: [nddev.tech](https://nddev.tech)

### Author

**Danil Silantyev**
- GitHub: [@rldyourmnd](https://github.com/rldyourmnd)
- Telegram: [@Danil_Silantyev](https://t.me/Danil_Silantyev)
- Company: NDDev OpenNetwork

---

## Russian

### Обзор

Local LLM Prompt Optimizer — инструмент для оптимизации промптов для различных LLM-провайдеров с использованием локальной AI-обработки. Все вычисления выполняются через LM Studio на вашей машине без внешних API-запросов и передачи данных.

**Лицензия:** MIT
**Версия:** 1.0.0
**Язык:** Python 3.11+, TypeScript
**Архитектура:** Domain-Driven Design с микросервисами

### Возможности

- **Локальная обработка**: Все AI-операции через LM Studio
- **Поддержка нескольких провайдеров**: OpenAI, Claude, Grok, Gemini, Qwen, DeepSeek
- **Режим Think**: AI-генерация уточняющих вопросов для точной оптимизации
- **Множество интерфейсов**: Веб-UI, REST API, Telegram-бот
- **Чистая архитектура**: Принципы DDD с адаптерами провайдеров
- **Поддержка Docker**: Полная контейнеризация с docker-compose
- **Управление через окружение**: Вся конфигурация через переменные окружения
- **Мультиязычность**: Автоопределение языка для генерации вопросов

### Поддерживаемые LLM-провайдеры

| Провайдер | Модели | Стратегия оптимизации |
|-----------|--------|-----------------------|
| OpenAI | GPT-4o, o1, o3-mini, o4-mini | Структурированные инструкции, few-shot обучение, chain-of-thought |
| Claude | 3.7 Sonnet, 3.5 Haiku | XML-теги, блоки мышления, структура документов |
| Grok | Grok 4, Grok 4 Fast, Code Fast 1 | Разговорный тон, real-time контекст |
| Gemini | 2.5 Pro, 2.5 Flash | Многошаговое рассуждение, структурированные форматы, длинный контекст |
| Qwen | Qwen3-235B, Qwen3-30B, QwQ-32B | Мультиязычность, математическое рассуждение, техническая точность |
| DeepSeek | V3.2-Exp, R1-0528 | Генерация кода, системный дизайн, техническая документация |

### Архитектура

```
┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│   React UI   │────▶│   FastAPI   │────▶│  LM Studio   │
│   (Порт 3000)│     │  (Порт 8000)│     │  (Локально)  │
└──────────────┘     └──────┬──────┘     └──────────────┘
                            │
                     ┌──────▼──────┐
                     │  Telegram   │
                     │     Bot     │
                     └─────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
   ┌──────▼──────┐   ┌──────▼──────┐  ┌──────▼──────┐
   │  PostgreSQL │   │    Redis    │  │   Адаптеры  │
   │             │   │     Кэш     │  │  провайдеров│
   └─────────────┘   └─────────────┘  └─────────────┘
```

### Требования

- Docker & Docker Compose
- LM Studio работает на `http://127.0.0.1:1234` ([скачать](https://lmstudio.ai/))
- Любая локальная модель загружена в LM Studio (например, Qwen 2.5, Llama 3, Mistral)
- (Опционально) Telegram Bot Token от [@BotFather](https://t.me/BotFather)

### Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/rldyourmnd/local-llm-prompt-optimizer.git
cd local-llm-prompt-optimizer

# Настроить окружение
cp .env.example .env
# Отредактировать .env (указать URL LM Studio и опционально токен Telegram-бота)

# Запустить сервисы
docker-compose --profile with-bot up -d --build

# Доступ
# Веб-UI: http://localhost:3000
# API документация: http://localhost:8000/docs
# Health Check: http://localhost:8000/health
```

### Конфигурация

Все настройки через файл `.env`:

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `LM_STUDIO_BASE_URL` | Endpoint LM Studio API | `http://host.docker.internal:1234/v1` |
| `LM_STUDIO_MODEL` | Название модели (пусто для автоопределения) | - |
| `LM_STUDIO_MAX_TOKENS` | Максимум токенов на запрос | `2048` |
| `LM_STUDIO_TEMPERATURE` | Температура генерации | `0.7` |
| `TELEGRAM_BOT_TOKEN` | Токен Telegram-бота (опционально) | - |
| `TELEGRAM_ALLOWED_USER_IDS` | ID пользователей через запятую для контроля доступа | - |
| `DATABASE_URL` | Строка подключения PostgreSQL | Автонастройка |
| `REDIS_URL` | Строка подключения Redis | Автонастройка |
| `APP_PORT` | Порт backend API | `8000` |
| `FRONTEND_PORT` | Порт frontend UI | `3000` |
| `CORS_ORIGINS` | Разрешённые CORS origins | `http://localhost:3000,http://localhost:5173` |
| `LOG_LEVEL` | Уровень логирования | `INFO` |

См. [`.env.example`](.env.example) для полного справочника конфигурации.

### Использование

#### Веб-интерфейс

1. Перейти на http://localhost:3000
2. Ввести текст промпта
3. Выбрать целевой LLM-провайдер
4. (Опционально) Включить режим Think (5/10/25 вопросов)
5. Отправить и скопировать оптимизированный результат

#### REST API

**Быстрая оптимизация:**
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Напиши функцию для вычисления чисел Фибоначчи",
    "vendor": "openai"
  }'
```

**Режим Think - Генерация вопросов:**
```bash
curl -X POST http://localhost:8000/api/think/generate-questions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Объясни квантовые вычисления",
    "vendor": "claude",
    "num_questions": 5
  }'
```

**Режим Think - Оптимизация с ответами:**
```bash
curl -X POST http://localhost:8000/api/think/optimize-with-answers \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Объясни квантовые вычисления",
    "vendor": "claude",
    "questions": ["Какой у вас уровень знаний?"],
    "answers": ["Начальный"]
  }'
```

#### Telegram-бот

```
/start - Инициализировать бота
/help - Показать справку

Отправить текстовый промпт → Выбрать провайдера → (Опционально) Выбрать режим Think → Получить оптимизированный промпт
```

### Разработка

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

#### Telegram-бот

```bash
cd telegram-bot
pip install -r requirements.txt
python src/bot.py
```

#### Тестирование

```bash
cd backend
pytest
pytest -v  # Подробный вывод
pytest tests/test_health.py  # Конкретный тест
```

### Docker команды

```bash
# Собрать все сервисы
docker-compose --profile with-bot build

# Запустить все сервисы
docker-compose --profile with-bot up -d

# Запустить без Telegram-бота
docker-compose up -d

# Просмотр логов
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f telegram-bot

# Остановить все сервисы
docker-compose down

# Очистка (включая volumes)
docker-compose down -v
```

### Структура проекта

```
local-llm-prompt-optimizer/
├── backend/
│   ├── src/
│   │   ├── api/                  # API роуты и схемы
│   │   ├── application/          # Бизнес-логика и сервисы
│   │   ├── domain/               # Модели и интерфейсы домена
│   │   └── infrastructure/       # Клиент LM Studio, база данных, конфиг
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/                      # React + TypeScript компоненты
│   ├── public/                   # Статические ресурсы
│   └── package.json
├── telegram-bot/
│   ├── src/
│   │   └── bot.py
│   └── requirements.txt
├── docs/
│   ├── API_USAGE.md             # Справочник API
│   └── DEVELOPMENT.md           # Руководство разработчика
├── .env.example
├── docker-compose.yml
├── CLAUDE.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── README.md
```

### Участие в проекте

Вклад приветствуется. См. [CONTRIBUTING.md](CONTRIBUTING.md) для руководства.

**Формат commit-сообщений:** Conventional Commits
- `feat:` новые функции
- `fix:` исправления ошибок
- `docs:` изменения документации
- `test:` добавление или изменение тестов
- `refactor:` рефакторинг кода
- `chore:` задачи обслуживания

### Лицензия

MIT License. См. [LICENSE](LICENSE) для деталей.

**Copyright (c) 2025 NDDev OpenNetwork. Danil Silantyev**

### Безопасность

Сообщения об уязвимостях отправлять на business@nddev.tech

См. [SECURITY.md](SECURITY.md) для полной политики безопасности.

### Коммерческая поддержка

NDDev OpenNetwork предоставляет:
- Enterprise развёртывание и кастомизация
- Интеграции с кастомными провайдерами
- Техническое консультирование и обучение
- Разработка функций и приоритизация
- Расширенные соглашения о поддержке

**Контакты:** business@nddev.tech | https://nddev.tech

### Сообщество

- Telegram: [@DevsOpenNetwork](https://t.me/DevsOpenNetwork)
- GitHub: [github.com/rldyourmnd](https://github.com/rldyourmnd)
- Сайт: [nddev.tech](https://nddev.tech)

### Автор

**Danil Silantyev**
- GitHub: [@rldyourmnd](https://github.com/rldyourmnd)
- Telegram: [@Danil_Silantyev](https://t.me/Danil_Silantyev)
- Компания: NDDev OpenNetwork
