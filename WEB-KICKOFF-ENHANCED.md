# Claude Code for Web - Enhanced Kickoff Prompt

**Project:** conversation-analyzer → Web Kickoff for Projects (system-wide tool)
**Repository:** /home/tanya/Documents/Projects/conversation-analyzer
**GitHub:** https://github.com/TDProServices/conversation-analyzer
**Session Type:** Research, Analysis, Implementation, Quality Improvement
**Credit Budget:** Part of 48-hour $700 optimization

---

## 🎯 ENTRY PROMPT (Copy to Claude Code for Web)

```
Execute autonomous workflow for conversation-analyzer project using continuation protocol.

CRITICAL: Read these files IN ORDER before starting:
1. CLAUDE.md (all project requirements and workflows)
2. TODO.md (current state and task list)
3. COMPREHENSIVE-INSTRUCTIONS-RESPONSE.md (15 instruction points, research topics)
4. REUSABLE-PROMPTS.md (10 prompt templates, quality standards)
5. This file (WEB-KICKOFF-ENHANCED.md - execution protocol)

Then execute the work protocol defined below.
```

---

## 📋 PRE-FLIGHT VERIFICATION

**Before starting any work, verify:**

### Repository Verification
```bash
# Verify correct repo
pwd → /home/tanya/Documents/Projects/conversation-analyzer
git remote -v → https://github.com/TDProServices/conversation-analyzer.git

# Verify branch
git branch → master (or main)

# Check sync status
git status → should be clean or show only expected changes
```

### File Existence Check
**These files MUST exist (fail if missing):**
- [ ] CLAUDE.md (project guidance)
- [ ] TODO.md (task tracking)
- [ ] README.md (project overview)
- [ ] REUSABLE-PROMPTS.md (prompt templates)
- [ ] COMPREHENSIVE-INSTRUCTIONS-RESPONSE.md (requirements)
- [ ] WEB-SESSION-FOLLOWUP-PROMPT.md (previous Web prompt)

**If any file missing:** STOP and report to user

---

## 🔍 SESSION CONTEXT

### Previous Work Summary

**CLI Session (2025-11-16):**
- Created comprehensive documentation system
- Developed 10 reusable prompts (A+ quality)
- Analyzed Web session screenshot
- Received 15 comprehensive instruction points
- Created transcription relay system with critique

**Files Created (now in repo):**
1. CLAUDE.md - Complete project guidance
2. TODO.md - Task tracking
3. REUSABLE-PROMPTS.md - 10 prompt templates, rated and ranked
4. WEB-SESSION-FOLLOWUP-PROMPT.md - Original Web prompt
5. COMPREHENSIVE-INSTRUCTIONS-RESPONSE.md - 54KB of requirements/analysis
6. TRANSCRIPTION-RELAY-PROMPT.md - Speech cleanup system
7. TRANSCRIPTION-RELAY-CRITIQUE.md - Quality analysis (B+ → A+ path)

**Current State:**
- Documentation: ✅ Complete
- Research phase: ⚠️ Partially done (needs synthesis)
- Implementation: ❌ Not started
- Testing: ❌ Not started

---

## 📝 YOUR WORK ASSIGNMENTS

### Phase 1: Documentation Review & Improvement (2-3 hours)

**Tasks:**
1. **Read all documentation thoroughly**
   - CLAUDE.md, TODO.md, all instruction files
   - Take notes on contradictions, gaps, redundancies

