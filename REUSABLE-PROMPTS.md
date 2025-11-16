# Reusable Prompts & Agents for CLI-to-Web Handoff Workflow

**Created:** 2025-11-16
**Purpose:** Make the CLI → Claude Code for Web handoff process repeatable and systematic
**Use Case:** When CLI session needs to hand off work to Web session for intensive development

---

## Overview

This document contains 10 specialized, reusable prompts/agent templates for systematically:
1. Analyzing ongoing work in CLI
2. Preparing comprehensive handoff documentation
3. Ensuring Web session has all context needed
4. Maintaining commit discipline and quality standards
5. Enabling autonomous Web execution
6. Creating feedback loops for continuous improvement

**Goal:** Repeatable, high-quality handoffs that maximize $700 credit value over 48 hours.

---

## Prompt Template Structure

Each prompt follows this format:
```
## [ID] Prompt Name
**Purpose:** What this prompt accomplishes
**When to Use:** Triggering conditions
**Input Requirements:** What you need before using
**Output:** What it produces
**Template:** The actual prompt to use
```

---

## 1️⃣ SESSION ANALYSIS & EXTRACTION AGENT

**Purpose:** Analyze a Web session screenshot/conversation and extract all critical information

**When to Use:**
- After Web session completes work
- Before creating follow-up prompts
- When Web session ran out of context
- Need to understand what was accomplished

**Input Requirements:**
- Screenshot(s) of Web session
- Path to project repository
- Original session prompt (if available)

**Output:**
- List of all work completed
- Questions asked by Web session and answers
- Decisions made
- Code/files created
- Remaining TODOs
- Issues encountered

**Template:**
```
Analyze this Claude Code for Web session screenshot and extract comprehensive information.

PROJECT: [repo path or name]
SCREENSHOT: [path to screenshot file]

EXTRACT THE FOLLOWING:

1. WORK COMPLETED:
   - What files were created/modified?
   - What research was conducted?
   - What decisions were made?
   - What was implemented?

2. QUESTIONS & ANSWERS:
   - List every question the Web session asked
   - Document the user's answers
   - Note any unresolved questions

3. REMAINING WORK:
   - What TODOs are left?
   - What was started but not finished?
   - What's blocked and why?

4. ISSUES & BLOCKERS:
   - What errors occurred?
   - What problems were encountered?
   - What needs fixing before continuing?

5. COMMITS & GITHUB:
   - What was committed?
   - What wasn't committed but should be?
   - Is repo synced with GitHub?

6. CRITIQUE:
   - What could have been done better?
   - Was existing tools research done properly?
   - Were commits made frequently enough?
   - Is documentation clear for beginners?

OUTPUT FORMAT:
- Structured markdown with hierarchical numbering
- Include file paths and line numbers
- Link related items
- Provide remediation steps for issues
```

---

## 2️⃣ PROJECT CONTEXT CONSOLIDATOR

**Purpose:** Ensure project has ALL necessary context files for Web session to work autonomously

**When to Use:**
- Before starting any Web session
- When Web session says "I don't have access to X"
- Handoff between CLI and Web

**Input Requirements:**
- Project repository path
- Global CLAUDE.md location
- Relevant templates and SOPs

**Output:**
- Updated project CLAUDE.md with all guidance
- Project TODO.md with current state
- Any missing templates/docs copied into repo

**Template:**
```
Prepare [PROJECT NAME] repository for autonomous Claude Code for Web session.

REPOSITORY: [path to repo]
GLOBAL GUIDANCE: /home/tanya/CLAUDE.md
TEMPLATES: /home/tanya/Templates/

TASKS:

1. CREATE/UPDATE CLAUDE.md in project root:
   - Copy ALL relevant sections from /home/tanya/CLAUDE.md
   - Add project-specific guidance
   - Include technology constraints
   - Document user's experience level (beginner/novice)
   - Add commit template and requirements
   - List analysis targets specific to project
   - Include success criteria

2. CREATE/UPDATE TODO.md in project root:
   - Use template from /home/tanya/Templates/TODO.md
   - Document current state (what's done, what's pending)
   - Include all known issues
   - List feature requests
   - Add commit hashes for completed work

3. VERIFY CONTEXT FILES:
   - Check if README.md exists and is current
   - Ensure .gitignore is appropriate
   - Verify git config (user.name, user.email)
   - Check if repo is synced with GitHub

4. COPY ESSENTIAL REFERENCES:
   - Commit format examples
   - Relevant workflow docs
   - Any project-specific templates

OUTPUT:
- List of files created/updated
- Confirmation that Web session has all context
- Any warnings about missing information
```

