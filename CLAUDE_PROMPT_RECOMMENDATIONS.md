# Claude.md Prompt Recommendations - Based on Session 2 Learnings

**Document Purpose:** Comprehensive recommendations for updating the original project prompt based on Session 2 discoveries

**Project:** Conversation Analyzer
**Analysis Date:** November 18, 2025
**Sessions Analyzed:** 1 & 2
**Total Gaps Found:** 125 (2 CRITICAL security vulnerabilities)
**Evidence Source:** Complete Session 2 gap analysis with 125 documented issues

---

## Executive Summary

Based on comprehensive analysis of Session 1 and Session 2 outcomes, this document provides **evidence-based recommendations** for improving the original prompt that created this project.

**Key Finding:** The original prompt produced excellent results (research-first approach, phased implementation, comprehensive documentation), BUT missed critical security vulnerabilities and left 125 improvement opportunities undiscovered until explicit "% sure you researched 100%?" question was asked.

**Impact:** Session 1 ended with A+ self-assessment and 100% confidence, but Session 2 comprehensive analysis revealed:
- 2 CRITICAL security vulnerabilities (SQL injection, pickle deserialization)
- 18 HIGH priority issues (missing tests, path traversal, race conditions)
- 64 MEDIUM priority issues (missing features, incomplete infrastructure)
- 41 LOW priority issues (documentation, usability enhancements)

**Root Cause:** Original prompt lacked explicit mandates for:
1. Security-first development with OWASP checklist
2. Per-module test verification (not just "write tests")
3. Design-to-implementation verification
4. Dead code detection
5. Exhaustive gap analysis built into workflow

---

## Original Prompt Analysis

### What the Original Prompt Said (Reconstructed from Summary)

Based on Session 1 summary, the original prompt included:

```markdown
"🔬 Research Phase Guidance
- Existing tools evaluation mandate
- Model selection criteria
- Prompt engineering research
- Framework comparison

🏗️ Implementation Phases
1. Research (don't skip!)
2. Design (architecture, schema, prompts)
3. MVP (parser, extractor, reports)
4. Intelligence (dedup, scoring, linking)
5. Integration (automation, updates)

📊 Example Input/Output
- Shows exactly what analysis should look like
- Includes confidence scores, source tracking
- Demonstrates priority classification

Testing:
'we will need to do testing too on this so lets research
tools/models/prompts/research to help with that.'
"
```

### What Worked Excellently ✅

1. **Research-First Approach**
   - Resulted in 824-line RESEARCH_REPORT.md
   - Prevented architectural mistakes
   - Led to optimal technology choices

2. **Phased Implementation**
   - Clear milestones prevented scope creep
   - 12 semantic commits representing logical phases
   - Incremental value delivery

3. **Explicit Tech Stack**
   - Python, Ollama, SQLite specified
   - Privacy requirements (offline, local) clear
   - Reduced ambiguity

### What Failed Critically ❌

1. **"Research Testing" ≠ "Implement Tests"**
   - Prompt said: "research tools/models/prompts/research to help with that"
   - Agent interpreted: Research testing frameworks (✅ done)
   - Missing: IMPLEMENT comprehensive test suite (❌ not done initially)
   - **Impact:** 0 actual tests despite 3,500+ lines of code

2. **No Security Mandate**
   - No mention of OWASP Top 10
   - No requirement to check for SQL injection, path traversal, unsafe deserialization
   - **Impact:** 2 CRITICAL vulnerabilities shipped in "A+" code

3. **No Verification Checklist**
   - Design mentioned DocumentParser, GitAnalyzer
   - No requirement to verify all designed components built
   - **Impact:** Features designed but not implemented

4. **No "Every Module" Specification**
   - Said "write tests" not "write test for EVERY module"
   - **Impact:** 6 major modules with 0% test coverage despite 68+ tests total

5. **No Dead Code Detection**
   - No requirement to verify all code integrated
   - **Impact:** text_chunking.py implemented but never imported/used

---

## Recommended Claude.md Structure

Based on all learnings, here's the complete recommended prompt:

