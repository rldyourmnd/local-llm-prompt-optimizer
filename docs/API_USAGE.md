# API Usage Guide

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required (local-first design). For production deployments, implement authentication middleware.

## Endpoints

### Health Check

**GET** `/health`

Check service health and LM Studio availability.

**Response**
```json
{
  "status": "healthy",
  "lm_studio_available": true,
  "vendor_adapters": 6
}
```

**cURL Example**
```bash
curl http://localhost:8000/health
```

---

### Optimize Prompt

**POST** `/api/optimize`

Optimize a prompt for a specific LLM vendor.

**Request Body**
```json
{
  "prompt": "Write a function to calculate fibonacci numbers",
  "vendor": "openai",
  "context": "This is for a Python tutorial",
  "max_length": 1000
}
```

**Parameters**
- `prompt` (string, required) - The original prompt to optimize
- `vendor` (string, required) - Target vendor: `openai`, `claude`, `grok`, `gemini`, `qwen`, or `deepseek`
- `context` (string, optional) - Additional context for optimization
- `max_length` (integer, optional) - Maximum length constraint

**Response**
```json
{
  "original": "Write a function to calculate fibonacci numbers",
  "optimized": "Create a Python function that efficiently calculates...",
  "vendor": "openai",
  "enhancement_notes": "Enhanced for OpenAI: added role definition...",
  "metadata": {
    "vendor": "openai",
    "format": "markdown",
    "temperature_recommendation": "0.2 for precise tasks",
    "model_recommendation": "gpt-4-turbo for complex tasks"
  }
}
```

**cURL Examples**

OpenAI Optimization:
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "vendor": "openai"
  }'
```

Claude with Context:
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analyze this data",
    "vendor": "claude",
    "context": "Financial quarterly report data"
  }'
```

---

## Vendor-Specific Features

### OpenAI
**Best For**: General tasks, code, few-shot learning
**Format**: Markdown with structured sections
**Enhancements**:
- Role-based prompting
- Clear task decomposition
- Output format specification
- Step-by-step reasoning

**Example**
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a REST API endpoint",
    "vendor": "openai",
    "context": "Using FastAPI framework"
  }'
```

### Claude (Anthropic)
**Best For**: Long documents, complex reasoning, analysis
**Format**: XML tags structure
**Enhancements**:
- `<task>`, `<context>`, `<instructions>` tags
- Thinking blocks for reasoning
- Document organization
- Multi-shot examples

**Example**
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review this code for security issues",
    "vendor": "claude",
    "context": "Production payment processing system"
  }'
```

### Grok (xAI)
**Best For**: Current events, conversational tasks
**Format**: Conversational, engaging
**Enhancements**:
- Real-time context awareness
- Internet culture references
- Direct, witty tone
- Current information emphasis

**Example**
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain latest AI developments",
    "vendor": "grok"
  }'
```

### Gemini (Google)
**Best For**: Multi-modal, long-context, structured data
**Format**: Structured with clear sections
**Enhancements**:
- Multi-step reasoning
- Task decomposition
- Quality standards
- Comprehensive specifications

**Example**
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a data pipeline",
    "vendor": "gemini",
    "context": "Processing 1M+ records daily"
  }'
```

### Qwen (Alibaba)
**Best For**: Multilingual, math, reasoning
**Format**: Structured reasoning with methodology
**Enhancements**:
- System role definition
- Step-by-step methodology
- Multilingual support
- Technical precision

**Example**
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Solve optimization problem",
    "vendor": "qwen",
    "context": "Linear programming with constraints"
  }'
```

### DeepSeek
**Best For**: Code generation, system design, debugging
**Format**: Technical structured
**Enhancements**:
- Technical specifications
- Implementation approach
- Code quality focus
- Testing and validation

**Example**
```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Design a caching layer",
    "vendor": "deepseek",
    "context": "High-traffic web application"
  }'
```

---

## Python Client Example

```python
import requests

API_URL = "http://localhost:8000"

def optimize_prompt(prompt: str, vendor: str, context: str = None):
    """Optimize a prompt for a specific vendor."""
    response = requests.post(
        f"{API_URL}/api/optimize",
        json={
            "prompt": prompt,
            "vendor": vendor,
            "context": context
        },
        timeout=120
    )
    response.raise_for_status()
    return response.json()

# Example usage
result = optimize_prompt(
    prompt="Create a user authentication system",
    vendor="openai",
    context="Using JWT tokens and PostgreSQL"
)

print(f"Original: {result['original']}")
print(f"Optimized: {result['optimized']}")
print(f"Notes: {result['enhancement_notes']}")
print(f"Recommended temp: {result['metadata']['temperature_recommendation']}")
```

## JavaScript/TypeScript Client Example

```typescript
interface OptimizationRequest {
  prompt: string
  vendor: string
  context?: string
  max_length?: number
}

interface OptimizationResult {
  original: string
  optimized: string
  vendor: string
  enhancement_notes: string
  metadata: {
    vendor: string
    format: string
    temperature_recommendation?: string
    model_recommendation?: string
  }
}

async function optimizePrompt(
  request: OptimizationRequest
): Promise<OptimizationResult> {
  const response = await fetch('http://localhost:8000/api/optimize', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  })

  if (!response.ok) {
    throw new Error(`Optimization failed: ${response.statusText}`)
  }

  return response.json()
}

// Example usage
const result = await optimizePrompt({
  prompt: 'Build a recommendation engine',
  vendor: 'gemini',
  context: 'E-commerce platform with 100k products',
})

console.log('Optimized:', result.optimized)
console.log('Format:', result.metadata.format)
```

## Error Handling

### Validation Errors (422)

```json
{
  "detail": [
    {
      "loc": ["body", "vendor"],
      "msg": "value is not a valid enumeration member",
      "type": "type_error.enum"
    }
  ]
}
```

### Service Errors (500)

```json
{
  "detail": "Optimization failed: LM Studio connection timeout"
}
```

### Example Error Handling

```python
import requests

try:
    response = requests.post(
        "http://localhost:8000/api/optimize",
        json={"prompt": "Test", "vendor": "openai"},
        timeout=120
    )
    response.raise_for_status()
    result = response.json()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 422:
        print(f"Validation error: {e.response.json()}")
    elif e.response.status_code == 500:
        print(f"Server error: {e.response.json()['detail']}")
except requests.exceptions.Timeout:
    print("Request timeout - LM Studio may be slow or unavailable")
except requests.exceptions.ConnectionError:
    print("Connection error - is the service running?")
```

## Rate Limiting

Currently no rate limiting implemented (local-first). For production deployments, consider adding rate limiting middleware.

## CORS Configuration

CORS is configured via `CORS_ORIGINS` environment variable. Default:
```
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## API Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Best Practices

1. **Timeouts**: Set appropriate timeouts (120s recommended)
2. **Error Handling**: Always handle connection and HTTP errors
3. **Vendor Selection**: Choose vendor based on task type
4. **Context**: Provide relevant context for better optimization
5. **Validation**: Validate prompts client-side before sending
6. **Monitoring**: Monitor LM Studio availability via `/health` endpoint
