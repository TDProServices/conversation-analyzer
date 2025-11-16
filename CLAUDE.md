# CLAUDE.md - Conversation Analyzer Project

**Last Updated:** 2025-11-16
**Project:** conversation-analyzer - Local LLM-powered conversation and file analysis system
**GitHub:** https://github.com/TDProServices/conversation-analyzer
**See also:** `/home/tanya/CLAUDE.md` (global guidance - all rules apply)

---

## Project Mission

Analyze Claude Code conversations, project files, and documentation to automatically extract:
- Missed TODOs and action items
- Bugs mentioned but not filed
- Feature requests discussed but not documented
- Patterns suggesting new projects or automation opportunities

**Privacy-First:** 100% local/offline using Ollama (no cloud APIs for sensitive legal/medical data)

---

## Critical Requirements

### ALL Global CLAUDE.md Rules Apply

This project MUST follow ALL requirements from `/home/tanya/CLAUDE.md`, especially:

1. **Use Existing Tools First** - Research before building, compose tools, avoid reinventing wheel
2. **Hierarchical Numbering** - Use 1.1, 1.2, 2.1 format (never restart mid-session)
3. **Task Tracking** - Maintain TODO.md, update after every change
4. **Conventional Commits** - Include proper footer, no AI co-author attribution
5. **Directory Discipline** - Never change directories without permission
6. **Background Task Tracking** - Record ID, report status, remediate failures
7. **Execution-First** - Do safe operations immediately, don't just describe
8. **Session Verification** - Provide comprehensive checkpoints when requested

**If there's a conflict, `/home/tanya/CLAUDE.md` takes precedence.**

---

## Project-Specific Guidance

### Research-First Development

**MANDATORY:** Before building ANY component:

1. **Search for existing tools** (2024-2025):
   - Conversation analysis frameworks
   - TODO extraction libraries
   - LLM-based code analysis tools
   - Ollama integration examples
   - Document parsers (markdown, code)

2. **Evaluate options**:
   - Does it meet 80%+ of need?
   - Can we compose multiple tools?
   - Is it maintained and documented?

3. **Only build custom when**:
   - No existing tool exists
   - Can't compose existing tools
   - Building is genuinely faster/better

**User feedback:** "we have had a lot of issues with doing things the hard way (creating scripts when we don't need to, not using necessary tools like docker, treating the user as an expert when they are a beginner/novice)"

### Work Smarter, Not Harder

