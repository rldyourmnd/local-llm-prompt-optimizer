# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-10-04

### Added
- CODE_OF_CONDUCT.md for community guidelines
- GitHub issue templates (bug report, feature request, question)
- Pull request template for standardized contributions
- FUNDING.yml for project support information
- README badges for better project visibility

### Changed
- Updated Gemini vendor adapter to reflect latest API models:
  - Gemini 2.5 Pro (flagship with thinking mode)
  - Gemini 2.5 Flash (best price/performance)
  - Flash variants: Flash-Image, Flash-Live, Flash-TTS, Flash-Lite
- Updated Grok vendor adapter with documentation link (docs.x.ai)
- Updated Qwen vendor adapter for Qwen3 generation (July 2025 builds)
  - qwen3-235b and qwen3-30b replace Qwen 2.5
  - QwQ-32B for specialized reasoning tasks
- Updated DeepSeek vendor adapter with latest models:
  - DeepSeek-V3.2-Exp (Sep 29, 2025) with dual thinking/non-thinking modes
  - DeepSeek-R1-0528 (May 28, 2025) for advanced reasoning
- Updated README with vendor information and badges
- Bumped version to 1.0.2

### Documentation
- Enhanced vendor adapter docstrings with latest model information
- Improved open-source project structure and community guidelines

## [1.0.1] - 2025-10-04

### Fixed
- Resolved all flake8 E501 line length violations (>127 characters)
- Removed unused imports (F401 violations) in domain interfaces and vendor adapters
- Fixed GitHub Actions CI/CD pipeline permission issues
- Resolved npm dependency caching errors in frontend build

### Changed
- Updated LLM vendor model recommendations to latest versions
  - Qwen: Qwen3-235B (July 2025), Qwen3-30B, QwQ-32B
  - DeepSeek: V3.2-Exp (Sep 29, 2025), R1-0528 (May 28, 2025)
  - Gemini: 2.5 Pro, 2.5 Flash confirmed as current flagships
- Simplified CI/CD workflow by removing security scans requiring special permissions
- Improved error handling in GitHub Actions with informative messages

### Removed
- Release workflow attempting GHCR push without organization permissions
- CodeQL and Trivy security scans (require special repository permissions)

## [1.0.0] - 2025-10-04

### Added
- Initial production release
- Multi-vendor LLM prompt optimization (OpenAI, Claude, Grok, Gemini, Qwen, DeepSeek)
- Think Mode with AI-generated clarifying questions (5/10/25 questions)
- Domain-Driven Design architecture with clean separation of concerns
- FastAPI backend with REST endpoints
- React TypeScript frontend with Tailwind CSS
- Telegram bot integration with inline keyboards
- Docker Compose orchestration for all services
- PostgreSQL database for persistence
- Redis caching layer
- Comprehensive test suite
- GitHub Actions CI/CD pipeline
- Bilingual documentation (English/Russian)
- Environment-driven configuration (no hardcoded values)
- LM Studio client with OpenAI-compatible API
- Six vendor-specific optimization adapters
- Health check endpoints with LM Studio connectivity test
- Automatic language detection for question generation

### Documentation
- README.md with English and Russian sections
- CONTRIBUTING.md with contribution guidelines
- SECURITY.md with vulnerability reporting policy
- LICENSE (MIT)
- API_USAGE.md with REST API reference
- DEVELOPMENT.md with local development setup
- QUICKSTART.md for rapid onboarding
- PROJECT_STATUS.md for development roadmap

[1.0.1]: https://github.com/rldyourmnd/local-llm-prompt-optimizer/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/rldyourmnd/local-llm-prompt-optimizer/releases/tag/v1.0.0