2. **Critique existing docs**
   - Use "Beginner-Friendly Documentation Validator" (Prompt #7)
   - Apply A+ Prompt Rubric (from COMPREHENSIVE-INSTRUCTIONS-RESPONSE.md)
   - Score each document

3. **Improve documentation to A+ level**
   - Fix clarity issues
   - Add missing prerequisites
   - Improve examples
   - Ensure beginner-friendly language
   - Remove redundancies

4. **Commit improvements**
   ```bash
   git commit -m "$(cat <<'EOF'
   docs(quality): improve documentation to A+ level

   Applied Beginner-Friendly Documentation Validator and A+ Prompt Rubric:
   - [List specific improvements]
   - [Clarity enhancements]
   - [Prerequisites added]

   Scoring:
   - CLAUDE.md: [X/100] → [Y/100]
   - TODO.md: [X/100] → [Y/100]

   Author: Tanya Davis
   Organization: TD Professional Services LLC
   EOF
   )"
   ```

---

### Phase 2: Research & Tool Selection (4-6 hours)

**CRITICAL: This is your PRIMARY responsibility**

**User feedback:**
> "we have had a lot of issues with doing things the hard way (creating scripts when we don't need to, not using necessary tools like docker, treating the user as an expert when they are a beginner/novice)"

**Your mandate:** RESEARCH FIRST, BUILD LAST

#### 2.1 Core Technology Research

**Python Project Structure:**
- Research: pyproject.toml vs requirements.txt vs poetry vs hatch vs PDM
- Sources required: 3-5 (official docs, community best practices, expert opinions)
- Evaluate: beginner-friendliness, maintenance, industry adoption (2024-2025)
- **Decision:** Recommend ONE approach with detailed justification
- **Document:** Create RESEARCH.md with source citations

**Docker Evaluation:**
- Research: When to use Docker for Python development
- Evaluate: Complexity vs benefits for THIS project
- Sources: 3-5 diverse perspectives
- **Decision:** Use Docker? Yes/No with detailed justification
- **If Yes:** Provide beginner-friendly Dockerfile with comments explaining every line
- **If No:** Explain alternative (venv) with complete setup instructions

**Ollama Model Selection:**
- Research: qwen2.5:3b vs llama3.1:8b vs mistral for analysis tasks
- Test: Create sample prompts and compare outputs (if possible)
- Evaluate: Speed vs accuracy vs context window
- **Decision:** Primary model + fallback model
- **Document:** Model comparison with test results

#### 2.2 Existing Tools Research

**Conversation Analysis Tools:**
- Search: "conversation analysis llm python" (GitHub, PyPI, papers)
- Search: "todo extraction from text" (existing libraries)
- Search: "markdown parser python" (best libraries 2024-2025)
- **Requirement:** Find 5-10 tools, evaluate each
- **Apply:** Research-First Validator (Prompt #5) with 3-5 sources
- **Document:** Tools considered, why chosen/rejected

**Critical questions:**
- Does a tool already exist that does 80%+ of what we need?
- Can we compose multiple existing tools?
- Is building custom genuinely better, or are we reinventing the wheel?

#### 2.3 Research Documentation Requirements

**Create RESEARCH.md:**
```markdown
# Research Report - conversation-analyzer

## Technology Decisions

### Python Project Structure
**Decision:** [Chosen approach]
**Justification:** [Detailed reasoning]

**Sources:**
[Source 1] Official Python Packaging Guide
- URL: https://packaging.python.org/
- Date: 2024-11
- Perspective: Community best practices
- Recommends: [Tool X]
- Reliability: Very High

[Source 2] Real Python Tutorial
- URL: [...]
- Date: [...]
- Perspective: Educator, beginner-focused
- Recommends: [Tool Y]
- Reliability: High

[Source 3] [...]

**Analysis:**
- Agreement points: [...]
- Disagreements: [...]
- Truth/Best practice: [...]
- **Recommendation for THIS project:** [...]

### Docker Decision
[Same structure]

### Ollama Model Selection
[Same structure]

### Existing Tools Evaluation

**Tools Considered:**
1. **Tool Name** - [Brief description]
   - Pros: [...]
   - Cons: [...]
   - Meets needs: [X%]
   - Decision: [Use / Don't use]

2. [...]

**Final Tool Stack:**
- Markdown parsing: [Chosen tool]
- Ollama client: [Chosen library]
- Database: [SQLite with X library]
- CLI framework: [Click/Typer/argparse]
- Testing: [pytest + ...]
- Linting: [ruff + black + mypy]

**Justification:** [Why this stack]
```

**Commit research:**
```bash
git add RESEARCH.md
git commit -m "docs(research): comprehensive tool and technology research

Researched and evaluated:
- Python project structures (5 approaches compared)
- Docker necessity (3 perspectives analyzed)
- Ollama models (qwen2.5:3b vs llama3.1:8b vs mistral)
- 10 existing conversation analysis tools

Sources: 15 total (3-5 per decision)
All sources from 2023-2025, diverse perspectives

Recommendations:
- Project structure: [Choice] (beginner-friendly)
- Docker: [Yes/No] (justified)
- Ollama: [Model] primary, [Model] fallback
- Tool stack: [List]

Next: Implement based on these decisions

Author: Tanya Davis
Organization: TD Professional Services LLC"
```

---

### Phase 3: Project Setup (1-2 hours)

**Based on Phase 2 research, set up project:**

#### 3.1 Python Project Structure
```
conversation-analyzer/
├─ pyproject.toml (or requirements.txt, based on research)
├─ .gitignore (Python-specific)
├─ README.md (updated with setup instructions)
├─ src/
│  ├─ __init__.py
│  ├─ parser.py
│  ├─ ollama_client.py
│  ├─ extractor.py
│  ├─ database.py
│  └─ reporter.py
├─ tests/
│  ├─ __init__.py
│  ├─ test_parser.py
│  ├─ test_ollama.py
│  ├─ test_extractor.py
│  ├─ test_database.py
│  └─ test_reporter.py
├─ docs/
│  ├─ RESEARCH.md
│  ├─ ARCHITECTURE.md
│  └─ SETUP.md
└─ examples/
   ├─ sample_conversation.md
   └─ sample_output.md
```

#### 3.2 Configuration Files

**pyproject.toml (or equivalent):**
- Beginner-friendly comments explaining every section
- All dependencies listed with versions
- Development dependencies (testing, linting)
- Entry points for CLI

**.gitignore:**
```gitignore
# Python
__pycache__/
*.py[cod]
*.so
*.egg
*.egg-info/
dist/
build/
.venv/
venv/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Linting
.ruff_cache/
.mypy_cache/

# IDE
.vscode/
.idea/
*.swp

# Project-specific
results/
reports/
*.db
```

**Docker (if research says yes):**
```dockerfile
# Dockerfile with extensive comments explaining every line
FROM python:3.10-slim

# [Comment: Why this base image]
# [Comment: What this layer does]
# ... etc
```

#### 3.3 Linting Setup

**Create pyproject.toml sections or separate configs:**
```toml
[tool.ruff]
# Explain why these rules

[tool.black]
# Explain formatting choices

[tool.mypy]
# Explain type checking level
```

**Commit setup:**
```bash
git add .
git commit -m "chore(setup): initialize Python project structure

Based on research in RESEARCH.md:
- [Chosen structure] for project management
- [Docker/venv] for environment (justified in research)
- Linting: ruff + black + mypy
- Testing: pytest

Directory structure:
- src/ - Main code
- tests/ - Test suite
- docs/ - Documentation
- examples/ - Usage examples

All config files extensively commented for beginner-friendliness

Author: Tanya Davis
Organization: TD Professional Services LLC"
```

---

### Phase 4: Implementation (6-8 hours)

**Implement MVP using existing tools where possible**

#### 4.1 Parser Implementation
```python
# src/parser.py
"""
Conversation parser for Claude Code markdown exports.

Uses [Chosen library] based on research (see docs/RESEARCH.md).
Chosen because: [Reason from research]
"""

# Extensive comments explaining:
# - WHY this approach (not just what it does)
# - Edge cases handled
# - Assumptions made
# - Beginner-friendly explanations
```

**Commit after each component:**
```bash
git commit -m "feat(parser): add Claude conversation markdown parser

Implemented using [Library] (researched in RESEARCH.md):
- Parses user/assistant messages
- Extracts timestamps and metadata
- Handles code blocks and file references
- Edge cases: empty files, malformed markdown

Tested with sample conversation (examples/sample_conversation.md)
Performance: <1s for 100KB conversation

Why this library: [Reason from research]
Alternative considered: [X] (rejected because [Y])

Author: Tanya Davis
Organization: TD Professional Services LLC"
```

#### 4.2 Through 4.5 (Similar pattern for Ollama, Extractor, Database, Reporter)

**Each component:**
- Well-commented code (WHY, not just WHAT)
- Uses existing libraries where researched
- Handles errors gracefully with beginner-friendly messages
- Tested before committing
- Committed separately with detailed message

---

### Phase 5: Intelligence & Quality (4-6 hours)

#### 5.1 Refactoring
**CRITICAL:** Use Continuous Improvement Protocol (from COMPREHENSIVE-INSTRUCTIONS-RESPONSE.md)

**Process:**
1. Run all linters (ruff, black, mypy)
2. Fix all issues
3. Identify redundancies
4. Simplify complex code
5. Improve variable/function names
6. Add/improve comments (focus on WHY)
7. Document refactoring decisions

**Commit refactoring separately:**
```bash
git commit -m "refactor(code): apply continuous improvement protocol

Improvements:
- Reduced cyclomatic complexity in extract_todos() (was 15, now 8)
- Eliminated duplicate validation logic (DRY principle)
- Renamed ambiguous variables (X → descriptive_name)
- Added WHY comments to complex algorithms

Linting results:
- ruff: 0 issues (was 12)
- black: formatted (127 files changed)
- mypy: 0 type errors (was 5)

No functionality changed, only code quality improved

Author: Tanya Davis
Organization: TD Professional Services LLC"
```

#### 5.2 Redundancy Elimination

**Task:** Find and eliminate redundancies WITHOUT losing:
- Context
- Nuance
- Task tracking
- Feature documentation
- Bug reports
- Decision rationale

**Create REDUNDANCY-ANALYSIS.md:**
```markdown
# Redundancy Analysis

## Duplicates Found
1. **Function X duplicated in Y and Z**
   - Keep: Y (more complete implementation)
   - Remove: Z
   - Context preserved: Migrated comments to Y

2. **Documentation repeated in README and CLAUDE.md**
   - Keep: Detailed version in CLAUDE.md
   - README: Link to CLAUDE.md with brief summary
   - Why: Single source of truth, reduce maintenance

## Redundancies Preserved (Intentionally)
1. **Examples in both docs/ and examples/**
   - Keep both: Different audiences (readers vs runners)
   - Not true redundancy: Different formats

## Analysis Complete
- Code redundancy: Eliminated 15 duplicates
- Doc redundancy: Reduced by 40% via linking
- No context lost: All migrated or preserved
```

---

### Phase 6: Testing & Quality Assurance (2-3 hours)

#### 6.1 Real Data Testing

**Test with 3-5 real conversations:**
```bash
# From user's actual projects
test_files=(
  "/home/tanya/Documents/Projects/ai-audio-pipeline/.claude/session-X.md"
  "/home/tanya/Documents/Projects/ai-agents/planning-conversation.md"
  "/home/tanya/Documents/Projects/phone-issues/legal-discussion.md"
)

# Run analyzer on each
# Document results
```

**Create TEST-RESULTS.md:**
```markdown
# Test Results - Real Conversation Data

## Test 1: ai-audio-pipeline session
**File:** session-2025-11-15.md
**Size:** 150KB
**Processing time:** 1.2s

**TODOs Extracted:** 12
- True positives: 10 (83% accuracy)
- False positives: 2
- False negatives: 3 (missed)

**Accuracy:** 77% (below 85% target - needs improvement)

**Issues found:**
- Missed implicit TODOs ("we should probably...")
- False positive on rhetorical "we could..." statements

**Improvements needed:**
- Better context analysis for "could/should" statements
- Detect implicit TODOs better

[Similar for each test file]

## Overall Results
- **Accuracy:** 81% (target: 85%)
- **Performance:** <5min for all tests ✅
- **Offline:** 100% local ✅
- **Crashes:** 0 ✅

**Grade:** B+ (needs accuracy improvement to reach A)

## Improvement Plan
1. Refine LLM prompts for implicit TODO detection
2. Add context window for "could/should" disambiguation
3. Test again, target 85%+ accuracy
```

#### 6.2 Documentation for Beginners

**Update README.md:**
- Assume ZERO knowledge
- Step-by-step setup (every command explained)
- Troubleshooting section
- Examples that work out-of-the-box
- Prerequisites spelled out completely (including prerequisites of prerequisites)

**Apply Documentation Validator (Prompt #7):**
- All prerequisites listed (recursive)
- Nothing assumed
- OS-specific instructions
- Docker alternative (if complex)

---

### Phase 7: Session Analysis & Handoff (1-2 hours)

#### 7.1 Extract Session Insights

**Use Session Analysis Agent (Prompt #1):**

**Create SESSION-REPORT.md:**
```markdown
# Session Report - Web Implementation

## Work Completed
1. Documentation improved to A+ level
   - CLAUDE.md: 85 → 98/100
   - Added 15 missing prerequisites
   - Improved beginner-friendliness

2. Comprehensive research conducted
   - 15 sources evaluated
   - Tool selections documented
   - All decisions justified

3. Project set up with [Structure]
   - [Docker/venv] environment
   - Full linting configured
   - Tests scaffolded

4. MVP implemented
   - All 5 components complete
   - Tested with real data (81% accuracy)
   - Performance meets targets

5. Code quality improved
   - 0 linting errors
   - Redundancy reduced 40%
   - Refactored for clarity

## Decisions Made
1. **Project structure:** [Choice] because [Reason]
2. **Docker:** [Yes/No] because [Reason]
3. **Primary Ollama model:** [Model] because [Reason]
4. **Tool stack:** [List] because [Reason]

## Bugs Discovered
[List with severity]

## Features Requested
[Ideas that came up during work]

## Issues & Blockers
[Anything incomplete or problematic]

## Meta-Learnings
1. [Workflow insight]
2. [Tool lesson]
3. [Process improvement]

## GitHub Issues to Create
### Bugs
1. [Bug description] - Label: bug, Priority: High

### Features
1. [Feature idea] - Label: enhancement, Priority: Medium

### Technical Debt
1. [Debt item] - Label: technical-debt

## Next Steps
1. [Immediate priority]
2. [Follow-up work]
3. [Future enhancements]
```

#### 7.2 Update TODO.md

**Use TODO.md Synchronizer (Prompt #6):**
- Move completed tasks to ✅ with commit hashes
- Add new TODOs discovered
- Update priorities based on testing
- Add bugs to 🐛 section
- Add features to 💡 section

#### 7.3 Session Verification

**Use Session Verification (Prompt #10):**
- Git status clean?
- All commits pushed?
- All commits properly formatted?
- Documentation current?
- Tests passing?
- Lint errors: 0?

**Create verification checklist in SESSION-REPORT.md**

---

## 🤖 AUTONOMOUS EXECUTION PROTOCOL

### Work Methodology

**You are empowered to work autonomously following these rules:**

#### When to PROCEED without asking:
✅ Reading any file
✅ Researching tools/libraries
✅ Searching documentation
✅ Writing code (you'll commit it, user can review)
✅ Creating documentation
✅ Running linters/formatters
✅ Installing dependencies (document in requirements)
✅ Refactoring code (git is backup)
✅ Making implementation choices (document WHY)
✅ Creating test files
✅ Organizing files/directories

#### When to ASK the user:
❓ Requirements genuinely unclear (not just complex)
❓ Multiple valid architectural paths (can't decide which)
❓ Breaking existing functionality
❓ Major technology pivot (abandoning research findings)
❓ Stuck after exhausting all research/troubleshooting
❓ Budget/resource constraints

#### Decision Framework:
1. **Is it safe?** (no data loss, reversible) → Do it
2. **Is it in requirements?** (CLAUDE.md, TODO.md) → Do it
3. **Does research support it?** (RESEARCH.md) → Do it
4. **Is it unclear?** (genuinely ambiguous) → Ask
5. **Will user be surprised?** (unexpected direction) → Ask

---

## ✅ QUALITY CHECKLIST (Before Each Commit)

- [ ] **Code works** - Tested, no crashes
- [ ] **Existing tools used** - Researched, not reinvented
- [ ] **Beginner-friendly** - Comments explain WHY, not just WHAT
- [ ] **No redundancy** - DRY principle applied
- [ ] **Error messages helpful** - Actionable guidance
- [ ] **Documentation current** - README, comments match code
- [ ] **TODO.md updated** - Reflects current state
- [ ] **Linters pass** - ruff, black, mypy clean
- [ ] **Tests added** - If implementing feature
- [ ] **Commit message proper** - Conventional Commits + footer

---

## 📊 COMMIT REQUIREMENTS

**EVERY commit MUST:**

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body - detailed explanation of WHY>

<list major changes>
<note any decisions made>
<reference research if applicable>

Author: Tanya Davis
Organization: TD Professional Services LLC
EOF
)"
```

**Commit types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `refactor` - Code improvement (no functionality change)
- `test` - Tests
- `chore` - Maintenance (deps, config)
- `perf` - Performance improvement

**Commit frequency:**
- After each logical unit (30-60 min of work)
- After each component completed
- Before refactoring
- After research documented
- **NOT at end of session** - commit as you go!

**Push frequency:**
- After each commit (or every 2-3 commits max)
- Never accumulate >10 commits locally
- Keep remote in sync

---

## 🔬 RESEARCH PROTOCOL

**For EVERY major decision:**

### 1. Source Requirements
- **Minimum:** 3 sources
- **Maximum:** 5 sources
- **Recency:** 2023-2025 preferred
- **Diversity:** Different perspectives, all reliable

### 2. Source Types
Mix of:
- Official documentation (authoritative)
- Community best practices (practical)
- Expert analysis (nuanced)
- Real-world usage (validated)

### 3. Source Evaluation
For each source, note:
- **URL/Citation**
- **Date** (when published/updated)
- **Perspective** (what angle does it take)
- **Reliability** (Official? Community? Expert?)
- **Recommendation** (what does it suggest)
- **Bias** (any apparent bias)

### 4. Synthesis
- Agreement points across sources
- Disagreements and why
- Truth/best practice determination
- Recommendation for THIS project
- Justification (why this choice)

### 5. Documentation
All research goes in RESEARCH.md with proper citations

**Zotero Integration (to research):**
- How to integrate Zotero with markdown
- Best practices for technical citations
- Alternatives (if Zotero is overkill)

---

## 🎯 SUCCESS CRITERIA

### Session is successful when:
1. ✅ All documentation at A+ level
2. ✅ Comprehensive research documented (RESEARCH.md)
3. ✅ All decisions justified with 3-5 sources
4. ✅ Project structure set up (beginner-friendly)
5. ✅ MVP implemented using existing tools
6. ✅ Tested with 3-5 real conversations
7. ✅ Accuracy ≥85% on TODO extraction
8. ✅ All code linted (0 errors)
9. ✅ Redundancy eliminated (context preserved)
10. ✅ All commits properly formatted
11. ✅ TODO.md reflects current state
12. ✅ SESSION-REPORT.md created
13. ✅ GitHub issues suggested
14. ✅ Meta-learnings documented
15. ✅ Beginner can follow README to success

### Quality Standards:
- Code is maintainable by beginner
- Documentation assumes zero knowledge
- Error messages are actionable
- Examples work out-of-the-box
- Runs 100% offline (Ollama only)
- No unnecessary custom code

---

## 📈 CONTINUOUS IMPROVEMENT

### After Completing Work:

#### 1. Self-Critique
- Grade your work (A-F) on each success criterion
- Identify what could be better
- Document in SESSION-REPORT.md

#### 2. Refactor Pass
- Run Continuous Improvement Protocol
- Eliminate redundancy
- Simplify complex code
- Improve clarity

#### 3. Lint & Format
```bash
ruff check .
black .
mypy src/
```
Fix ALL issues, no exceptions

#### 4. Documentation Review
- Apply Documentation Validator (Prompt #7)
- Ensure beginner-friendliness
- Check prerequisites are complete

#### 5. Meta-Learning Extraction
Document in .meta/LEARNINGS.md:
- What worked well (repeat in future)
- What was challenging (avoid or improve)
- Tool choices (were they good?)
- Workflow improvements discovered

---

## 🚀 BEGIN WORK

**Your workflow:**

1. **Read all documentation** (CLAUDE.md, TODO.md, COMPREHENSIVE-INSTRUCTIONS-RESPONSE.md, REUSABLE-PROMPTS.md)

2. **Verify pre-flight** (all files exist, correct repo, clean git status)

3. **Start with Phase 1** (Documentation review & improvement)

4. **Move to Phase 2** (Research - your primary responsibility)

5. **Continue through phases** systematically

6. **Commit frequently** with proper format

7. **Update TODO.md** after each commit

8. **Work autonomously** using decision framework

9. **Ask only when genuinely needed**

10. **Complete with Session Report**

---

## 📚 REFERENCE: Reusable Prompts Available

**Use these throughout your work:**

1. **Session Analysis Agent** - Analyze previous work
2. **Project Context Consolidator** - Ensure context complete
3. **Follow-Up Prompt Generator** - Create next session prompt
4. **Commit Quality Auditor** - Review commits before pushing
5. **Research-First Validator** - Validate tool choices (3-5 sources)
6. **TODO.md Synchronizer** - Keep tracking accurate
7. **Beginner-Friendly Documentation Validator** - Check docs accessible
8. **Continuous Improvement Protocol** - Systematic refactoring
9. **Autonomous Execution Framework** - Decision-making guide (this doc)
10. **Session Verification** - Final quality check

**All prompts detailed in REUSABLE-PROMPTS.md**

---

## 💡 REMEMBER

**User's core feedback:**
- "doing things the hard way" → Research existing tools first
- "not using necessary tools like docker" → Evaluate Docker properly
- "treating user as expert when beginner/novice" → Beginner-friendly everything
- "creating scripts when we don't need to" → Use existing solutions

**Your mission:**
- RESEARCH before building
- USE existing tools (80% threshold)
- DOCUMENT for beginners
- COMMIT frequently
- WORK autonomously
- PRODUCE quality

**You've got this! Start with documentation review, then research. Quality over speed.**

---

**Created:** 2025-11-16
**For:** Claude Code for Web Autonomous Execution
**Based On:** REUSABLE-PROMPTS.md (Prompts #1-10) + COMPREHENSIVE-INSTRUCTIONS-RESPONSE.md (15 instruction points)
**Grade Target:** A+ (95-100 across all success criteria)