**Anti-patterns to avoid:**
- ❌ Custom scripts when existing tools work
- ❌ Assuming user is expert (they're beginner/novice)
- ❌ Skipping Docker when it simplifies deployment
- ❌ Overcomplicating solutions
- ❌ Building from scratch before researching

**Correct patterns:**
- ✅ Use pip/apt installable tools
- ✅ Docker for reproducible environments
- ✅ Simple, maintainable code
- ✅ Clear documentation for beginners
- ✅ Compose existing tools creatively

### Technology Constraints

**Required:**
- **LLM:** Ollama (http://localhost:11434) - MUST be local/offline
- **Models:** qwen2.5:3b (fast), llama3.1:8b (better reasoning), mistral, codellama
- **Language:** Python 3.10+ (user preference)
- **Storage:** SQLite (structured data) + Markdown (reports)
- **Search:** Ripgrep (fast file scanning)

**Consider:**
- **Docker:** For consistent environment (user wants this evaluated)
- **Existing libraries:** For parsing, NLP, data validation
- **CLI frameworks:** Click, Typer, argparse

### User Experience Level

**Assume beginner/novice:**
- Clear error messages with remediation steps
- Examples in documentation
- Setup instructions that work first time
- No assumed knowledge of tools
- Comments explaining WHY, not just WHAT

### Commit Requirements

**Every commit MUST include:**

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<detailed body explaining WHY>

Author: Tanya Davis
Organization: TD Professional Services LLC
EOF
)"
```

**Commit frequently:**
- After implementing each feature
- After fixing each bug
- After adding documentation
- Before refactoring
- Push to GitHub regularly

**Types:**
- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code improvement
- test: Tests
- chore: Maintenance

**NEVER include:** "Co-Authored-By: Claude" or AI attribution

---

## Analysis Targets

**What to scan:**
1. Claude Code conversation exports (markdown)
2. TODO.md and TASKS.md files across repos
3. Code comments (TODO, FIXME, HACK, XXX, NOTE)
4. Git commit messages (WIP, TODO markers)
5. Documentation files (README.md, docs/)
6. Session summaries and planning docs

**Where to scan:**
- `/home/tanya/Documents/Projects/` (20+ repositories)
- `.claude/` directories in projects (CLI sessions)
- `COMPREHENSIVE-*.md` planning docs
- `SESSION-*.md` summaries

---

## Extraction Categories

### TODOs/Action Items
- **Explicit:** "I need to...", "We should...", "TODO:"
- **Implicit:** Problems stated without solutions
- **Commitments:** "I'll do X", "Let me Y"
- **Follow-ups:** "I'll get back to you on..."

### Bugs/Issues
- **Explicit:** "This is broken", "Error when..."
- **Workarounds:** "For now we manually...", "Temporary fix..."
- **Known limitations:** "This doesn't handle..."
- **Performance:** "This is slow", "Memory leak..."

### Feature Requests
- **Explicit:** "We should add...", "It would be nice if..."
- **User needs:** "I need a way to..."
- **Improvements:** "This could be better by..."

### Potential Projects
- Repeated manual tasks (automation opportunities)
- Tool gaps: "We need a tool to..."
- Pain points mentioned 3+ times
- "We should build..." statements

---

## Output Requirements

### Daily Reports (Markdown)
```markdown
## Analysis Report - YYYY-MM-DD

### 🔴 High Priority TODOs (X)
1. **repo-name:** Task description
   - Severity: High/Medium/Low
   - Source: file.md:line
   - Context: "quote from conversation"
   - Mentioned: Nx
   - Existing TODO: ✅ / ❌
   - Confidence: XX%
   - Suggested action: Add to TODO.md under "Priority"

### 📊 Statistics
- Conversations analyzed: X
- TODOs found: X
- Bugs found: X
- Duplicates: X
- Processing time: X.Xs
```

### Structured Database (SQLite)
- Items table (id, type, description, source, confidence, created_at)
- Sources table (file_path, line_number, context)
- Deduplication tracking
- Cross-references

---

## Intelligence Features

**Deduplication:**
- Same TODO if: >80% similar description, same repo/file, within 7 days
- Handle variations: "fix bug" vs "fix the bug" vs "we need to fix bug"

**Priority Scoring:**
- Urgency words: "critical", "urgent", "asap", "blocking"
- Impact words: "broken", "crash", "fails", "security"
- Frequency: Multiple mentions = higher priority
- Recency: Recent mentions = higher priority
- Context: Legal/medical = higher priority

**Cross-referencing:**
- Link related items across conversations
- Track patterns (same issue in multiple projects)
- Suggest consolidation opportunities

---

## Development Workflow

### Phase 1: Research (MANDATORY - Don't Skip!)
1. Search for existing conversation analysis tools
2. Review LLM-based code analysis frameworks
3. Find TODO extraction libraries/tools
4. Evaluate Ollama models for this task
5. Research prompt engineering for extraction
6. **Present findings before building**

### Phase 2: Design
1. Architecture diagram (data flow)
2. Database schema (tables, relationships)
3. LLM prompt templates for each analysis type
4. File scanning strategy (what to scan, what to ignore)
5. Deduplication algorithm
6. Priority scoring methodology

### Phase 3: MVP Implementation
1. Conversation parser (Claude markdown format)
2. File scanner (ripgrep integration)
3. Ollama client (retry/timeout handling)
4. Basic TODO extractor (regex + LLM validation)
5. SQLite database setup
6. Simple markdown report generator

### Phase 4: Intelligence Layer
1. Deduplication logic
2. Cross-referencing system
3. Priority scoring
4. Project pattern detection
5. Confidence scoring

### Phase 5: Integration
1. Batch processing scripts
2. Daily report automation
3. TODO.md update suggestions
4. GitHub issue creation (optional)

---

## Testing & Quality

**Test with real data:**
- Use actual Claude conversations from `/home/tanya/Documents/Projects/`
- Test on ai-audio-pipeline, ai-agents, phone-issues repos
- Measure accuracy (target: 85%+ for TODO extraction)

**Measure performance:**
- Processing time for typical conversation (target: < 5 minutes)
- Deduplication accuracy
- False positive rate

**Validate output:**
- Reports should be immediately useful
- Confidence scores should be realistic
- Suggested actions should be specific

---

## Success Criteria

1. ✅ Can analyze a Claude conversation and extract TODOs with 85%+ accuracy
2. ✅ Deduplicates across multiple conversations
3. ✅ Generates useful daily reports in under 5 minutes
4. ✅ Runs completely offline with Ollama
5. ✅ Easy to add new analysis types
6. ✅ Clear documentation for future maintenance

---

## Continuous Improvement Protocol

**After completing any significant work:**

1. **Review & Critique:**
   - What worked well?
   - What could be simpler?
   - Are we using existing tools where we could?
   - Is the code maintainable for a beginner?
   - Is documentation clear?

2. **Refactor:**
   - Eliminate redundancy
   - Simplify complex logic
   - Improve variable/function names
   - Add comments for WHY

3. **Lint & Format:**
   - Run linters (ruff, black, mypy for Python)
   - Fix all warnings
   - Ensure consistent style

4. **Document:**
   - Update TODO.md with completed tasks
   - Add examples to README
   - Document any gotchas
   - Note future improvements

5. **Commit & Push:**
   - Use Conventional Commits format
   - Include detailed body
   - Push to GitHub

**Note:** For major refactoring, consider creating a second Web session with a focused prompt.

---

## Known Anti-Patterns from Previous Work

Based on user feedback, avoid:

1. **Building custom parsers** - Look for existing markdown/code parsers first
2. **Assuming expertise** - Write docs for beginners
3. **Skipping Docker** - Evaluate if it simplifies setup
4. **Overcomplicating** - Simple working code > clever complex code
5. **Not researching** - Always search before building

---

## Quick Reference

**Ollama:**
```bash
# Check available models
ollama list

# Test model
ollama run qwen2.5:3b "Extract TODOs from this text: I need to fix the bug and add tests"

# API endpoint
curl http://localhost:11434/api/generate -d '{"model": "qwen2.5:3b", "prompt": "text"}'
```

**Project locations:**
- ai-audio-pipeline: `/home/tanya/Documents/Projects/ai-audio-pipeline/`
- ai-agents: `/home/tanya/Documents/Projects/ai-agents/`
- phone-issues: `/home/tanya/Documents/Projects/phone-issues/`
- medical: `/home/tanya/Documents/Projects/medical/`

**Templates:**
- TODO.md: `/home/tanya/Templates/TODO.md`
- Commit format: `/home/tanya/Documents/Projects/computer-setup/llm-workflows/prompts/commit-with-proper-format.md`

---

**For detailed global guidance, see `/home/tanya/CLAUDE.md`**
