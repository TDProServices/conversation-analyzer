# Claude Code for Web - Follow-Up Prompt: Conversation Analyzer

**Project:** conversation-analyzer
**Repository:** /home/tanya/Documents/Projects/conversation-analyzer
**GitHub:** https://github.com/TDProServices/conversation-analyzer
**Previous Session:** Research phase completed
**This Session:** Implementation and deployment

---

## 🎯 COPY THIS PROMPT INTO CLAUDE CODE FOR WEB

```
Continue the conversation-analyzer project implementation.

## SESSION CONTINUATION CONTEXT

### Previous Web Session Completed:
1. ✅ Researched existing conversation analysis tools
2. ✅ Evaluated TODO extraction approaches
3. ✅ Analyzed Ollama model capabilities for analysis tasks
4. ✅ Investigated prompt engineering techniques
5. ⚠️  Work was NOT committed to repository

### Current Repository State:
- README.md: Basic project description (committed)
- CLAUDE.md: Comprehensive project guidance (NOT YET committed - just created in CLI)
- TODO.md: Current task tracking (NOT YET committed - just created in CLI)
- REUSABLE-PROMPTS.md: 10 reusable prompt templates (NOT YET committed - just created in CLI)
- No code implementation yet
- Git configured with proper user.name and user.email

### What's Left to Complete:
1. Review and commit all new documentation files
2. Synthesize research findings into implementation decisions
3. Set up project structure (Python, dependencies, Docker if beneficial)
4. Implement MVP (parser, Ollama integration, extractor, reporter)
5. Add intelligence layer (deduplication, scoring, cross-referencing)
6. Test with real conversation data
7. Document setup and usage for beginners

---

## 📋 CRITICAL REQUIREMENTS - READ CAREFULLY

### YOU MUST READ THESE FILES FIRST (in the repo):
1. **CLAUDE.md** - Contains ALL project requirements and workflows
2. **TODO.md** - Current state and tasks to complete
3. **REUSABLE-PROMPTS.md** - Quality standards and processes

**IMPORTANT:** Everything you need is in CLAUDE.md. If something is unclear, check CLAUDE.md first.

---

## 🔍 Q&A FROM PREVIOUS SESSION

### Questions Asked by Web Session:
(Extract from screenshot if any - user to provide)

### User Answers:
(User to provide from screenshot analysis)

### Clarifications for This Session:

**Q: What level of technical expertise should I assume?**
A: Beginner/novice. Write documentation and error messages assuming minimal technical knowledge.

**Q: Should I use Docker?**
A: Research and evaluate. User feedback: "we have had issues... not using necessary tools like docker". If Docker simplifies deployment, use it.

**Q: Custom code or existing tools?**
A: ALWAYS research existing tools first. User feedback: "creating scripts when we don't need to". Only build custom if no existing tool meets 80%+ of need.

**Q: How often should I commit?**
A: After EVERY logical unit of work. Previous session didn't commit research - don't repeat that mistake.

**Q: What Ollama model should I use?**
A: Test and compare:
- qwen2.5:3b (fast, good for quick analysis)
- llama3.1:8b (better reasoning, slower)
- Document your testing and recommendation

---

## 📝 WORK TO COMPLETE

### Priority 1: Documentation & Setup
1. Review CLAUDE.md, TODO.md, REUSABLE-PROMPTS.md (just created)
2. Commit documentation with proper format
3. Update README.md with setup instructions
4. Create .gitignore for Python projects

**Success Criteria:**
- All docs committed and pushed to GitHub
- README has clear setup instructions for beginners
- Git status clean

### Priority 2: Project Structure
1. Research Python project structures (pyproject.toml vs requirements.txt vs poetry)
2. Set up dependencies (Ollama client, SQLite, markdown parser)
3. Evaluate Docker setup (research if it simplifies deployment)
4. Create src/ and tests/ directories
5. Add linting configuration (ruff, black, mypy)

**Success Criteria:**
- Can create virtual environment and install dependencies
- Linting runs successfully
- Structure documented in README

### Priority 3: MVP Implementation
1. **Conversation Parser:**
   - Research existing markdown parsers
   - Parse Claude conversation format (user/assistant messages)
   - Extract metadata (timestamps, file references)
   - Test with real conversation file

2. **Ollama Integration:**
   - Research Ollama Python clients
   - Implement connection with retry/timeout
   - Test different models (qwen2.5:3b vs llama3.1:8b)
   - Document performance comparison

3. **TODO Extractor:**
   - Design prompt templates for LLM
   - Implement extraction logic (regex + LLM validation)
   - Test on sample conversations
   - Measure accuracy

4. **SQLite Database:**
   - Design schema (items, sources, cross-refs)
   - Implement database operations
   - Add deduplication tracking

5. **Report Generator:**
   - Generate markdown reports
   - Include confidence scores
   - Add suggested actions
   - Test output format

**Success Criteria:**
- Can parse a conversation and extract TODOs
- Ollama integration works reliably
- Generates useful markdown report
- 85%+ accuracy on test conversations

### Priority 4: Intelligence Layer
1. Deduplication logic (>80% similarity detection)
2. Priority scoring algorithm
3. Cross-referencing system
4. Confidence scoring

**Success Criteria:**
- Duplicate TODOs are identified and merged
- Priority scores match manual evaluation
- Related items are linked

### Priority 5: Testing & Documentation
1. Test with 3-5 real conversations from `/home/tanya/Documents/Projects/`
2. Document setup process for beginners
3. Add usage examples to README
4. Create troubleshooting guide

**Success Criteria:**
- Works on real data
- Beginner can follow setup instructions
- Examples are clear and correct

---

## 🔧 COMMIT REQUIREMENTS

**YOU MUST commit frequently using this EXACT format:**

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<detailed body explaining WHY, not just WHAT>

<list major changes>

Author: Tanya Davis
Organization: TD Professional Services LLC
EOF
)"
```