```markdown
# Project: [Name]

## 🎯 Success Criteria (ALL Required for Completion)

Before declaring project complete, ALL must be verified:

- [ ] 80%+ test coverage for EVERY module (per-file, not aggregate)
- [ ] All CRITICAL and HIGH security issues fixed (Bandit, Safety, Semgrep pass)
- [ ] All code type-hinted and mypy passes with no errors
- [ ] Production-ready error handling on all external calls
- [ ] Complete documentation (README, installation, usage, troubleshooting, API)
- [ ] All standard project files present (see checklist below)
- [ ] CI/CD pipeline configured and passing on all platforms
- [ ] Design-to-implementation verification complete (all designed features exist)
- [ ] Dead code detection complete (no orphaned implementations)
- [ ] Real examples generated (not just described)
- [ ] Self-assessed as A+ quality WITH EVIDENCE

## 🔒 Security-First Development (MANDATORY)

**CRITICAL: Security is not optional. All security checks must pass before proceeding.**

### Phase 1: Security Research (Include in Research Phase)

Research and document in RESEARCH_REPORT.md:
- [ ] OWASP Top 10 vulnerabilities for Python
- [ ] Language-specific security issues (pickle, SQL injection, path traversal, command injection)
- [ ] Dependency vulnerability scanning tools (Safety, Snyk, Dependabot)
- [ ] Secure coding practices for this tech stack
- [ ] Common attack vectors for similar applications

### Phase 2: Secure Design (Include in Design Phase)

Document in DESIGN.md:
- [ ] Input validation strategy (validate ALL user inputs)
- [ ] Database security (parameterized queries, no SQL injection)
- [ ] File handling security (path validation, no traversal attacks)
- [ ] Serialization strategy (JSON not pickle, no unsafe deserialization)
- [ ] Rate limiting and DoS prevention
- [ ] Authentication/authorization approach (if applicable)
- [ ] Secrets management (environment variables, never hardcoded)

### Phase 3: Secure Implementation (Every Feature)

For EVERY function that:
- **Accepts user input:** Validate type, range, format, sanitize for injection
- **Queries database:** Use parameterized queries (?, %s), NEVER f-strings in SQL
- **Reads files:** Validate paths with Path.resolve(), check against base directory
- **Executes commands:** Sanitize inputs, avoid shell=True, use subprocess safely
- **Serializes data:** Use JSON/msgpack, NEVER pickle on untrusted data
- **Handles secrets:** Use environment variables, never hardcode API keys

### Phase 4: Security Testing (Before Final Commit)

Run ALL security tools and fix issues:
```bash
# Python security linter
bandit -r src/ -ll

# Dependency vulnerability scanner
safety check

# SAST (Static Application Security Testing)
semgrep --config=auto .

# Type checking
mypy src/ --strict
```

ALL tools must pass with 0 CRITICAL/HIGH issues before proceeding.

### Phase 5: Security Documentation

Create SECURITY.md with:
- [ ] Vulnerability reporting process
- [ ] Security assumptions documented
- [ ] Threat model (what attacks are we preventing?)
- [ ] Security testing performed
- [ ] Known limitations

**Security Checklist (Verify Before Declaring Complete):**
- [ ] No SQL injection (verified with parameterized queries, tested)
- [ ] No path traversal (verified with path validation, tested with ../../../etc/passwd)
- [ ] No unsafe deserialization (no pickle, verified)
- [ ] No command injection (no shell=True, verified)
- [ ] No hardcoded secrets (grep for "api_key", "password", "secret")
- [ ] Input validation on ALL user-provided data
- [ ] Output encoding where applicable
- [ ] Rate limiting on expensive operations
- [ ] File size limits on uploads/processing

## 🧪 Test-Driven Development (STRICT MANDATE)

**CRITICAL: Write tests FIRST for every feature. No exceptions.**

### TDD Workflow for Every Feature

1. **Write Tests First (Red)**
   ```python
   # tests/test_feature.py
   def test_feature_happy_path():
       assert feature_function(valid_input) == expected_output

   def test_feature_edge_case_empty():
       assert feature_function("") raises ValueError

   def test_feature_injection_attack():
       assert feature_function("'; DROP TABLE--") is_safe
   ```

2. **Verify Tests Fail** (they should, nothing implemented yet)
   ```bash
   pytest tests/test_feature.py  # Should fail
   ```

3. **Implement Minimal Code** (Green)
   ```python
   # src/feature.py
   def feature_function(input):
       # Minimal implementation to pass tests
   ```

4. **Verify Tests Pass**
   ```bash
   pytest tests/test_feature.py  # Should pass
   ```

5. **Refactor for Quality**
   - Add type hints
   - Improve error handling
   - Add documentation
   - Optimize if needed

6. **Commit Atomically**
   ```bash
   git add tests/test_feature.py src/feature.py
   git commit -m "feat: add feature with tests"
   ```

### Per-Module Test Verification (MANDATORY)

For EVERY .py file in src/ (excluding __init__.py), verify:

```
src/module.py -> tests/test_module.py MUST exist
```

**Verification Script (Run Before Every Commit):**

```python
# scripts/verify_test_coverage.py
from pathlib import Path

