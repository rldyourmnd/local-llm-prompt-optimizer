# Security Policy

**[English](#english)** | **[Русский](#русский)**

---

## English

### 🔒 Security Commitment

At **NDDev OpenNetwork**, we take security seriously. **Local LLM Prompt Optimizer** is designed with privacy and security in mind:

- **100% Local Processing** - All LLM operations run locally via LM Studio
- **No External API Calls** - Your prompts never leave your machine
- **No Telemetry** - Zero tracking or analytics by default
- **Open Source** - Full transparency, auditable code

### 🐛 Reporting a Vulnerability

**Please DO NOT report security vulnerabilities through public GitHub issues.**

#### Private Reporting

To report a security vulnerability, please email:

**📧 [business@nddev.tech](mailto:business@nddev.tech)**

Include the following information:

1. **Type of vulnerability** (e.g., SQL injection, XSS, authentication bypass)
2. **Affected components** (backend, frontend, Telegram bot)
3. **Steps to reproduce** the vulnerability
4. **Potential impact** of the vulnerability
5. **Suggested fix** (if you have one)
6. **Your contact information** for follow-up

#### Response Timeline

- **Acknowledgment**: Within 72 hours
- **Initial Assessment**: Within 1 week
- **Fix & Disclosure**: Depends on severity (see below)

### 🎯 Severity Levels

| Severity | Description | Response Time |
|----------|-------------|---------------|
| **Critical** | Remote code execution, data breach | 24-48 hours |
| **High** | Authentication bypass, privilege escalation | 3-7 days |
| **Medium** | XSS, CSRF, information disclosure | 1-2 weeks |
| **Low** | Minor issues with limited impact | 2-4 weeks |

### 🛡️ Security Best Practices

#### For Users

1. **Keep Software Updated**
   - Regularly update Docker images
   - Update LM Studio to latest version
   - Monitor security advisories

2. **Environment Variables**
   - **Never commit** `.env` files to version control
   - Use strong, unique tokens for Telegram bot
   - Restrict `TELEGRAM_ALLOWED_USER_IDS` appropriately

3. **Network Security**
   - Run behind firewall if exposing to network
   - Use HTTPS for production deployments
   - Limit database access to localhost

4. **Docker Security**
   - Don't run containers as root
   - Use Docker secrets for sensitive data
   - Regularly scan images for vulnerabilities

#### For Developers

1. **Input Validation**
   - Sanitize all user inputs
   - Use Pydantic for schema validation
   - Prevent SQL injection with parameterized queries

2. **Authentication & Authorization**
   - Implement proper access control
   - Use secure session management
   - Validate Telegram user IDs

3. **Dependency Management**
   - Regularly update dependencies
   - Use `pip-audit` for Python
   - Use `npm audit` for Node.js

4. **Code Review**
   - All PRs require review
   - Security-focused code reviews for critical components
   - Automated security scanning in CI/CD

### 🔐 Secure Configuration

#### Recommended `.env` Settings

```env
# Strong tokens (example - use your own!)
TELEGRAM_BOT_TOKEN=your_secure_token_here

# Restrict user access
TELEGRAM_ALLOWED_USER_IDS=123456789,987654321

# Database security
DATABASE_URL=postgresql://user:strong_password@localhost:5432/dbname

# Disable debug in production
DEBUG=False

# Use secure cookies
SECURE_COOKIES=True
SAMESITE_COOKIES=strict
```

#### Docker Production Setup

```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - DEBUG=False
      - SECURE_COOKIES=True
    secrets:
      - telegram_token
      - db_password
```

### 📦 Supported Versions

| Version | Supported | End of Support |
|---------|-----------|----------------|
| main (latest) | ✅ Yes | Active development |
| 1.x.x | ✅ Yes | 6 months after next major release |
| < 1.0.0 | ❌ No | Unsupported |

### 🏆 Security Acknowledgments

We appreciate the security research community! If you report a valid security issue, we will:

- Credit you in our security advisories (if desired)
- Mention you in release notes
- Provide a thank-you message in our README

**Hall of Fame** (Security Researchers who helped us):

*None yet - be the first!*

### 📜 Disclosure Policy

1. **Private Disclosure**: Report sent to business@nddev.tech
2. **Acknowledgment**: We confirm receipt within 72 hours
3. **Investigation**: We assess severity and impact
4. **Fix Development**: We develop and test a fix
5. **Public Disclosure**: Coordinated disclosure after fix is released
6. **Credit**: We publicly thank the reporter (if desired)

### 🔗 Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

### 💼 Commercial Security Services

For enterprise security needs:

- Security audits
- Penetration testing
- Compliance consulting (GDPR, SOC 2, etc.)
- Custom security features

Contact: [business@nddev.tech](mailto:business@nddev.tech)

---

<div align="center">

**Security is a shared responsibility. Thank you for helping keep our community safe!**

NDDev OpenNetwork | [nddev.tech](https://nddev.tech)

</div>

---

## Русский

### 🔒 Приверженность безопасности

В **NDDev OpenNetwork** мы серьёзно относимся к безопасности. **Local LLM Prompt Optimizer** разработан с учётом приватности и безопасности:

- **100% Локальная обработка** - Все LLM операции выполняются локально через LM Studio
- **Никаких внешних API вызовов** - Ваши промпты не покидают ваш компьютер
- **Нет телеметрии** - Никакого отслеживания или аналитики по умолчанию
- **Open Source** - Полная прозрачность, аудируемый код

### 🐛 Сообщение об уязвимости

**Пожалуйста, НЕ сообщайте об уязвимостях через публичные GitHub issues.**

#### Приватное сообщение

Для сообщения об уязвимости, пожалуйста, напишите на email:

**📧 [business@nddev.tech](mailto:business@nddev.tech)**

Включите следующую информацию:

1. **Тип уязвимости** (например, SQL injection, XSS, обход аутентификации)
2. **Затронутые компоненты** (backend, frontend, Telegram бот)
3. **Шаги для воспроизведения** уязвимости
4. **Потенциальное влияние** уязвимости
5. **Предлагаемое исправление** (если есть)
6. **Ваши контактные данные** для обратной связи

#### Сроки ответа

- **Подтверждение**: В течение 72 часов
- **Первоначальная оценка**: В течение 1 недели
- **Исправление и раскрытие**: Зависит от серьёзности (см. ниже)

### 🎯 Уровни серьёзности

| Серьёзность | Описание | Время ответа |
|-------------|----------|--------------|
| **Критическая** | Удалённое выполнение кода, утечка данных | 24-48 часов |
| **Высокая** | Обход аутентификации, повышение привилегий | 3-7 дней |
| **Средняя** | XSS, CSRF, раскрытие информации | 1-2 недели |
| **Низкая** | Незначительные проблемы с ограниченным влиянием | 2-4 недели |

### 🛡️ Лучшие практики безопасности

#### Для пользователей

1. **Обновляйте ПО**
   - Регулярно обновляйте Docker образы
   - Обновляйте LM Studio до последней версии
   - Следите за security advisories

2. **Переменные окружения**
   - **Никогда не коммитьте** файлы `.env` в систему контроля версий
   - Используйте сильные, уникальные токены для Telegram бота
   - Ограничивайте `TELEGRAM_ALLOWED_USER_IDS` соответственно

3. **Сетевая безопасность**
   - Используйте firewall при раскрытии в сеть
   - Используйте HTTPS для production развертываний
   - Ограничьте доступ к БД до localhost

4. **Безопасность Docker**
   - Не запускайте контейнеры как root
   - Используйте Docker secrets для чувствительных данных
   - Регулярно сканируйте образы на уязвимости

### 📜 Политика раскрытия

1. **Приватное раскрытие**: Отчёт отправлен на business@nddev.tech
2. **Подтверждение**: Мы подтверждаем получение в течение 72 часов
3. **Расследование**: Мы оцениваем серьёзность и влияние
4. **Разработка исправления**: Мы разрабатываем и тестируем исправление
5. **Публичное раскрытие**: Координированное раскрытие после выпуска исправления
6. **Благодарность**: Мы публично благодарим исследователя (если желает)

### 💼 Коммерческие услуги безопасности

Для enterprise потребностей безопасности:

- Аудиты безопасности
- Тестирование на проникновение
- Консалтинг по соответствию (GDPR, SOC 2 и т.д.)
- Кастомные функции безопасности

Контакт: [business@nddev.tech](mailto:business@nddev.tech)

---

<div align="center">

**Безопасность — это общая ответственность. Спасибо за помощь в защите нашего сообщества!**

NDDev OpenNetwork | [nddev.tech](https://nddev.tech)

</div>
