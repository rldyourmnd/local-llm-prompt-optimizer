# Contributing to Local LLM Prompt Optimizer

**[English](#english)** | **[Русский](#русский)**

---

## English

Thank you for your interest in contributing to **Local LLM Prompt Optimizer**!

We welcome contributions from the community and are grateful for any help—whether it's reporting bugs, suggesting features, improving documentation, or submitting code.

### How to Contribute

#### 1. Report Bugs

If you find a bug, please open an issue on GitHub with:

- **Clear title** describing the problem
- **Steps to reproduce** the bug
- **Expected vs actual behavior**
- **Environment details** (OS, Docker version, Python version, etc.)
- **Logs** if applicable

#### 2. Suggest Features

We love new ideas! Open an issue with:

- **Clear description** of the feature
- **Use case** explaining why it's needed
- **Proposed implementation** (if you have ideas)

#### 3. Improve Documentation

Documentation is crucial! You can:

- Fix typos or unclear explanations
- Add examples or tutorials
- Translate documentation
- Improve code comments

#### 4. Submit Code

**Before starting major work, please open an issue to discuss your approach.**

### Development Workflow

#### Fork & Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/local-llm-prompt-optimizer.git
cd local-llm-prompt-optimizer
git remote add upstream https://github.com/rldyourmnd/local-llm-prompt-optimizer.git
```

#### Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

#### Make Changes

- Follow existing code style (see [Code Style](#code-style) below)
- Write clear, concise commit messages (see [Commit Messages](#commit-messages))
- Add tests for new features
- Update documentation if needed

#### Test Your Changes

```bash
# Backend tests
cd backend
pytest

# Frontend
cd frontend
npm run lint
npm run build

# Docker
docker-compose --profile with-bot build
docker-compose --profile with-bot up -d
# Test manually
```

#### Push & Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:

- **Clear title** summarizing the change
- **Description** explaining what and why
- **Reference to related issues** (e.g., "Fixes #123")
- **Screenshots** if UI changes

### Commit Messages

We use **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, no logic change)
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `test:` Adding or updating tests
- `chore:` Maintenance tasks (dependencies, build, etc.)

**Examples:**
```
feat(backend): add Think Mode question generation API

fix(telegram-bot): resolve handler priority issue for Think Mode

docs(readme): update vendor models to October 2025 versions

chore(deps): bump fastapi from 0.104 to 0.105
```

### Code Style

#### Python

- Follow **PEP 8**
- Use **Black** for formatting:
  ```bash
  black src/
  ```
- Use **type hints** where applicable
- Maximum line length: **100 characters**
- Write docstrings for functions and classes

#### TypeScript/JavaScript

- Follow **Airbnb Style Guide**
- Use **Prettier** for formatting
- Use **ESLint** for linting
- Prefer `const` over `let`
- Use arrow functions for callbacks

#### General

- **No hardcoded values** - use environment variables
- **Clear variable names** - avoid abbreviations
- **Comments** for complex logic
- **Keep functions small** - single responsibility

### Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages follow Conventional Commits
- [ ] No merge conflicts with `main`
- [ ] PR description is clear and complete

### Architecture Guidelines

- **Backend**: Follow Domain-Driven Design (DDD) principles
  - `domain/` - Core business logic, models, interfaces
  - `application/` - Use cases, services
  - `infrastructure/` - External dependencies (DB, LM Studio, etc.)
  - `api/` - HTTP routes, schemas, DTOs

- **Frontend**: Component-based architecture
  - Keep components small and focused
  - Use hooks for state management
  - Separate business logic from presentation

- **Telegram Bot**: Event-driven architecture
  - Use handlers for different update types
  - Keep conversation state in `context.user_data`
  - Isolate per-user state with `per_chat=True, per_user=True`

### Testing Guidelines

- **Write tests** for new features and bug fixes
- **Unit tests** for business logic
- **Integration tests** for API endpoints
- **E2E tests** for critical user flows

#### Backend Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_optimization_service.py

# Run with coverage
pytest --cov=src tests/
```

### Internationalization

- **README.md** must have EN/RU sections
- **Other documentation** should have EN/RU if possible
- **UI messages** should support multiple languages
- **Error messages** should be clear in English

### Commercial Contributions

If your contribution is for commercial use or you need custom development:

- Contact: [business@nddev.tech](mailto:business@nddev.tech)
- We offer:
  - Custom integrations
  - Feature prioritization
  - Enterprise support
  - Training and consulting

### Communication

- **Issues** - Bug reports and feature requests
- **Pull Requests** - Code contributions
- **Telegram** - [@DevsOpenNetwork](https://t.me/DevsOpenNetwork) for community discussion
- **Email** - [business@nddev.tech](mailto:business@nddev.tech) for commercial inquiries

### License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

<div align="center">

**Thank you for contributing to Local LLM Prompt Optimizer!**

Built by NDDev OpenNetwork

</div>

---

## Русский

Спасибо за ваш интерес к проекту **Local LLM Prompt Optimizer**!

Мы приветствуем вклад сообщества и благодарны за любую помощь — будь то сообщения об ошибках, предложения функций, улучшение документации или отправка кода.

### Как внести вклад

#### 1. Сообщить об ошибке

Если вы нашли ошибку, откройте issue на GitHub с:

- **Чётким заголовком**, описывающим проблему
- **Шагами для воспроизведения** ошибки
- **Ожидаемым и фактическим поведением**
- **Деталями окружения** (ОС, версия Docker, Python и т.д.)
- **Логами** при наличии

#### 2. Предложить функцию

Мы любим новые идеи! Откройте issue с:

- **Чётким описанием** функции
- **Примером использования**, объясняющим зачем она нужна
- **Предлагаемой реализацией** (если есть идеи)

#### 3. Улучшить документацию

Документация критически важна! Вы можете:

- Исправить опечатки или неясные объяснения
- Добавить примеры или туториалы
- Перевести документацию
- Улучшить комментарии в коде

#### 4. Отправить код

**Перед началом крупной работы откройте issue для обсуждения подхода.**

### Процесс разработки

#### Fork & Clone

```bash
# Сделайте fork репозитория на GitHub, затем:
git clone https://github.com/YOUR_USERNAME/local-llm-prompt-optimizer.git
cd local-llm-prompt-optimizer
git remote add upstream https://github.com/rldyourmnd/local-llm-prompt-optimizer.git
```

#### Создать ветку

```bash
git checkout -b feature/your-feature-name
# или
git checkout -b fix/your-bug-fix
```

#### Внести изменения

- Следуйте существующему стилю кода (см. [Стиль кода](#стиль-кода) ниже)
- Пишите чёткие, лаконичные commit messages (см. [Commit Messages](#commit-messages))
- Добавляйте тесты для новых функций
- Обновляйте документацию при необходимости

#### Тестировать изменения

```bash
# Тесты backend
cd backend
pytest

# Frontend
cd frontend
npm run lint
npm run build

# Docker
docker-compose --profile with-bot build
docker-compose --profile with-bot up -d
# Ручное тестирование
```

#### Push & Создать Pull Request

```bash
git push origin feature/your-feature-name
```

Затем откройте Pull Request на GitHub с:

- **Чётким заголовком**, резюмирующим изменение
- **Описанием**, объясняющим что и почему
- **Ссылкой на связанные issues** (например, "Fixes #123")
- **Скриншотами** при изменениях UI

### Commit Messages

Мы используем формат **Conventional Commits**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Типы:**
- `feat:` Новая функция
- `fix:` Исправление ошибки
- `docs:` Изменения документации
- `style:` Изменения стиля кода (форматирование, без изменения логики)
- `refactor:` Рефакторинг кода
- `perf:` Улучшения производительности
- `test:` Добавление или обновление тестов
- `chore:` Задачи обслуживания (зависимости, сборка и т.д.)

**Примеры:**
```
feat(backend): добавлен API генерации вопросов Think Mode

fix(telegram-bot): исправлен приоритет обработчиков для Think Mode

docs(readme): обновлены модели вендоров до версий октября 2025

chore(deps): обновлён fastapi с 0.104 до 0.105
```

### Чек-лист Pull Request

Перед отправкой PR убедитесь:

- [ ] Код соответствует стилю проекта
- [ ] Все тесты проходят
- [ ] Новые функции покрыты тестами
- [ ] Документация обновлена
- [ ] Commit messages следуют Conventional Commits
- [ ] Нет конфликтов с `main`
- [ ] Описание PR чёткое и полное

### Лицензия

Внося вклад, вы соглашаетесь, что ваши материалы будут лицензированы под MIT License.

---

<div align="center">

**Спасибо за вклад в Local LLM Prompt Optimizer!**

Сделано командой NDDev OpenNetwork

</div>