src_files = Path('src').rglob('*.py')
missing_tests = []

for src_file in src_files:
    if src_file.name == '__init__.py':
        continue

    test_file = Path('tests') / src_file.relative_to('src').with_name(f'test_{src_file.name}')

    if not test_file.exists():
        missing_tests.append(f"❌ {src_file} -> {test_file} MISSING")
    else:
        print(f"✓ {src_file} -> {test_file}")

if missing_tests:
    print("\n🚨 MISSING TEST FILES:")
    for missing in missing_tests:
        print(missing)
    print("\n⛔ FIX: Create test files before proceeding")
    exit(1)
else:
    print("\n✅ All modules have test files")
```

**Run this script before EVERY commit. If ANY test file is missing: STOP and create it.**

### Test Coverage Requirements

- **Minimum per module:** 80% line coverage
- **Verify with:** `pytest --cov=src --cov-report=term-missing`
- **If ANY module < 80%:** STOP and write more tests

### Required Test Types

For each module:
- [ ] **Unit tests:** Every function, every class method
- [ ] **Edge cases:** Empty input, null, invalid types
- [ ] **Error paths:** Exception handling, error messages
- [ ] **Security tests:** Injection attacks, path traversal, malformed input
- [ ] **Integration tests:** Full workflows with mocked dependencies

### Mock External Dependencies

NEVER require external services for tests:
```python
# conftest.py
@pytest.fixture
def mock_ollama():
    class MockOllama:
        def generate(self, prompt):
            return '{"items": [{"type": "TODO", ...}]}'
    return MockOllama()

# test_extractor.py
def test_extraction(mock_ollama):
    extractor = Extractor(client=mock_ollama)
    # Test without real Ollama