---

## 3️⃣ FOLLOW-UP PROMPT GENERATOR

**Purpose:** Generate comprehensive, context-rich prompts for Web session continuation

**When to Use:**
- After analyzing Web session work
- Ready to hand off to Web for next phase
- Need Web to work autonomously

**Input Requirements:**
- Analysis from Prompt #1 (Session Analysis)
- Context from Prompt #2 (Project Context)
- Current TODO.md and CLAUDE.md

**Output:**
- Complete prompt ready to paste into Web
- Includes all context, requirements, and expectations
- Embeds Q&A from previous session
- Clear autonomous execution guidelines

**Template:**
```
Generate a comprehensive follow-up prompt for Claude Code for Web continuation.

PROJECT: [name]
PREVIOUS WORK: [summary from Session Analysis]
CURRENT STATE: [from TODO.md analysis]

CREATE PROMPT WITH THESE SECTIONS:

## PROMPT STRUCTURE:

### 1. Session Continuation Context
- What was done in previous session
- What's left to complete
- Current state of repo

### 2. Q&A from Previous Session
- List all questions asked
- Document all answers provided
- Clarify any ambiguities

### 3. Work to Complete
- Specific tasks (from TODO.md)
- Priority order
- Success criteria for each

### 4. Critical Requirements
- MUST follow CLAUDE.md (in repo)
- MUST commit frequently with proper format
- MUST use existing tools (research first)
- MUST document for beginners
- MUST ask questions if stuck (don't assume)

### 5. Commit Template
```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body>

Author: Tanya Davis
Organization: TD Professional Services LLC
EOF
)"
```

### 6. Quality Checklist
Before each commit:
- [ ] Used existing tools where possible?
- [ ] Documented for beginner level?
- [ ] Included WHY in comments?
- [ ] Tested the code?
- [ ] Updated TODO.md?

### 7. Autonomous Execution Protocol
- Work through TODOs systematically
- Commit after each logical unit
- Update TODO.md after each commit
- Push to GitHub regularly
- If blocked, document in TODO.md and ask user
- Regular progress updates in commits

### 8. Continuous Improvement
After completing work:
- Review and critique your code
- Identify redundancies
- Simplify where possible
- Ensure beginner-friendly
- Prepare for lint/refactor pass

OUTPUT FORMAT:
Complete prompt text ready to copy-paste into Claude Code for Web.
```

---

## 4️⃣ COMMIT QUALITY AUDITOR

**Purpose:** Review commits before pushing to ensure quality and compliance

**When to Use:**
- Before pushing to GitHub
- After completing significant work
- During session verification
- Before handoff to another session

**Input Requirements:**
- Repository path
- Number of recent commits to review (default: 10)

**Output:**
- Compliance report (pass/fail for each requirement)
- List of commits needing fixes
- Specific remediation steps

**Template:**
```
Audit recent Git commits for quality and compliance.

REPOSITORY: [path]
COMMITS TO REVIEW: [last N commits, default 10]

CHECK EACH COMMIT FOR:

1. CONVENTIONAL COMMITS FORMAT:
   - [ ] Has type (feat, fix, docs, refactor, test, chore, etc.)
   - [ ] Has scope (optional but recommended)
   - [ ] Subject line: present tense, imperative mood
   - [ ] Subject < 72 characters

2. COMMIT BODY:
   - [ ] Explains WHY, not just WHAT
   - [ ] Provides context
   - [ ] References issues/files if relevant
   - [ ] Clear and detailed

3. ATTRIBUTION:
   - [ ] Includes footer: "Author: Tanya Davis"
   - [ ] Includes footer: "Organization: TD Professional Services LLC"
   - [ ] NO "Co-Authored-By: Claude" or AI attribution

4. COMMIT LOGIC:
   - [ ] One logical change per commit
   - [ ] Not mixing unrelated changes
   - [ ] Reasonable size (not too large)

5. COMMIT MESSAGE QUALITY:
   - [ ] Clear and descriptive
   - [ ] Easy to understand
   - [ ] Helpful for future reference

OUTPUT FORMAT:

## Commit Audit Report - [DATE]

### ✅ PASSING COMMITS (X/Y)
[List commits that pass all checks]

### ❌ FAILING COMMITS (X/Y)
[For each failing commit, list:]
- Commit hash
- What's wrong
- How to fix

### 📊 SUMMARY
- Compliance rate: X%
- Most common issues:
  1. [issue]
  2. [issue]

### 🔧 REMEDIATION
[If any commits fail:]
```bash
# Commands to fix commits
git rebase -i HEAD~N
# [specific instructions]
```
```