**Commit types:** feat, fix, docs, refactor, test, chore

**Examples:**
- `feat(parser): add Claude conversation markdown parser`
- `fix(ollama): improve retry logic for connection timeouts`
- `docs(readme): add beginner setup instructions`
- `refactor(extractor): simplify TODO detection logic`

**CRITICAL:**
- ✅ Commit after each logical unit
- ✅ Push to GitHub after each commit
- ✅ Update TODO.md after each commit
- ❌ NEVER include "Co-Authored-By: Claude" or AI attribution
- ❌ NEVER batch commits at end (commit as you go!)

---

## 🤖 AUTONOMOUS EXECUTION PROTOCOL

You are empowered to work autonomously. Follow this framework:

### When to PROCEED without asking:
- Reading files (always safe)
- Searching/analyzing code
- Writing new files
- Installing dependencies (document in requirements)
- Testing code
- Creating documentation
- Refactoring code (git is backup)
- Choosing implementation details
- Selecting tools (after research)

### When to ASK the user:
- Requirements are ambiguous (genuinely unclear)
- Multiple valid architectural approaches
- Breaking changes to existing code
- Major technology decisions (unless researched thoroughly)
- Stuck after genuine research effort
- Budget/resource constraints

### Decision-Making Framework:
1. Is it safe? → Do it
2. Is it reversible (git)? → Do it
3. Is it in requirements (CLAUDE.md)? → Do it
4. Is it unclear? → Check TODO.md, then ask
5. Will it surprise user? → Ask

### Quality Checklist (before each commit):
- [ ] Works correctly (tested)?
- [ ] Used existing tools where possible (researched)?
- [ ] Documented for beginners (clear language)?
- [ ] Comments explain WHY, not just WHAT?
- [ ] No obvious redundancy?
- [ ] Error messages are helpful?
- [ ] TODO.md updated?

---

## 🔍 RESEARCH-FIRST MANDATE

**Before implementing ANY component:**

1. **Search for existing tools:**
   - pip search / PyPI.org
   - GitHub repositories
   - awesome-python lists
   - StackOverflow / Reddit

2. **Evaluate findings:**
   - Does it meet 80%+ of need?
   - Is it maintained?
   - Is it well-documented?
   - Can we compose multiple tools?

3. **Document research:**
   - What tools were considered
   - Why they were/weren't chosen
   - Add to comments or RESEARCH.md