```

## 🔬 Research Phase (DON'T SKIP!)

### What to Research

1. **Existing Tools Evaluation**
   - List 5+ competitors/similar tools
   - What features do they have?
   - What are their limitations?
   - What can we do better?

2. **Technology Selection**
   - Which LLM models are best for this task? (benchmark)
   - Which frameworks? (pros/cons comparison)
   - Which testing tools? (evaluation with examples)
   - Which CI/CD platforms?

3. **Security Research** (See Security-First section)

4. **Testing Strategy**
   - Which test frameworks? (pytest, unittest, nose)
   - How to test LLM outputs? (DeepEval, Promptfoo)
   - How to mock external dependencies?
   - What's industry standard coverage? (80%+)

5. **Infrastructure Research**
   - Which CI/CD? (GitHub Actions, GitLab CI, CircleCI)
   - Which container platform? (Docker, Podman)
   - Which deployment targets? (AWS, GCP, self-hosted)
   - Which monitoring/observability tools?

### Research Deliverable

Create RESEARCH_REPORT.md with:
- [ ] Executive summary of decisions
- [ ] Comparison tables (tool A vs B vs C)
- [ ] Citations for all claims
- [ ] Specific recommendations with justification
- [ ] What we're building vs deferring

**Minimum 500 lines of documented research.**

## 🏗️ Design Phase

### Design Deliverable: DESIGN.md

Create comprehensive design document with:

1. **System Architecture**
   - ASCII diagram of components
   - Data flow diagram
   - Component responsibilities
   - Technology choices justified

2. **Database Schema**
   - All tables with columns, types, constraints
   - Indexes for performance
   - Relationships and foreign keys
   - Sample queries

3. **API Design**
   - All public functions/methods
   - Parameters and return types
   - Error conditions
   - Example usage

4. **Module Structure**
   - Directory tree
   - File purposes
   - Import relationships
   - Configuration approach

5. **Testing Strategy**
   - What tests for each module
   - Mock strategy
   - CI/CD pipeline design
   - Coverage targets

6. **Security Design** (See Security-First section)

7. **Component Checklist**

   **CRITICAL: Extract every component mentioned and create checklist:**

   ```markdown
   ## Implementation Checklist

   From DESIGN.md, implement:

   - [ ] ConversationParser (src/parsers/conversation.py + tests/test_conversation.py)
   - [ ] CodeParser (src/parsers/code.py + tests/test_code.py)
   - [ ] DocumentParser (src/parsers/document.py + tests/test_document.py)
   - [ ] Extractor (src/extraction/extractor.py + tests/test_extractor.py)
   - [ ] Deduplicator (src/intelligence/deduplicator.py + tests/test_deduplicator.py)
   - [ ] etc.

   **Check off ONLY when:**
   - Implementation file exists with full functionality
   - Test file exists with 80%+ coverage
   - Integrated into main workflow (imported and used)
   - Configuration connected (if needed)
   ```

   **Use this checklist during implementation. If design mentions it, implementation MUST have it.**

**Minimum 800 lines of documented design.**

## 🚀 Implementation Phases

### Phase 1: Project Structure & Configuration

```bash
project/
├── .github/
│   ├── workflows/
│   │   ├── test.yml          # CI testing (Linux, macOS, Windows)
│   │   └── release.yml       # Automated releases
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── src/
│   └── [your_project]/
│       ├── __init__.py       # Public API exports
│       ├── models.py         # Pydantic models
│       ├── config.py         # Configuration management
│       └── ... (other modules)
├── tests/
│   ├── conftest.py           # Pytest fixtures, mocks
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── fixtures/             # Test data
├── docs/
│   ├── INSTALLATION.md       # Step-by-step install
│   ├── USAGE.md              # User guide
│   ├── TROUBLESHOOTING.md    # Common errors & fixes
│   └── DEVELOPMENT.md        # Developer guide
├── examples/
│   ├── inputs/               # Sample input files
│   └── outputs/              # Example outputs (actually generated!)
├── scripts/
│   └── verify_test_coverage.py
├── .gitignore                # Comprehensive for your language
├── .editorconfig             # Editor consistency
├── .pre-commit-config.yaml   # Pre-commit hooks
├── LICENSE                   # MIT, Apache 2.0, or specified
├── README.md                 # With badges, quickstart
├── CONTRIBUTING.md           # Contribution guidelines
├── CHANGELOG.md              # Version history (Keep a Changelog format)
├── CODE_OF_CONDUCT.md        # Contributor Covenant
├── SECURITY.md               # Vulnerability reporting
├── RESEARCH_REPORT.md        # Research findings
├── DESIGN.md                 # System design
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project metadata
└── Dockerfile                # Container image
```

**Create ALL of these files. No exceptions.**

### Phase 2: Core Implementation (TDD)

For each module:

1. **Design tests FIRST** (based on DESIGN.md)
2. **Write tests** (red)
3. **Implement** (green)
4. **Refactor** (clean)
5. **Verify** (tests pass, coverage >80%)
6. **Commit** (atomic, tests + implementation together)

**Order:**
1. Data models (models.py + tests)
2. Configuration (config.py + tests)
3. Core logic (business logic + tests)
4. Integrations (APIs, databases + tests)
5. CLI/UI (interface + tests)

### Phase 3: Integration Testing

Test full workflows:
- [ ] End-to-end user scenarios
- [ ] Error recovery paths
- [ ] Performance under load
- [ ] Concurrent access (if applicable)
- [ ] Real data processing (anonymized)

### Phase 4: Documentation & Examples

**CRITICAL: Generate REAL examples, don't just describe:**

```bash
# 1. Create sample inputs
examples/inputs/sample_conversation.md