---

## 5️⃣ RESEARCH-FIRST VALIDATOR

**Purpose:** Ensure proper research was done before building custom solutions

**When to Use:**
- Before implementing new features
- When about to write custom code
- During code review
- Before committing implementation work

**Input Requirements:**
- Description of what's being built
- Project domain/technology
- Repository path (to check for research docs)

**Output:**
- Research completeness score
- List of tools/frameworks that should have been considered
- Recommendations for existing tools
- Approval/rejection to proceed with custom build

**Template:**
```
Validate that proper research was conducted before building custom solution.

FEATURE/COMPONENT: [what's being built]
TECHNOLOGY DOMAIN: [e.g., "conversation parsing", "LLM integration", "CLI tools"]
REPOSITORY: [path to check for research docs]

RESEARCH VALIDATION CHECKLIST:

1. DOCUMENTATION CHECK:
   - [ ] Is there a RESEARCH.md or similar file?
   - [ ] Does it list existing tools considered?
   - [ ] Does it explain why existing tools won't work?

2. EXISTING TOOLS SEARCH:
   - [ ] apt/pip/npm packages searched?
   - [ ] GitHub repositories reviewed?
   - [ ] Documentation sites checked?
   - [ ] Stack Overflow / Reddit / forums consulted?

3. EVALUATION CRITERIA:
   - [ ] Tools rated against requirements (80%+ threshold)?
   - [ ] Composition of multiple tools considered?
   - [ ] Installation complexity vs build complexity compared?
   - [ ] Maintenance burden evaluated?

4. JUSTIFICATION FOR CUSTOM BUILD:
   - [ ] No existing tool meets need?
   - [ ] Can't compose existing tools?
   - [ ] Custom genuinely faster/better?
   - [ ] User explicitly requested custom?

PERFORM RESEARCH (if not done):

Search for: [domain] + "python library"
Search for: [domain] + "CLI tool"
Search for: [domain] + "open source"
Check: awesome-[domain] lists on GitHub

PROVIDE:
1. List of 5-10 existing tools that could work
2. Evaluation of each (pros/cons)
3. Recommendation: Use existing vs Build custom
4. If building custom, explain why it's justified

OUTPUT FORMAT:

## Research Validation Report

### Research Status: [COMPLETE / INCOMPLETE / MISSING]

### Existing Tools Found:
1. [tool name] - [description] - [pros/cons] - [80%+ match? Y/N]
2. [tool name] - [description] - [pros/cons] - [80%+ match? Y/N]
...

### Recommendation:
[Use existing tool X] OR [Build custom because...]

### Approval: [APPROVED / REJECTED / NEEDS MORE RESEARCH]
```

---

## 6️⃣ TODO.md SYNCHRONIZER

**Purpose:** Keep TODO.md in perfect sync with actual work state

**When to Use:**
- After completing each task
- After each commit
- Before and after each session
- During session verification

**Input Requirements:**
- Project repository path
- Recent git commits
- Current TODO.md content

**Output:**
- Updated TODO.md
- Move completed items to ✅ section
- Add any new issues/todos discovered
- Ensure commit hashes are included

**Template:**
```
Synchronize TODO.md with actual project state.

REPOSITORY: [path]
COMMITS SINCE LAST UPDATE: [git log --oneline --since="X hours ago"]

TASKS:

1. REVIEW RECENT COMMITS:
   - Extract what was accomplished
   - Identify completed TODO items
   - Note any new TODOs mentioned in commits
   - Find any bugs/issues mentioned

2. UPDATE TODO.md:

   Move to ✅ COMPLETED:
   - Match commit subjects to TODO items
   - Add commit hash next to each completed item
   - Group by session with timestamp

   Add to 🐛 KNOWN ISSUES:
   - Extract from commit messages
   - Note severity and status
   - Document workarounds if any

   Add to ACTIVE SECTIONS:
   - Any new TODOs from commits
   - Proper priority (High/Medium/Low)
   - Clear action items

3. VERIFY ACCURACY:
   - Every recent commit reflected in TODO.md?
   - Priorities still correct?
   - Blockers clearly marked?
   - Summary stats updated?

4. UPDATE METADATA:
   - Last Updated timestamp
   - Summary section counts
   - Next Actions list

OUTPUT:
- Updated TODO.md content
- Summary of changes made
```

---

## 7️⃣ BEGINNER-FRIENDLY DOCUMENTATION VALIDATOR

