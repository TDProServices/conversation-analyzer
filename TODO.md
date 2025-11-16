# TODO: Conversation Analyzer

**Last Updated:** 2025-11-16 07:00
**Project:** Local LLM-powered conversation and file analysis system

---

## 🚨 HIGH PRIORITY (Blocking)

### 1. Complete research phase findings
**Status:** IN PROGRESS
**Blocker:** None

**Description:**
Web session completed initial research but needs to synthesize findings into actionable recommendations.

**Action:**
1. Review research notes from Web session
2. Document recommended tools/frameworks
3. Make architecture decisions based on research
4. Get user approval before implementation

### 2. Set up project structure
**Status:** PENDING
**Blocker:** Needs research completion

**Description:**
Create proper Python project structure with dependencies, Docker setup, and dev environment.

**Action:**
1. Create pyproject.toml or requirements.txt
2. Set up Docker configuration (if beneficial)
3. Configure linting (ruff, black, mypy)
4. Add .gitignore for Python
5. Create src/ and tests/ directories

---

## ⚠️ MEDIUM PRIORITY (Important but not blocking)

### 1. Implement conversation parser
**Status:** PENDING

**Description:**
Parse Claude Code conversation exports (markdown format) to extract structured data.

**Action:**
- Research existing markdown parsers
- Handle conversation format (user/assistant messages)
- Extract metadata (timestamps, file references)
- Test with real conversation files

### 2. Implement Ollama integration
**Status:** PENDING

**Description:**
Connect to local Ollama instance for LLM-based analysis.

**Action:**
- Research Ollama Python client libraries
- Implement retry/timeout handling
- Test different models (qwen2.5:3b vs llama3.1:8b)
- Create prompt templates for extraction tasks

### 3. Design database schema
**Status:** PENDING

**Description:**
SQLite schema for storing extracted items, sources, and relationships.

**Action:**
- Items table (todos, bugs, features)
- Sources table (file paths, line numbers)
- Deduplication tracking
- Cross-reference relationships

---

## 📋 LOW PRIORITY (Nice to have)

### 1. GitHub issue integration
**Status:** BACKLOG

**Description:**
Automatically create GitHub issues from discovered items.

**Action:**
- Use gh CLI
- Map item types to issue labels
- Include source references
- Handle rate limiting

### 2. Web dashboard
**Status:** BACKLOG

**Description:**
Optional web UI for viewing analysis results.

**Action:**
- Consider if CLI + markdown reports sufficient
- Evaluate lightweight frameworks (Flask, FastAPI)
- Only build if genuinely needed

---

## 🔮 FUTURE ENHANCEMENTS (Backlog)

### 1. Support for other conversation formats
**Status:** BACKLOG

**Description:**
Parse ChatGPT exports, Gemini logs, etc.

**Action:**
Evaluate demand before implementing

### 2. Real-time analysis
**Status:** BACKLOG

**Description:**
Watch directories and analyze new conversations automatically.

**Action:**
Use file system watchers (watchdog library)

### 3. Integration with project management tools
**Status:** BACKLOG

**Description:**
Export to Jira, Linear, Asana, etc.

**Action:**
Only if user requests

---

## ✅ COMPLETED TASKS

### Session 2025-11-16 05:00 (Web - Initial Research)
- [x] Researched existing conversation analysis tools (commit unknown - Web session)
- [x] Evaluated TODO extraction approaches (commit unknown - Web session)
- [x] Analyzed Ollama model capabilities (commit unknown - Web session)

### Session 2025-11-16 07:00 (CLI - Documentation Setup)
- [x] Created CLAUDE.md with comprehensive project guidance (pending commit)
- [x] Created TODO.md template (pending commit)
- [x] Analyzed Web session screenshot (in progress)

---

## 🐛 KNOWN ISSUES

### 1. Web session didn't commit work
**Severity:** Medium
**Discovered:** 2025-11-16
**Status:** Open

**Description:**
Research phase completed in Web but no code/docs committed to repo.

**Impact:**
Need to recreate research findings or extract from conversation.

**Workaround:**
Review screenshot and conversation history.

**Fix plan:**
Create follow-up prompt that emphasizes regular commits.

---

## 💡 FEATURE REQUESTS

### 1. Pattern-based project suggestions
**Requested:** 2025-11-16 (Original brief)
**Priority:** Medium
**Status:** Planned

**Description:**
Detect repeated manual tasks and suggest automation projects.

**Use case:**
"I manually process emails 3x/week" → Suggest email automation project

**Implementation notes:**
- Track frequency of pain points
- Cluster similar complaints
- Generate project briefs automatically

### 2. Confidence scoring
**Requested:** 2025-11-16 (Original brief)
**Priority:** High
**Status:** Planned

**Description:**
Rate confidence in each extracted item (0-100%).

**Use case:**
Help user prioritize review of discovered items.

**Implementation notes:**
- Explicit markers (TODO:) = high confidence
- Implicit mentions = lower confidence
- LLM can help score ambiguous cases

---

## 📊 SUMMARY

**Total Active Tasks:** 7
- High priority: 2
- Medium priority: 3
- Low priority: 2

**Total Completed This Session:** 3
**Total Open Issues:** 1
**Total Feature Requests:** 2

---

**Next Actions:**
1. Complete analysis of Web session work
2. Create comprehensive follow-up prompt for Web
3. Create reusable prompt templates for this handoff workflow
4. Commit all documentation to GitHub
5. Continue implementation in Web with proper commit discipline