# 2. RUN YOUR TOOL on the inputs
python -m your_project analyze examples/inputs/sample_conversation.md --output examples/outputs/

# 3. COMMIT the actual outputs
examples/outputs/report.md
examples/outputs/report.json
examples/outputs/cli_output.txt

# 4. LINK in README
"See [examples/outputs/report.md](examples/outputs/report.md) for real output."
```

Users need to SEE what your tool produces, not imagine it.

### Phase 5: Infrastructure & DevOps

1. **CI/CD (GitHub Actions)**

   ```yaml
   # .github/workflows/test.yml
   name: Tests

   on: [push, pull_request]

   jobs:
     test:
       strategy:
         matrix:
           os: [ubuntu-latest, macos-latest, windows-latest]
           python-version: ['3.10', '3.11', '3.12']

       runs-on: ${{ matrix.os }}

       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v4
           with:
             python-version: ${{ matrix.python-version }}
         - run: pip install -r requirements.txt
         - run: pytest --cov=src --cov-report=xml
         - run: bandit -r src/ -ll
         - run: safety check
         - run: mypy src/ --strict
   ```

2. **Pre-commit Hooks**

   ```yaml
   # .pre-commit-config.yaml
   repos:
     - repo: https://github.com/psf/black
       rev: 23.11.0
       hooks:
         - id: black
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.1.6
       hooks:
         - id: ruff
     - repo: https://github.com/pre-commit/mirrors-mypy
       rev: v1.7.1
       hooks:
         - id: mypy
   ```

3. **Docker**

   ```dockerfile
   # Dockerfile
   FROM python:3.11-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .

   CMD ["python", "-m", "your_project"]
   ```

4. **Dependency Security**

   ```yaml
   # .github/dependabot.yml
   version: 2
   updates:
     - package-ecosystem: "pip"
       directory: "/"
       schedule:
         interval: "weekly"
   ```

## 🔍 Mandatory Self-Critique Checkpoints

**CRITICAL: After each phase, STOP and run comprehensive self-analysis.**

### After Research Phase

Ask yourself:
- [ ] Did I research ALL categories (tools, security, testing, infra, docs)?
- [ ] Do I have citations for all claims?
- [ ] Did I compare 3+ alternatives for each decision?
- [ ] Is security research included (OWASP Top 10)?
- [ ] Is testing strategy documented (which frameworks, why)?

**If ANY answer is NO: go back and research more.**

### After Design Phase

Ask yourself:
- [ ] Does DESIGN.md mention every component I plan to build?
- [ ] Did I create implementation checklist from DESIGN.md?
- [ ] Is database schema complete with types, constraints, indexes?
- [ ] Is security design documented (input validation, serialization)?
- [ ] Is testing strategy specified per module?

**If ANY answer is NO: update DESIGN.md.**

### After Implementation Phase

Run these commands and verify ALL pass:

```bash
# 1. Test coverage (MUST be 80%+ for EVERY module)
pytest --cov=src --cov-report=term-missing

# 2. Verify test files exist
python scripts/verify_test_coverage.py

# 3. Security checks (MUST pass with 0 CRITICAL/HIGH)
bandit -r src/ -ll
safety check
semgrep --config=auto .

# 4. Type checking (MUST pass)
mypy src/ --strict

# 5. Dead code detection
grep -r "import.*module_name" .  # For each module, verify it's imported