**Purpose:** Ensure all documentation is clear for beginner/novice users

**When to Use:**
- After writing documentation
- Before committing README/guides
- During code review
- When user says "I don't understand X"

**Input Requirements:**
- Documentation file(s) to review
- Target user level (beginner/novice)

**Output:**
- Readability score
- List of improvements needed
- Rewritten sections (if requested)

**Template:**
```
Validate documentation for beginner/novice accessibility.

FILES TO REVIEW: [list of markdown/doc files]
TARGET AUDIENCE: Beginner/Novice (assumes minimal technical knowledge)

EVALUATION CRITERIA:

1. CLARITY:
   - [ ] No unexplained jargon?
   - [ ] Technical terms defined when first used?
   - [ ] Clear, simple language?
   - [ ] Short sentences and paragraphs?

2. COMPLETENESS:
   - [ ] All steps included (no assumed steps)?
   - [ ] Prerequisites listed?
   - [ ] Example commands copy-pasteable?
   - [ ] Expected output shown?

3. ORGANIZATION:
   - [ ] Logical flow (simple → complex)?
   - [ ] Clear headings and structure?
   - [ ] Table of contents for long docs?
   - [ ] Quick start section?

4. EXAMPLES:
   - [ ] Real, working examples?
   - [ ] Common use cases covered?
   - [ ] Troubleshooting section?
   - [ ] "What if X goes wrong" addressed?

5. BEGINNER PITFALLS:
   - [ ] Path assumptions explained (relative vs absolute)?
   - [ ] Environment setup clearly documented?
   - [ ] Error messages explained?
   - [ ] "Why am I doing this" answered?

REVIEW EACH SECTION:

For each technical term/command/concept:
- Is it explained?
- Is there an example?
- Is the purpose clear?
- Could a beginner follow this?

OUTPUT FORMAT:

## Documentation Review

### Overall Score: [X/10]
- Clarity: [X/10]
- Completeness: [X/10]
- Organization: [X/10]
- Examples: [X/10]
- Beginner-Friendly: [X/10]

### Issues Found:
[Hierarchically numbered list]
1. Section "X":
   1.1 Problem: [what's unclear]
   1.2 Fix: [how to improve]

### Recommendations:
[Specific improvements needed]

### Approval: [APPROVED / NEEDS REVISION]
```

---

## 8️⃣ CONTINUOUS IMPROVEMENT PROTOCOL

**Purpose:** Systematic review, critique, and improvement of completed work

**When to Use:**
- After completing major features
- Before declaring work "done"
- Preparing for lint/refactor pass
- End of sprint/session

**Input Requirements:**
- Repository path
- Code/docs to review
- Original requirements/goals

**Output:**
- Critique report
- Refactoring recommendations
- List of redundancies to eliminate
- Quality improvement action items

**Template:**
```
Execute continuous improvement review on completed work.

PROJECT: [name]
REPOSITORY: [path]
WORK COMPLETED: [description or commit range]

SYSTEMATIC REVIEW:

1. FUNCTIONALITY REVIEW:
   - [ ] Does it work as intended?
   - [ ] All requirements met?
   - [ ] Edge cases handled?
   - [ ] Error handling robust?

2. CODE QUALITY:
   - [ ] DRY (Don't Repeat Yourself) - any redundancy?
   - [ ] KISS (Keep It Simple) - any overcomplexity?
   - [ ] Clear variable/function names?
   - [ ] Appropriate comments (WHY, not WHAT)?

3. EXISTING TOOLS CHECK:
   - [ ] Could we use existing library instead?
   - [ ] Are we reinventing the wheel anywhere?
   - [ ] Could tools be composed better?

4. BEGINNER-FRIENDLINESS:
   - [ ] Clear error messages?
   - [ ] Documentation understandable?
   - [ ] Examples provided?
   - [ ] Setup process simple?

5. MAINTAINABILITY:
   - [ ] Future-you can understand this?
   - [ ] Easy to modify/extend?
   - [ ] Tests exist (if applicable)?
   - [ ] Dependencies documented?

IDENTIFY IMPROVEMENTS:

For each file/component:
- What works well? (keep doing)
- What could be simpler? (refactor)
- What's redundant? (eliminate)
- What's missing? (add)

OUTPUT FORMAT:

## Continuous Improvement Report

### ✅ What Works Well
[Keep these patterns]

### 🔄 Refactoring Opportunities
1. [Location]:
   - Current state: [description]
   - Issue: [why it needs improvement]
   - Suggested fix: [how to improve]
   - Impact: [effort vs benefit]

### ❌ Redundancies to Eliminate
[List duplicate code, repeated logic, etc.]

### ➕ Missing Elements
[Features, tests, docs, error handling]

### 📋 Action Items
[Prioritized list of improvements]
1.1 High priority
1.2 Medium priority
1.3 Low priority

### 🎯 Next Steps
[Immediate actions to take]
```

