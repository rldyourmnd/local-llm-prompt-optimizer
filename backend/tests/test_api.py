"""API endpoint integration tests."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_optimize_endpoint_success(async_client: AsyncClient):
    """Test successful optimization request."""
    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": "Write a function",
            "vendor": "openai"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "original" in data
    assert "optimized" in data
    assert "vendor" in data
    assert "enhancement_notes" in data
    assert "metadata" in data
    assert data["vendor"] == "openai"


@pytest.mark.asyncio
async def test_optimize_endpoint_with_context(async_client: AsyncClient):
    """Test optimization with additional context."""
    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": "Write a function",
            "vendor": "claude",
            "context": "For beginners"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["vendor"] == "claude"


@pytest.mark.asyncio
async def test_optimize_endpoint_invalid_vendor(async_client: AsyncClient):
    """Test optimization with invalid vendor."""
    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": "Write a function",
            "vendor": "invalid_vendor"
        }
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_optimize_endpoint_missing_prompt(async_client: AsyncClient):
    """Test optimization without prompt."""
    response = await async_client.post(
        "/api/optimize",
        json={
            "vendor": "openai"
        }
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_optimize_endpoint_empty_prompt(async_client: AsyncClient):
    """Test optimization with empty prompt."""
    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": "",
            "vendor": "openai"
        }
    )

    assert response.status_code == 422  # Validation error (min_length=1)


@pytest.mark.asyncio
@pytest.mark.parametrize("vendor", [
    "openai", "claude", "grok", "gemini", "qwen", "deepseek"
])
async def test_optimize_all_vendors_via_api(async_client: AsyncClient, vendor):
    """Test API optimization for all vendors."""
    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": "Test prompt",
            "vendor": vendor
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["vendor"] == vendor


@pytest.mark.asyncio
async def test_api_docs_available(async_client: AsyncClient):
    """Test that API documentation is available."""
    response = await async_client.get("/api/docs")
    assert response.status_code == 200


# Think Mode Tests

@pytest.mark.asyncio
async def test_generate_questions_endpoint_success(async_client: AsyncClient):
    """Test successful question generation endpoint."""
    response = await async_client.post(
        "/api/think/generate-questions",
        json={
            "prompt": "Explain machine learning",
            "vendor": "openai",
            "num_questions": 5
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert "total" in data
    assert isinstance(data["questions"], list)
    assert data["total"] >= 0


@pytest.mark.asyncio
async def test_generate_questions_with_10_questions(async_client: AsyncClient):
    """Test question generation with 10 questions."""
    response = await async_client.post(
        "/api/think/generate-questions",
        json={
            "prompt": "Teach me Python",
            "vendor": "claude",
            "num_questions": 10
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_generate_questions_with_25_questions(async_client: AsyncClient):
    """Test question generation with 25 questions."""
    response = await async_client.post(
        "/api/think/generate-questions",
        json={
            "prompt": "Advanced quantum physics",
            "vendor": "gemini",
            "num_questions": 25
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "questions" in data


@pytest.mark.asyncio
async def test_generate_questions_invalid_vendor(async_client: AsyncClient):
    """Test question generation with invalid vendor."""
    response = await async_client.post(
        "/api/think/generate-questions",
        json={
            "prompt": "Test",
            "vendor": "invalid_vendor",
            "num_questions": 5
        }
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_generate_questions_missing_fields(async_client: AsyncClient):
    """Test question generation with missing fields."""
    response = await async_client.post(
        "/api/think/generate-questions",
        json={
            "prompt": "Test"
            # Missing vendor and num_questions
        }
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_optimize_with_answers_endpoint_success(async_client: AsyncClient):
    """Test successful optimization with answers endpoint."""
    response = await async_client.post(
        "/api/think/optimize-with-answers",
        json={
            "prompt": "Teach me Python",
            "vendor": "openai",
            "questions": [
                "What is your knowledge level?",
                "What is your main goal?",
                "What format do you prefer?"
            ],
            "answers": [
                "Beginner",
                "Learn the basics",
                "Step-by-step tutorial"
            ]
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "original" in data
    assert "optimized" in data
    assert "vendor" in data
    assert "enhancement_notes" in data
    assert "metadata" in data
    assert data["vendor"] == "openai"


@pytest.mark.asyncio
async def test_optimize_with_answers_with_context(async_client: AsyncClient):
    """Test optimization with answers and context."""
    response = await async_client.post(
        "/api/think/optimize-with-answers",
        json={
            "prompt": "Explain AI",
            "vendor": "claude",
            "questions": ["Level?"],
            "answers": ["Expert"],
            "context": "For research paper"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["vendor"] == "claude"


@pytest.mark.asyncio
async def test_optimize_with_answers_mismatched_qa(async_client: AsyncClient):
    """Test optimization with mismatched questions and answers."""
    response = await async_client.post(
        "/api/think/optimize-with-answers",
        json={
            "prompt": "Test",
            "vendor": "openai",
            "questions": ["Q1?", "Q2?", "Q3?"],
            "answers": ["A1"]  # Only 1 answer for 3 questions
        }
    )

    assert response.status_code == 400  # Should fail validation


@pytest.mark.asyncio
async def test_optimize_with_answers_empty_questions(async_client: AsyncClient):
    """Test optimization with empty questions list."""
    response = await async_client.post(
        "/api/think/optimize-with-answers",
        json={
            "prompt": "Test",
            "vendor": "openai",
            "questions": [],
            "answers": []
        }
    )

    # Should either succeed with empty Q&A or fail validation
    assert response.status_code in [200, 400, 422]


@pytest.mark.asyncio
async def test_optimize_with_answers_invalid_vendor(async_client: AsyncClient):
    """Test optimization with answers using invalid vendor."""
    response = await async_client.post(
        "/api/think/optimize-with-answers",
        json={
            "prompt": "Test",
            "vendor": "invalid_vendor",
            "questions": ["Q1?"],
            "answers": ["A1"]
        }
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
@pytest.mark.parametrize("vendor", [
    "openai", "claude", "grok", "gemini", "qwen", "deepseek"
])
async def test_think_mode_all_vendors(async_client: AsyncClient, vendor):
    """Test Think Mode works with all vendors."""
    # Generate questions
    response = await async_client.post(
        "/api/think/generate-questions",
        json={
            "prompt": "Test prompt",
            "vendor": vendor,
            "num_questions": 5
        }
    )
    assert response.status_code == 200

    # Optimize with answers
    response = await async_client.post(
        "/api/think/optimize-with-answers",
        json={
            "prompt": "Test prompt",
            "vendor": vendor,
            "questions": ["Q1?"],
            "answers": ["A1"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["vendor"] == vendor