# 6. Design verification
# Open DESIGN.md checklist, verify every component exists
```

**If ANY check fails: STOP and fix before proceeding.**

### Design-to-Implementation Verification (MANDATORY)

```bash
# Create this script: scripts/verify_design_implementation.py
"""
Read DESIGN.md, extract all mentioned components.
For each component:
1. Verify implementation file exists
2. Verify test file exists
3. Verify it's imported somewhere (not orphaned)
4. Verify configuration exists (if needed)

Report missing components.
"""
```

**Run this script. If anything missing: implement it or remove from design.**

### Dead Code Detection (MANDATORY)

```bash
# For each .py file in src/
for file in src/**/*.py; do
    module=$(basename $file .py)

    # Check if imported anywhere
    if ! grep -r "from.*import.*$module" . &>/dev/null; then
        if ! grep -r "import.*$module" . &>/dev/null; then
            echo "⚠️  $file implemented but never imported (dead code)"
        fi
    fi
done
```

**If ANY dead code found: either integrate it or delete it.**

### Final Self-Assessment (Before Declaring Complete)

Grade yourself honestly on each category:

**Code Quality:**
- [ ] All functions type-hinted: A/B/C/D/F
- [ ] No TODO comments in code: A/B/C/D/F
- [ ] Comprehensive error handling: A/B/C/D/F
- [ ] Secure coding practices: A/B/C/D/F
- [ ] Performance optimized: A/B/C/D/F

**Testing:**
- [ ] 80%+ coverage per module: A/B/C/D/F
- [ ] Tests for all edge cases: A/B/C/D/F
- [ ] Tests for security (injection, traversal): A/B/C/D/F
- [ ] Integration tests: A/B/C/D/F
- [ ] All tests passing: A/B/C/D/F

**Documentation:**
- [ ] README clear & comprehensive: A/B/C/D/F
- [ ] Installation instructions complete: A/B/C/D/F
- [ ] Troubleshooting guide: A/B/C/D/F
- [ ] API documentation: A/B/C/D/F
- [ ] Real examples provided: A/B/C/D/F

**Infrastructure:**
- [ ] CI/CD configured: A/B/C/D/F
- [ ] All platforms tested: A/B/C/D/F
- [ ] Security scanning: A/B/C/D/F
- [ ] Pre-commit hooks: A/B/C/D/F
- [ ] Docker support: A/B/C/D/F

**Security:**
- [ ] No SQL injection: A/B/C/D/F
- [ ] No path traversal: A/B/C/D/F
- [ ] No unsafe deserialization: A/B/C/D/F
- [ ] All inputs validated: A/B/C/D/F
- [ ] Security tools pass: A/B/C/D/F

**Overall Grade:** [A+/A/B/C/D/F]

**If not A+:** List specific gaps and fix them before proceeding.

## 🔎 Final Gap Analysis (MANDATORY)

**CRITICAL: Before declaring project complete, run exhaustive gap analysis.**

### Launch Gap Analysis Agent

Use Task tool with general-purpose agent:

```
"Analyze this codebase EXHAUSTIVELY for gaps:

1. Security Vulnerabilities:
   - SQL injection (check all database queries)
   - Path traversal (check all file operations)
   - Unsafe deserialization (check for pickle usage)
   - Command injection (check subprocess calls)
   - Hardcoded secrets (grep for api_key, password)
   - Input validation (check all user inputs)

2. Missing Features:
   - Compare README promises vs actual implementation
   - Compare DESIGN.md components vs src/ files
   - Check configuration options vs actual code
   - Identify unused implementations

3. Test Coverage Gaps:
   - List all .py files without test files
   - Calculate coverage per module
   - Identify untested functions
   - Check for missing edge case tests

4. Documentation Gaps:
   - Missing installation steps
   - Unclear usage instructions
   - No troubleshooting guide
   - Missing API documentation
   - No real examples

5. Infrastructure Gaps:
   - CI/CD not configured
   - Missing platform support (Windows, Mac, Linux)
   - No pre-commit hooks
   - No dependency scanning
   - No SAST tools

6. Integration Gaps:
   - Implemented files not imported
   - Functions defined but never called
   - Configuration exists but unused
   - Dead code detection

Be BRUTALLY thorough. Find EVERYTHING."
```

### Process Gap Analysis Results

Categorize findings:
- **CRITICAL:** Fix immediately (security vulnerabilities)
- **HIGH:** Fix before v1.0 (missing core features, test gaps)
- **MEDIUM:** Fix before next release (documentation, infrastructure)
- **LOW:** Add to backlog (nice-to-haves)

**Fix ALL CRITICAL and HIGH before declaring complete.**

Create KNOWN_ISSUES.md for MEDIUM and LOW:

```markdown
# Known Issues