---

## 9️⃣ WEB SESSION AUTONOMOUS EXECUTION FRAMEWORK

**Purpose:** Provide Web session with complete framework for autonomous work

**When to Use:**
- Starting any new Web session
- Web session needs clarification on how to work
- Handoff from CLI to Web
- User wants Web to work independently

**Input Requirements:**
- Project context (CLAUDE.md, TODO.md)
- Work to be done
- Success criteria

**Output:**
- Complete autonomous execution instructions
- Decision-making framework
- When to ask vs when to proceed
- Commit discipline guidelines

**Template:**
```
AUTONOMOUS EXECUTION FRAMEWORK for Claude Code for Web

PROJECT: [name]
SESSION GOAL: [high-level objective]

READ FIRST:
- CLAUDE.md in repo (contains ALL critical requirements)
- TODO.md in repo (current state and work to do)
- README.md (project context)

AUTONOMOUS WORK PROTOCOL:

1. WORK SYSTEMATICALLY:
   - Start with highest priority TODO
   - Complete one logical unit at a time
   - Don't jump between unrelated tasks
   - Finish before moving to next

2. RESEARCH BEFORE BUILDING:
   For ANY new component:
   a) Search for existing tools (pip, apt, GitHub)
   b) Evaluate if they meet 80%+ of need
   c) Only build custom if justified
   d) Document research in comments/docs

3. COMMIT DISCIPLINE:
   After each logical unit:
   ```bash
   # Stage relevant files
   git add [files]

   # Commit with proper format
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <subject>

   <detailed body explaining WHY>

   Author: Tanya Davis
   Organization: TD Professional Services LLC
   EOF
   )"

   # Push to GitHub
   git push origin main
   ```

4. UPDATE TODO.md:
   After each commit:
   - Move completed items to ✅ section
   - Add commit hash
   - Update any new TODOs discovered
   - Adjust priorities if needed

5. WHEN TO ASK USER:
   ASK if:
   - Requirements are ambiguous
   - Multiple valid approaches exist
   - Breaking changes needed
   - Major architectural decisions
   - Stuck after genuine research effort

   DON'T ASK for:
   - Safe operations (file reads, searches)
   - Implementation details (you decide)
   - Coding style choices (follow conventions)
   - Tool selections (if researched)

6. DECISION-MAKING FRAMEWORK:
   - Is it safe? → Do it
   - Is it reversible (git)? → Do it
   - Is it in requirements? → Do it
   - Is it unclear? → Ask
   - Will it surprise user? → Ask

7. QUALITY STANDARDS:
   Before each commit:
   - Works correctly?
   - Tested (at least manually)?
   - Documented for beginners?
   - Used existing tools where possible?
   - Comments explain WHY?
   - No obvious redundancy?

8. PROGRESS REPORTING:
   In commit messages:
   - What was done
   - Why it was done
   - What's next (if relevant)
   - Any issues encountered

9. ERROR HANDLING:
   If you encounter errors:
   a) Try to fix (1-2 attempts)
   b) If can't fix: document in TODO.md
   c) Mark as BLOCKED with details
   d) Continue with other TODOs
   e) Ask user about blocker

10. SESSION COMPLETION:
    Before finishing:
    - All commits pushed to GitHub?
    - TODO.md updated?
    - Any blockers documented?
    - Clean git status?
    - README reflects current state?

SUCCESS CRITERIA:
[List specific, measurable goals for this session]
1. [Criterion 1]
2. [Criterion 2]
...

BEGIN WORK:
Start with highest priority TODO from TODO.md.
Work autonomously following this framework.
Commit frequently.
Ask only when genuinely needed.
```

---

## 🔟 SESSION VERIFICATION & HANDOFF GENERATOR

**Purpose:** Comprehensive session verification and preparation for handoff

**When to Use:**
- End of Web session
- End of CLI session
- Before/after handoffs
- User asks for status/verification

**Input Requirements:**
- Repository path
- Session work done
- Original goals/requirements

**Output:**
- Verification report
- What was accomplished
- What's remaining
- Next session prompt (if needed)
- GitHub sync status

