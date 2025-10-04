# CI/CD Pipeline Overview

Complete automated testing and quality assurance for Local LLM Prompt Optimizer.

## 🔄 Workflows

### 1. **CI Pipeline** (`ci.yml`)
**Triggers:** Push/PR to `main`, `dev`, `develop`

**Jobs:**
- ✅ **Backend Lint & Test**
  - Python code linting (flake8)
  - Type checking (mypy)
  - Unit tests (pytest) with PostgreSQL
  - Code coverage reporting (Codecov)

- ✅ **Frontend Build & Lint**
  - ESLint checking
  - TypeScript compilation
  - Production build verification

- ✅ **Docker Build Verification**
  - Backend Docker image build
  - Frontend Docker image build
  - Build caching optimization

### 2. **Security Checks** (`security.yml`)
**Triggers:** Push/PR to `main`, `dev`, `develop` + Weekly schedule

**Jobs:**
- 🔒 **CodeQL Security Analysis**
  - Python security scanning
  - JavaScript security scanning
  - Extended security queries

- 🔒 **Dependency Review**
  - Vulnerability scanning in dependencies
  - Fails on moderate+ severity issues

- 🔒 **Python Security Scan (Bandit)**
  - Static security analysis for Python
  - JSON and text reports

- 🔒 **Docker Image Security Scan (Trivy)**
  - Container vulnerability scanning
  - CRITICAL and HIGH severity detection

- 🔒 **Secret Scanning (TruffleHog)**
  - Detects accidentally committed secrets
  - Scans entire git history

### 3. **Code Quality** (`code-quality.yml`)
**Triggers:** Push/PR to `main`, `dev`, `develop`

**Jobs:**
- 📊 **Python Code Quality**
  - Black formatting check
  - Flake8 comprehensive analysis
  - Pylint code analysis
  - Cyclomatic complexity (Radon)
  - Maintainability index

- 📊 **SonarCloud Analysis**
  - Code quality metrics
  - Code smells detection
  - Technical debt calculation
  - Coverage integration

- 📊 **Frontend Code Quality**
  - ESLint detailed analysis
  - TypeScript strict mode check

- 📊 **Documentation Quality**
  - Markdown linting
  - Link validation
  - Freshness check (90 days)

### 4. **Docker Build & Test** (`docker.yml`)
**Triggers:** Push/PR to `main`, `dev`, `develop`

**Jobs:**
- 🐳 **Backend Docker Build & Test**
  - Build verification
  - Container runtime test
  - Trivy security scan

- 🐳 **Frontend Docker Build & Test**
  - Build verification
  - HTTP response test

- 🐳 **Telegram Bot Docker Build**
  - Build verification

- 🐳 **Docker Compose Integration Test**
  - Full stack deployment test
  - Backend health check
  - Frontend availability

- 🐳 **Docker Image Size Check**
  - Monitors image bloat
  - Size reporting

### 5. **Performance Testing** (`performance.yml`)
**Triggers:** Push/PR to `main`, `dev` + Weekly schedule (Monday 2 AM)

**Jobs:**
- ⚡ **Backend Load Testing (Locust)**
  - 10 concurrent users
  - 60-second test duration
  - Health and API endpoints

- ⚡ **Memory Profiling**
  - Memory usage analysis
  - Leak detection

- ⚡ **Frontend Performance (Lighthouse)**
  - Performance score
  - Accessibility score
  - Best practices
  - SEO metrics

- ⚡ **Dependency Size Check**
  - Frontend bundle analysis
  - Python package sizes

## 📋 Quality Gates

### Must Pass (Blocking)
- ✅ All unit tests (45 tests)
- ✅ Python linting (flake8)
- ✅ Frontend build
- ✅ Docker builds

### Advisory (Non-blocking)
- ⚠️ Type checking (mypy)
- ⚠️ Security scans (informational)
- ⚠️ Code quality metrics
- ⚠️ Performance tests

## 🎯 Coverage Goals

- **Backend**: >80% code coverage
- **Frontend**: >70% code coverage
- **Integration**: All critical paths tested

## 🔐 Security Standards

- **Dependency Scanning**: All PRs checked
- **Secret Detection**: Full history scanned
- **Container Scanning**: CRITICAL/HIGH must be addressed
- **Code Security**: CodeQL extended queries

## 📊 Reporting

All workflows upload artifacts:
- `backend-coverage` - Code coverage reports
- `python-quality-reports` - Flake8, Pylint reports
- `frontend-quality-reports` - ESLint analysis
- `bandit-security-report` - Security findings
- `performance-results` - Load test results
- `memory-profile` - Memory usage data

## 🚀 Optimization Features

- **Caching**:
  - Python pip dependencies
  - Docker build layers (GitHub Cache)
  - Node.js modules

- **Parallel Execution**:
  - Backend/Frontend jobs run concurrently
  - Docker builds parallelized

- **Conditional Execution**:
  - SonarCloud only on push (not PR)
  - Dependency review only on PR
  - Performance tests weekly + on-demand

## 📈 Continuous Improvement

- Weekly scheduled scans catch gradual degradation
- Performance baselines tracked over time
- Dependency updates monitored
- Documentation freshness enforced

## 🛠️ Local Testing

Run checks locally before pushing:

```bash
# Backend
cd backend
flake8 src/ tests/
black --check src/ tests/
mypy src/
pytest tests/ -v --cov=src

# Frontend
cd frontend
npm run lint
npm run type-check
npm run build

# Docker
docker-compose build
docker-compose up -d
curl http://localhost:8000/health
```

## 📝 Adding New Checks

1. Create workflow in `.github/workflows/`
2. Add to this overview document
3. Test on `dev` branch first
4. Merge to `main` after verification

## 🔗 Integration Services

- **GitHub Actions**: All CI/CD orchestration
- **Codecov**: Code coverage tracking
- **SonarCloud**: Code quality analysis
- **Trivy**: Container security scanning
- **Lighthouse CI**: Frontend performance
- **TruffleHog**: Secret detection