## MEDIUM Priority (Next Release)
- Missing CSV export feature
- No Docker Compose configuration
- Performance not optimized for 1000+ files

## LOW Priority (Backlog)
- VS Code extension not available
- No multi-language support
- No web UI
```

## 📋 Final Deliverables Checklist

Before declaring project complete, verify ALL exist:

### Code & Tests (Verify Physically)
- [ ] All source files in src/ with type hints
- [ ] ALL test files in tests/ (verify with script)
- [ ] conftest.py with fixtures and mocks
- [ ] 80%+ coverage for EVERY module (verify with pytest)
- [ ] All tests passing (verify with pytest)
- [ ] No TODO comments in code (grep for TODO)

### Security (Verify Tools Pass)
- [ ] Bandit passes (0 CRITICAL/HIGH): `bandit -r src/ -ll`
- [ ] Safety passes: `safety check`
- [ ] Semgrep passes: `semgrep --config=auto .`
- [ ] MyPy passes: `mypy src/ --strict`
- [ ] Manual review for SQL injection, path traversal, pickle

### Documentation (Verify Files Exist)
- [ ] README.md with badges (build, coverage, license)
- [ ] docs/INSTALLATION.md (step-by-step for all platforms)
- [ ] docs/USAGE.md (command reference with examples)
- [ ] docs/TROUBLESHOOTING.md (common errors & solutions)
- [ ] docs/DEVELOPMENT.md (developer setup guide)
- [ ] CONTRIBUTING.md (contribution workflow)
- [ ] CHANGELOG.md (version history, Keep a Changelog format)
- [ ] CODE_OF_CONDUCT.md (Contributor Covenant)
- [ ] SECURITY.md (vulnerability reporting)
- [ ] RESEARCH_REPORT.md (research findings)
- [ ] DESIGN.md (system architecture)

### Project Files (Verify Files Exist)
- [ ] LICENSE (MIT, Apache 2.0, or specified)
- [ ] .gitignore (comprehensive for your language)
- [ ] .editorconfig (editor consistency)
- [ ] requirements.txt or package.json
- [ ] pyproject.toml or setup.py
- [ ] .env.example (if environment variables used)

### CI/CD (Verify Workflows)
- [ ] .github/workflows/test.yml (runs on push/PR)
- [ ] .github/workflows/release.yml (automated releases)
- [ ] .github/ISSUE_TEMPLATE/bug_report.md
- [ ] .github/ISSUE_TEMPLATE/feature_request.md
- [ ] .pre-commit-config.yaml (formatting, linting)
- [ ] .github/dependabot.yml (dependency scanning)

### Infrastructure (Verify Files)
- [ ] Dockerfile (container image)
- [ ] docker-compose.yml (if multi-service)
- [ ] .dockerignore (optimize builds)
- [ ] Makefile (common tasks: test, lint, format, clean)

### Examples (Verify Generated)
- [ ] examples/inputs/ (sample input files)
- [ ] examples/outputs/ (REAL outputs from running tool)
- [ ] examples/README.md (explaining examples)

### Design Verification (Manual Check)
- [ ] Open DESIGN.md implementation checklist
- [ ] Verify every component has implementation file
- [ ] Verify every component has test file
- [ ] Verify every component is integrated (imported/used)
- [ ] Verify no orphaned code (run dead code detection)

### Git Verification
- [ ] All changes committed
- [ ] Commit messages semantic (feat:, fix:, docs:, etc.)
- [ ] All commits pushed to remote
- [ ] Branch protection rules (if team project)

## 🎓 Key Lessons from Session 2

### Lesson 1: "Research Testing" ≠ "Implement Tests"

**What Happened:**
- Original prompt: "we will need to do testing too so let's research tools/models/prompts"
- Agent response: Created RESEARCH_REPORT.md with testing tools (✅)
- What was MISSING: Actually implementing 68+ test files (❌)

**Fix in Prompt:**
```markdown
Instead of: "research testing tools"