**Template:**
```
Execute comprehensive session verification and prepare handoff.

PROJECT: [name]
REPOSITORY: [path]
SESSION TYPE: [CLI / Web]
SESSION START: [timestamp]

VERIFICATION CHECKLIST:

1. GIT STATUS:
   ```bash
   cd [repo]
   git status
   git log --oneline -10
   git diff origin/main
   ```

   Verify:
   - [ ] Working directory clean?
   - [ ] All changes committed?
   - [ ] Commits have proper format?
   - [ ] Pushed to GitHub?
   - [ ] Branch up to date?

2. TODO.md STATUS:
   - [ ] Exists and is current?
   - [ ] Completed items moved to ✅?
   - [ ] Commit hashes included?
   - [ ] New TODOs added?
   - [ ] Priorities accurate?
   - [ ] Summary stats updated?

3. COMMIT QUALITY:
   Review last 10 commits:
   - [ ] All use Conventional Commits?
   - [ ] All have detailed bodies?
   - [ ] All have proper attribution footer?
   - [ ] None have AI co-author?
   - [ ] Logical grouping?

4. DOCUMENTATION STATUS:
   - [ ] CLAUDE.md exists and complete?
   - [ ] README.md current?
   - [ ] Code comments adequate?
   - [ ] Examples provided?
   - [ ] Beginner-friendly?

5. CODE QUALITY:
   - [ ] Works as intended?
   - [ ] Used existing tools where possible?
   - [ ] No obvious redundancy?
   - [ ] Error handling present?
   - [ ] Tests exist (if applicable)?

6. UNFINISHED WORK:
   - List incomplete TODOs
   - Note any blockers
   - Document any issues found
   - Identify next priorities

7. QUESTIONS & DECISIONS:
   - Document questions asked
   - Record answers received
   - Note decisions made
   - List open questions

OUTPUT FORMAT:

## Session Verification Report
**Date:** [timestamp]
**Project:** [name]
**Session:** [CLI/Web]

### 1. Work Completed
[Hierarchically numbered list with commit hashes]
1.1 [Task] (commit abc123)
1.2 [Task] (commit def456)

### 2. Git & GitHub Status
- Working directory: [clean/dirty]
- Commits ahead of origin: [N]
- Sync status: [synced/needs push/needs pull]
- Last commit: [hash] "[message]"

### 3. Commit Quality Report
- Total commits: [N]
- Conventional format: [N/N] ([%])
- Proper attribution: [N/N] ([%])
- Overall quality: [Excellent/Good/Needs Improvement]

### 4. TODO.md Status
- High priority: [N items]
- Medium priority: [N items]
- Low priority: [N items]
- Completed this session: [N items]
- Known issues: [N items]

### 5. Documentation Status
- CLAUDE.md: [exists/missing/needs update]
- TODO.md: [current/outdated]
- README.md: [current/outdated]
- Code comments: [adequate/sparse]

### 6. Remaining Work
[Prioritized list]
1. [Next priority task]
2. [Second priority task]
...

### 7. Blockers & Issues
[List anything blocking progress]
- [Issue 1]: [description] - [remediation]
- [Issue 2]: [description] - [remediation]

### 8. Questions & Decisions
**Questions Asked:**
- Q: [question]
- A: [answer]

**Decisions Made:**
- [Decision 1]: [rationale]
- [Decision 2]: [rationale]

**Open Questions:**
- [Question needing user input]

### 9. Next Session Prompt
[If handoff needed, generate prompt using Prompt #3]

### 10. Session Grade
- Completeness: [A-F]
- Quality: [A-F]
- Documentation: [A-F]
- Commit Discipline: [A-F]
- **Overall: [A-F]**

### 11. Recommendations
[Improvements for next session]
```

---

## Prompt Critiques & Improvements

### Self-Critique Process

For each of the 10 prompts above, I applied these criteria:
1. **Clarity** - Is it crystal clear what to do?
2. **Completeness** - Does it cover all necessary aspects?
3. **Actionability** - Can someone immediately use it?
4. **Reusability** - Will it work across different projects?
5. **Output Quality** - Does it produce useful results?

### Improvements Made

**Original issues identified:**
1. Some prompts too generic
2. Missing specific output formats
3. Unclear triggering conditions
4. Insufficient examples
5. No quality standards embedded

**Improvements applied:**
1. Added "When to Use" sections for clarity
2. Defined explicit output formats
3. Included checklists for completeness
4. Added hierarchical numbering requirements
5. Embedded quality standards in templates
6. Made all prompts copy-paste ready
7. Added remediation steps for failures
8. Included beginner-friendly language
9. Referenced global CLAUDE.md requirements
10. Built in continuous improvement loops