4. **Only build custom when:**
   - No existing tool exists
   - Can't compose existing tools
   - Custom is genuinely faster/better
   - Building is explicitly required

**User feedback:** "we have had a lot of issues with doing things the hard way (creating scripts when we don't need to, not using necessary tools like docker)"

---

## 🎯 SUCCESS CRITERIA

### Session is successful when:
1. ✅ All documentation committed and pushed
2. ✅ Project structure set up and documented
3. ✅ MVP implemented and working
4. ✅ Tested with 3-5 real conversations
5. ✅ 85%+ accuracy on TODO extraction
6. ✅ Beginner can follow setup instructions
7. ✅ All commits follow proper format
8. ✅ TODO.md reflects current state
9. ✅ No blockers remaining
10. ✅ Ready for daily use

### Quality Standards:
- Code is maintainable by future-me
- Documentation assumes beginner/novice level
- Error messages include remediation steps
- Examples work out-of-the-box
- Runs completely offline (Ollama only)

---

## 📊 PROGRESS REPORTING

**In commit messages, include:**
- What was done and why
- What was tested
- What's next (if relevant)
- Any issues encountered

**Example commit message:**
```
feat(parser): add Claude conversation markdown parser

Implemented parser for Claude Code conversation exports:
- Extracts user/assistant messages
- Captures timestamps and metadata
- Handles code blocks and file references

Used existing library 'markdown-it-py' instead of custom parser
(researched alternatives: mistune, python-markdown, commonmark)

Tested with:
- Sample conversation from ai-audio-pipeline project
- Edge cases: empty messages, long code blocks
- Performance: 100KB conversation in <1s

Next: Integrate with Ollama for TODO extraction

Author: Tanya Davis
Organization: TD Professional Services LLC
```

---

## 🔄 CONTINUOUS IMPROVEMENT

**After completing implementation:**

1. **Review your work:**
   - What could be simpler?
   - Any redundancy to eliminate?
   - Is it beginner-friendly?
   - Used existing tools where possible?

2. **Self-critique:**
   - Grade yourself (A-F) on each quality criterion
   - Identify improvements needed
   - Document in TODO.md

3. **Prepare for refactor:**
   - Note: DON'T do major refactoring in this session
   - Instead: Document refactoring opportunities in TODO.md
   - We'll create a separate refactor session later

4. **Generate handoff:**
   - Use Session Verification prompt (from REUSABLE-PROMPTS.md)
   - Document what's done, what's left
   - Create next session prompt if needed

---

## 🚀 BEGIN WORK

**Start here:**
1. Read CLAUDE.md in the repo (contains all requirements)
2. Read TODO.md (current state and priorities)
3. Review this prompt one more time
4. Start with highest priority TODO
5. Commit frequently with proper format
6. Update TODO.md after each commit
7. Work autonomously using the framework above
8. Ask only when genuinely needed

**You've got this!** Work systematically, commit frequently, and use existing tools where possible.

Remember: Quality over speed. The goal is a tool that will be used daily, so maintainability and beginner-friendliness matter more than rushing.

---

**Good luck! Start with Priority 1 (commit the new docs).**
```

---

## USAGE NOTES

### For User (Tanya):
1. Copy everything from the ``` code block above
2. Paste into Claude Code for Web
3. Let Web work autonomously
4. Check back periodically (Web will commit/push regularly)
5. Web will ask questions only when genuinely needed

### Expected Timeline:
- Priority 1 (Docs): 30 minutes
- Priority 2 (Setup): 1-2 hours
- Priority 3 (MVP): 4-6 hours
- Priority 4 (Intelligence): 2-3 hours
- Priority 5 (Testing/Docs): 2-3 hours

**Total:** 9-14 hours of high-quality development (fits within $700 credit budget)

### What to Expect:
- Frequent commits (every 30-60 minutes)
- Regular TODO.md updates
- Questions only when truly needed
- Detailed commit messages
- Working MVP by end of session

---

**Created:** 2025-11-16
**For:** Conversation Analyzer Web Session Continuation
**Based on:** Reusable Prompt Templates (Prompt #3 + #9)