Use: "Implement comprehensive test suite:
- Create test file for EVERY module
- Achieve 80%+ coverage per file
- Include unit, integration, security tests
- Run pytest --cov before each commit"
```

### Lesson 2: Self-Assessment Without Verification is Insufficient

**What Happened:**
- Session 1: Agent self-assessed A+ quality, 100% confidence
- Session 2: Found 125 gaps including 2 CRITICAL security vulnerabilities

**Fix in Prompt:**
```markdown
Add mandatory verification:
- Run security scanners (Bandit, Safety, Semgrep)
- Verify test coverage per module
- Run dead code detection
- Verify design-to-implementation
- Launch gap analysis agent

Only declare A+ AFTER verification, not before.
```

### Lesson 3: Design Documents Must Be Implementation Checklists

**What Happened:**
- DESIGN.md mentioned DocumentParser, GitAnalyzer
- Implementation phase didn't verify all components built
- Result: Configuration exists but no implementation

**Fix in Prompt:**
```markdown
Add to design phase:
"Extract every component from DESIGN.md into checklist.
During implementation, check off ONLY when:
- Implementation exists
- Tests exist (80%+ coverage)
- Integrated (imported and used)
- Configuration connected (if needed)

Before declaring phase complete: review checklist, implement missing."
```

### Lesson 4: "Write Tests" ≠ "Test Every Module"

**What Happened:**
- 68+ tests written (impressive!)
- But 6 major modules had 0% coverage

**Fix in Prompt:**
```markdown
Add per-module verification:
"For EVERY .py file in src/, verify tests/test_*.py exists.
Run verification script before each commit.
If ANY module < 80% coverage: STOP and write tests."
```

### Lesson 5: Dead Code Must Be Detected

**What Happened:**
- text_chunking.py implemented but never imported
- build_nuextract_prompt() defined but never called

**Fix in Prompt:**
```markdown
Add dead code detection:
"After implementing each module:
1. grep -r 'import.*module_name' to verify it's imported
2. For each function, verify it's called somewhere
3. If config option exists, verify code uses it

If orphaned: either integrate it or delete it."
```

## 📊 Evidence-Based Improvements Summary

| Issue | Original Prompt | Impact | Fix Required |
|-------|----------------|--------|--------------|
| Testing | "research testing tools" | 0 tests initially | "Implement tests for EVERY module" |
| Security | Not mentioned | 2 CRITICAL vulns | "Run Bandit, Safety, Semgrep, pass required" |
| Verification | None | 125 gaps undetected | "Launch gap analysis agent before complete" |
| Design Check | None | Features designed not built | "Use DESIGN.md as checklist, verify all exist" |
| Per-Module | "write tests" | 6 modules 0% coverage | "Verify test file for EVERY module" |
| Dead Code | None | Unused implementations | "Detect dead code, integrate or delete" |
| Platform | Not specified | Only Ubuntu/Mac tested | "Test on Windows, Linux, Mac in CI" |
| Examples | "describe output" | No real examples | "Generate REAL examples by running tool" |

## 🚀 Complete Updated Prompt Template

[See full template above - this section would include the complete 100% improved prompt incorporating all learnings]

---

## Conclusion

The original prompt was **excellent** and produced a high-quality project. However, Session 2 revealed that explicit mandates for security, per-module testing, and exhaustive verification would have prevented:

- 2 CRITICAL security vulnerabilities
- 18 HIGH priority gaps
- 64 MEDIUM priority gaps
- 41 LOW priority gaps

**Key Insight:** The difference between "A+ quality" and "A+ quality WITH verification" is the difference between:
- Believing you're done (Session 1)
- Proving you're done (Session 2)

**Recommendation:** Use this updated prompt template for future projects to achieve verified A+ quality from the start.

---

**Document Version:** 1.0
**Created:** November 18, 2025
**Based On:** Session 2 comprehensive gap analysis (125 issues documented)
**Purpose:** Improve prompt engineering for future AI agent projects
**Evidence:** Complete Session 2 findings with security vulnerabilities, missing features, and verification gaps documented