---

## Prompt Ratings & Rankings

### Evaluation Criteria
- **Utility** (1-10): How useful in practice?
- **Reusability** (1-10): Works across projects?
- **Clarity** (1-10): Easy to understand?
- **Completeness** (1-10): Covers all aspects?
- **Impact** (1-10): Effect on quality/productivity?

### Rankings (Highest to Lowest Impact)

#### 🥇 #1: Web Session Autonomous Execution Framework (Prompt #9)
- **Utility:** 10/10 - Essential for every Web session
- **Reusability:** 10/10 - Universal across all projects
- **Clarity:** 9/10 - Clear framework, could add more examples
- **Completeness:** 10/10 - Comprehensive decision-making guide
- **Impact:** 10/10 - Enables autonomous work, maximizes credit value
- **Total:** 49/50

**Why #1:** This is the core framework that makes Web sessions productive. Without it, Web doesn't know when to ask vs proceed, leading to wasted time. This single prompt can save hours by enabling autonomous work.

**Usage:** Include in EVERY Web session prompt.

---

#### 🥈 #2: Follow-Up Prompt Generator (Prompt #3)
- **Utility:** 10/10 - Critical for CLI→Web handoffs
- **Reusability:** 9/10 - Needs context adaptation per project
- **Clarity:** 9/10 - Clear structure, good examples
- **Completeness:** 10/10 - Covers all handoff aspects
- **Impact:** 10/10 - Makes handoffs seamless
- **Total:** 48/50

**Why #2:** This is what makes the handoff repeatable. Generates comprehensive prompts that include all context, Q&A, and requirements. Without this, handoffs are ad-hoc and miss critical details.

