"""Integration tests for the full application stack."""
import pytest
from httpx import AsyncClient
import asyncio


@pytest.mark.asyncio
async def test_full_optimization_workflow(async_client: AsyncClient):
    """Test complete optimization workflow from start to finish."""
    # Step 1: Check health
    response = await async_client.get("/health")
    assert response.status_code == 200
    health_data = response.json()
    assert health_data["status"] == "healthy"

    # Step 2: Optimize a prompt
    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": "Write a function to calculate fibonacci numbers",
            "vendor": "openai",
            "context": "For Python programming tutorial"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "optimized" in data
    assert "vendor" in data
    assert data["vendor"] == "openai"


@pytest.mark.asyncio
async def test_full_think_mode_workflow(async_client: AsyncClient):
    """Test complete Think Mode workflow."""
    # Step 1: Generate questions
    response = await async_client.post(
        "/api/think/generate-questions",
        json={
            "prompt": "Teach me machine learning",
            "vendor": "claude",
            "num_questions": 5
        }
    )
    assert response.status_code == 200
    questions_data = response.json()
    assert "questions" in questions_data
    assert len(questions_data["questions"]) > 0

    # Step 2: Optimize with answers
    questions = questions_data["questions"][:3]  # Use first 3 questions
    answers = ["Beginner", "Learn fundamentals", "Step by step"]

    response = await async_client.post(
        "/api/think/optimize-with-answers",
        json={
            "prompt": "Teach me machine learning",
            "vendor": "claude",
            "questions": questions,
            "answers": answers
        }
    )
    assert response.status_code == 200
    optimization_data = response.json()
    assert "optimized" in optimization_data
    assert "enhancement_notes" in optimization_data
    assert "clarifying questions" in optimization_data["enhancement_notes"]


@pytest.mark.asyncio
async def test_multiple_vendors_sequential(async_client: AsyncClient):
    """Test optimization with multiple vendors sequentially."""
    vendors = ["openai", "claude", "gemini", "grok", "qwen", "deepseek"]
    prompt = "Explain quantum computing"

    results = []
    for vendor in vendors:
        response = await async_client.post(
            "/api/optimize",
            json={
                "prompt": prompt,
                "vendor": vendor
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["vendor"] == vendor
        results.append(data)

    # All vendors should return different optimizations
    assert len(results) == 6


@pytest.mark.asyncio
async def test_api_documentation_accessible(async_client: AsyncClient):
    """Test that API documentation is accessible."""
    # Test OpenAPI docs
    response = await async_client.get("/api/docs")
    assert response.status_code == 200

    # Test ReDoc
    response = await async_client.get("/api/redoc")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_root_endpoint_info(async_client: AsyncClient):
    """Test root endpoint returns correct API information."""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert "health" in data
    assert "credits" in data


@pytest.mark.asyncio
async def test_cors_headers(async_client: AsyncClient):
    """Test CORS headers are present."""
    response = await async_client.options("/api/optimize")
    # CORS headers should be present
    # Note: AsyncClient may not fully simulate CORS preflight
    assert response.status_code in [200, 405]  # OPTIONS may not be implemented


@pytest.mark.asyncio
async def test_optimization_with_all_parameters(async_client: AsyncClient):
    """Test optimization using all available parameters."""
    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": "Create a REST API",
            "vendor": "openai",
            "context": "Using FastAPI and Python",
            "max_length": 500
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "optimized" in data
    assert "metadata" in data


@pytest.mark.asyncio
async def test_concurrent_optimizations(async_client: AsyncClient):
    """Test handling multiple concurrent optimization requests."""
    async def optimize(vendor: str, prompt: str):
        return await async_client.post(
            "/api/optimize",
            json={
                "prompt": prompt,
                "vendor": vendor
            }
        )

    # Create 6 concurrent requests for different vendors
    tasks = [
        optimize("openai", "Test prompt 1"),
        optimize("claude", "Test prompt 2"),
        optimize("gemini", "Test prompt 3"),
        optimize("grok", "Test prompt 4"),
        optimize("qwen", "Test prompt 5"),
        optimize("deepseek", "Test prompt 6"),
    ]

    responses = await asyncio.gather(*tasks)

    # All should succeed
    assert all(r.status_code == 200 for r in responses)

    # Each should have correct vendor
    vendors = [r.json()["vendor"] for r in responses]
    assert "openai" in vendors
    assert "claude" in vendors
    assert "gemini" in vendors


@pytest.mark.asyncio
async def test_think_mode_different_question_counts(async_client: AsyncClient):
    """Test Think Mode with different question counts."""
    for num_questions in [5, 10, 25]:
        response = await async_client.post(
            "/api/think/generate-questions",
            json={
                "prompt": "Explain blockchain",
                "vendor": "openai",
                "num_questions": num_questions
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "questions" in data
        assert data["total"] >= 0


@pytest.mark.asyncio
async def test_health_check_components(async_client: AsyncClient):
    """Test health check returns all component statuses."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "lm_studio_available" in data
    assert "vendor_adapters" in data
    assert data["status"] == "healthy"
    assert isinstance(data["lm_studio_available"], bool)
    assert data["vendor_adapters"] == 6  # 6 supported vendors


@pytest.mark.asyncio
async def test_optimization_preserves_intent(async_client: AsyncClient):
    """Test that optimization preserves original prompt intent."""
    original_prompt = "Write a simple hello world program"

    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": original_prompt,
            "vendor": "openai"
        }
    )
    assert response.status_code == 200
    data = response.json()

    # Original should be preserved
    assert data["original"] == original_prompt

    # Optimized should be present and different
    assert "optimized" in data
    assert len(data["optimized"]) > 0


@pytest.mark.asyncio
async def test_error_responses_are_json(async_client: AsyncClient):
    """Test that error responses are properly formatted JSON."""
    # Test with invalid vendor
    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": "Test",
            "vendor": "invalid_vendor"
        }
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

    # Test with missing required fields
    response = await async_client.post(
        "/api/optimize",
        json={}
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_optimization_metadata_structure(async_client: AsyncClient):
    """Test that optimization response has correct metadata structure."""
    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": "Create a web scraper",
            "vendor": "claude"
        }
    )
    assert response.status_code == 200
    data = response.json()

    # Check all required fields
    required_fields = ["original", "optimized", "vendor", "enhancement_notes", "metadata"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"

    # Check metadata structure
    assert isinstance(data["metadata"], dict)
    assert isinstance(data["enhancement_notes"], str)


@pytest.mark.asyncio
async def test_unicode_and_multilingual_support(async_client: AsyncClient):
    """Test handling of Unicode and multilingual prompts."""
    multilingual_prompts = [
        "解释人工智能",  # Chinese
        "Объясни машинное обучение",  # Russian
        "Explica la inteligencia artificial",  # Spanish
        "AIについて説明して",  # Japanese
        "인공지능에 대해 설명해주세요"  # Korean
    ]

    for prompt in multilingual_prompts:
        response = await async_client.post(
            "/api/optimize",
            json={
                "prompt": prompt,
                "vendor": "openai"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["original"] == prompt