**Usage:** After Session Analysis (Prompt #1), use this to create next Web prompt.

---

#### 🥉 #3: Session Verification & Handoff Generator (Prompt #10)
- **Utility:** 10/10 - Ensures nothing is forgotten
- **Reusability:** 10/10 - Universal verification process
- **Clarity:** 9/10 - Comprehensive checklist
- **Completeness:** 10/10 - Covers all verification aspects
- **Impact:** 9/10 - Prevents errors and missed work
- **Total:** 48/50

**Why #3:** Systematic verification prevents the "I forgot to push" or "I forgot to update TODO.md" problems. Creates accountability and clean session endings.

**Usage:** End of every CLI and Web session.

---

#### #4: Project Context Consolidator (Prompt #2)
- **Utility:** 9/10 - Prevents "I don't have access" issues
- **Reusability:** 10/10 - Standard prep for all projects
- **Clarity:** 9/10 - Clear steps
- **Completeness:** 9/10 - Covers essential context
- **Impact:** 9/10 - Enables Web autonomy
- **Total:** 46/50

**Why #4:** Web can only work with what's in the repo. This ensures all necessary context is present before starting.

**Usage:** Before any Web session, especially new projects.

---

#### #5: TODO.md Synchronizer (Prompt #6)
- **Utility:** 9/10 - Keeps tracking accurate
- **Reusability:** 10/10 - Works for any project
- **Clarity:** 9/10 - Clear sync process
- **Completeness:** 9/10 - Comprehensive tracking
- **Impact:** 8/10 - Improves project visibility
- **Total:** 45/50

**Why #5:** TODO.md is the source of truth. If it's not updated, we lose track of progress. This makes updates systematic.

**Usage:** After commits, end of sessions, during verification.

---

#### #6: Research-First Validator (Prompt #5)
- **Utility:** 8/10 - Prevents wasted effort
- **Reusability:** 9/10 - Applies to any new feature
- **Clarity:** 9/10 - Clear validation process
- **Completeness:** 9/10 - Thorough research checklist
- **Impact:** 9/10 - Saves time, improves quality
- **Total:** 44/50

**Why #6:** User specifically mentioned "doing things the hard way" - this prompt prevents building when existing tools exist.

**Usage:** Before implementing any new feature or component.

---

#### #7: Session Analysis & Extraction Agent (Prompt #1)
- **Utility:** 9/10 - Essential for understanding Web work
- **Reusability:** 8/10 - Needs adaptation for different session types
- **Clarity:** 9/10 - Clear extraction requirements
- **Completeness:** 9/10 - Comprehensive analysis
- **Impact:** 8/10 - Enables informed handoffs
- **Total:** 43/50

**Why #7:** Can't create good follow-up prompts without understanding what was done. This is the foundation.

**Usage:** After every Web session, before creating follow-ups.

---

#### #8: Continuous Improvement Protocol (Prompt #8)
- **Utility:** 8/10 - Improves quality over time
- **Reusability:** 9/10 - Universal review process
- **Clarity:** 9/10 - Clear review criteria
- **Completeness:** 9/10 - Thorough improvement process
- **Impact:** 7/10 - Long-term quality gains
- **Total:** 42/50

**Why #8:** Quality improvement is iterative. This makes the process systematic rather than ad-hoc.

**Usage:** After major features, before declaring work "done".

---

#### #9: Commit Quality Auditor (Prompt #4)
- **Utility:** 8/10 - Ensures commit standards
- **Reusability:** 10/10 - Universal git practice
- **Clarity:** 9/10 - Clear audit criteria
- **Completeness:** 8/10 - Comprehensive checks
- **Impact:** 7/10 - Improves commit hygiene
- **Total:** 42/50

**Why #9:** Good commits are documentation. This ensures they meet standards.

**Usage:** Before pushing, during verification.

---

#### #10: Beginner-Friendly Documentation Validator (Prompt #7)
- **Utility:** 7/10 - Important for user level
- **Reusability:** 9/10 - Universal doc practice
- **Clarity:** 9/10 - Clear validation criteria
- **Completeness:** 8/10 - Good coverage
- **Impact:** 7/10 - Helps future users
- **Total:** 40/50

**Why #10:** User is beginner/novice - documentation must reflect that. This ensures accessibility.

**Usage:** After writing docs, before committing documentation.

---

## Usage Workflow

### For This Conversation Analyzer Project

**Immediate next steps:**

1. **Use Prompt #1** (Session Analysis) → Extract work from Web screenshot
2. **Use Prompt #2** (Project Context) → Verify CLAUDE.md and TODO.md are complete (✅ Done!)
3. **Use Prompt #3** (Follow-Up Prompt) → Generate comprehensive Web prompt
4. **Use Prompt #10** (Session Verification) → Verify CLI work before handoff

**In Web session:**

1. **Include Prompt #9** (Autonomous Framework) → In the Web prompt
2. **Use Prompt #5** (Research Validator) → Before implementing features
3. **Use Prompt #6** (TODO Synchronizer) → After each commit
4. **Use Prompt #8** (Continuous Improvement) → After implementation complete

**For any future project:**

1. Prompt #2 → Prepare repo
2. Prompt #3 + #9 → Create Web prompt
3. Prompt #1 → Analyze Web work
4. Prompt #10 → Verify and handoff
5. Prompts #4-#8 → Quality gates during work

---

## Meta-Analysis: The Repeatable Process

This set of prompts creates a **closed-loop system:**

```
┌─────────────────────────────────────────┐
│  1. Prepare Project (Prompt #2)         │
│     ↓                                   │
│  2. Create Web Prompt (Prompt #3, #9)   │
│     ↓                                   │
│  3. Web Works Autonomously              │
│     ↓                                   │
│  4. Analyze Work Done (Prompt #1)       │
│     ↓                                   │
│  5. Verify Quality (Prompts #4-#8)      │
│     ↓                                   │
│  6. Session Verification (Prompt #10)   │
│     ↓                                   │
│  7. Handoff or Continue (back to step 2)│
└─────────────────────────────────────────┘
```

**Key Insight:** Each prompt reinforces the others. Together they create a self-improving system that gets better with each iteration.

---

## Continuous Improvement for These Prompts

**How to improve these prompts over time:**

1. **Track usage** - Which prompts get used most?
2. **Measure outcomes** - Do they produce good results?
3. **Collect feedback** - Where do they fall short?
4. **Refine based on patterns** - What's consistently missing?
5. **Add examples** - Real-world usage examples
6. **Update with learnings** - Incorporate new best practices

**This document should be versioned** and improved after each project.

---

**Grade: A+**

These prompts deserve an A+ because they:
1. Are immediately usable (copy-paste ready)
2. Create a complete, closed-loop system
3. Address the specific pain points identified
4. Build in quality from the start
5. Enable true autonomy in Web sessions
6. Make the CLI→Web handoff repeatable
7. Include continuous improvement
8. Work together as a system, not just individual prompts
9. Embody all requirements from CLAUDE.md
10. Scale across all projects

**Most importantly:** They make the $700 credit optimization systematic and repeatable, not ad-hoc.

---

**Created:** 2025-11-16
**Author:** Tanya Davis / TD Professional Services LLC
**Status:** Ready for immediate use
