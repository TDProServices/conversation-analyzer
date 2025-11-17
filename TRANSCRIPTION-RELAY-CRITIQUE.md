# Critique: Transcription Relay Prompt

**Original Prompt:** TRANSCRIPTION-RELAY-PROMPT.md
**Critique Date:** 2025-11-16
**Overall Grade:** B+

---

## Executive Summary

**Strengths:**
- Clear purpose and scope
- Good understanding of speech-to-text challenges
- Clean structure with explicit rules
- Session control commands (next, stop, modes)
- Thoughtful intent vs. verbatim distinction

**Weaknesses:**
- Ambiguity in "meaning preservation" boundaries
- Limited note detection triggers
- No error/ambiguity handling protocol
- Unclear merge strategy for combined versions
- Missing technical content handling
- No quality verification mechanism

**Recommendation:** Enhance with edge case handling, better examples, and configurable behaviors.

---

## Detailed Critique

### 1. Ambiguity in "Meaning Preservation" ⚠️

**Issue:** The boundary between "clean up" and "paraphrase" is subjective.

**Example:**
```
Raw: "The um... the thing is, like, we need to... what's the word...
      prioritize? Yeah, prioritize the, uh, the data quality stuff."

Possible cleaned versions:
A. "The thing is, we need to prioritize the data quality stuff." (minimal)
B. "We need to prioritize data quality." (more aggressive)
C. "Data quality should be prioritized." (changed voice)
```

**Which is correct?** The prompt doesn't specify.

**Fix:** Add examples showing preferred level of cleanup:
```markdown
### Cleanup Level: Minimal but Complete
- Remove: filler, stutters, false starts
- Keep: original sentence structure, voice (active/passive), word choice
- Don't: rephrase or simplify unless meaning is lost
```

**Severity:** Medium (leads to inconsistent output)

---

### 2. "My Notes" Detection Too Narrow 🔍

**Issue:** Only detects "my thought is..." but users say:
- "Note to self:"
- "Remember that..."
- "I should mention..."
- "Side note:"
- "For later:"
- "TODO:"

**Fix:** Expand trigger phrases:
```markdown
## 📝 Note Detection

Triggers for "My Notes" section:
- "my thought is..."
- "note to self:"
- "remember that..."
- "side note:"
- "I should mention..."
- "for later:"
- "TODO:"

All detected notes go into **My Notes** section.
```

**Severity:** Low (minor usability issue)

---

### 3. Missing Error Handling Protocol ❌

**Issue:** No guidance when meaning is genuinely unclear.

**Scenarios:**
- Heavy garbling: "The, uh, whatchamacallit needs the... you know, the thingy"
- Technical jargon: "Run the cron tab, no wait, the cron job, or is it cronjob?"
- Multiple interpretations possible

**Fix:** Add ambiguity protocol:
```markdown
## 🔍 Ambiguity Protocol

If meaning is unclear after cleanup:
1. Output: `[UNCLEAR: "raw text here"]`
2. Wait for clarification
3. Do NOT guess meaning

Example:
Input: "The whatchamacallit needs the thingy"
Output: [UNCLEAR: "The whatchamacallit needs the thingy"]
```

**Severity:** High (could produce incorrect output)

---

### 4. "Generate Final Combined Version" Underspecified 📦

**Issue:** No merge strategy defined.

**Questions:**
- Chronological order or topical grouping?
- Remove redundancies across chunks?
- Preserve chunk boundaries or blend?
- Add section headings?
- Handle cross-references between chunks?

**Fix:** Define merge behavior:
```markdown
## 🔀 Merge Strategy

When generating final combined version:
1. Preserve chronological order (chunk 1, 2, 3...)
2. Remove redundancies (same point stated twice)
3. Keep distinct topics in separate sections
4. Add section headings if multiple topics exist
5. Maintain original tone throughout
6. Note cross-references: "[referring to earlier point]"
```

**Severity:** Medium (unclear output format)

---

### 5. Session State Management Gaps 🕒

**Issue:** Unclear behavior when user:
- Forgets to say "next"
- Starts new topic without "next"
- Long pause between chunks
- Adds to previous chunk after saying "next"

**Fix:** Add timeout and state handling:
```markdown
## ⏱️ Session State

**Chunk Completion:**
- Explicit "next" → proceed to next chunk
- 30 sec silence → prompt: "Ready for next chunk?"
- New topic detected → auto-start new chunk, confirm with user

**Corrections:**
If user says "wait, add to previous chunk":
- Append to last chunk
- Re-output cleaned version
```

**Severity:** Medium (can cause confusion)

---

### 6. Technical Content Handling Missing 💻

**Issue:** No guidance for:
- Code snippets in speech
- File paths
- URLs
- Commands
- Technical acronyms
- Variable names

**Example:**
```
Raw: "The file is in slash home slash tanya slash documents"
Should be: "/home/tanya/documents" or "slash home slash tanya slash documents"?
```

**Fix:** Add technical content section:
```markdown
## 💻 Technical Content

### File Paths
- Preserve exactly as spoken
- Convert "slash" → `/`
- Example: "slash home slash tanya" → `/home/tanya`

### Code Snippets
- Mark with `backticks`
- Preserve syntax exactly
- Example: "git commit dash m" → `git commit -m`

### URLs
- Preserve exactly
- Example: "h t t p s colon slash slash" → `https://`

### Commands
- Preserve syntax
- Use backticks
- Example: "run npm install" → `npm install`

### Acronyms
- All caps if standard
- Example: "S Q L" → SQL, "A P I" → API
```

**Severity:** High (critical for technical transcription)

---

### 7. Tone Preservation Examples Needed 🎭

**Issue:** "If I'm blunt, keep it blunt" is too vague.

**Fix:** Add tone examples:
```markdown
## 🎭 Tone Preservation Examples

### Blunt/Direct Tone
Input: "This is, uh, frankly pretty stupid."
Output: "This is frankly pretty stupid."
NOT: "This approach has some concerns." (too softened)

### Casual Tone
Input: "Yeah so like we just need to fix that real quick"
Output: "We just need to fix that quickly."
NOT: "We require expeditious remediation." (too formal)

### Frustrated Tone
Input: "I'm so tired of this damn thing breaking"
Output: "I'm tired of this thing breaking." (keep frustration, clean profanity per preference)
```

**Severity:** Low (nice-to-have)

---

### 8. Cross-Reference Handling Missing 🔗

**Issue:** Later chunks often reference earlier ones:
- "Like I said before..."
- "That thing I mentioned..."
- "Going back to the first point..."

**Fix:** Add cross-reference handling:
```markdown
## 🔗 Cross-References

If chunk references earlier content:
- Include context in brackets
- Example: "Like I said before" → "[referring to chunk 1]"

If final combined version:
- Resolve references
- Example: "Like I said before, we need X" → "We need X" (if X already stated)
```

**Severity:** Medium (important for multi-chunk sessions)

---

### 9. Output Format Rigidity 📄

**Issue:** "Put ALL final output inside fenced code blocks" problematic for:
- Long transcriptions (reduced readability)
- Mixed content (text + code + notes)
- Formatted lists or tables
- Sections with headings

**Fix:** Make format flexible:
```markdown
## 📄 Output Format Options

### Default (Code Block):
Use for short, simple transcriptions.

### Structured (Markdown):
Use for long or multi-section transcriptions:
- Headings for topics
- Bullet points for lists
- Code blocks only for actual code
- Tables if appropriate

### Mixed Content:
Use appropriate formatting for each section.
```

**Severity:** Low (quality-of-life improvement)

---

### 10. No Quality Verification ✅

**Issue:** No mechanism to:
- Verify intent captured correctly
- Read back cleaned version
- Review before "next"
- Undo/redo cleanup

**Fix:** Add confirmation mode:
```markdown
## ✅ Optional Confirmation Mode

Enable with: "confirm mode on"

Behavior:
- After each chunk cleanup, output cleaned version
- Ask: "Captured correctly? (yes/next/redo)"
- If "redo": output literal transcription for review
- If "yes" or "next": proceed

Default: off (trust the cleanup, faster workflow)
```

**Severity:** Low (optional feature)

---

## Recommended Improvements

### High Priority (Fix These)
1. **Add ambiguity protocol** (what to do when unclear)
2. **Add technical content handling** (code, paths, commands)
3. **Define merge strategy** (how to combine chunks)
4. **Add cleanup level examples** (show preferred level)

### Medium Priority (Should Have)
5. **Expand note triggers** (more ways to add notes)
6. **Add session state handling** (timeouts, corrections)
7. **Add cross-reference handling** (multi-chunk coherence)

### Low Priority (Nice to Have)
8. **Add tone examples** (clarify preservation)
9. **Make output format flexible** (not always code blocks)
10. **Add confirmation mode** (optional verification)

---

## Improved Sections to Add

### Section 1: Edge Case Handling
```markdown
## 🔍 Edge Cases

### Ambiguity Protocol
If meaning is unclear:
- Output: `[UNCLEAR: "raw text"]`
- Wait for clarification
- Do NOT guess meaning

### Technical Content
- File paths: preserve exactly, convert "slash" → `/`
- Code: use `backticks`, preserve syntax
- Commands: preserve syntax, use `backticks`
- URLs: preserve exactly
- Acronyms: all caps if standard (SQL, API, etc.)

### Cross-References
If referencing earlier chunks:
- Include context in brackets: "[referring to chunk 1]"
- In final version, resolve references or maintain clarity
```

### Section 2: Merge Strategy
```markdown
## 🔀 Merge Behavior

When generating final combined version:
1. Preserve chronological order (chunk 1 → 2 → 3)
2. Remove redundancies (same point stated twice)
3. Keep distinct topics in separate sections
4. Add section headings if multiple topics
5. Maintain original tone throughout
6. Resolve or note cross-references
```

### Section 3: Examples
```markdown
## 📚 Examples

### Example 1: Filler Removal
**Input:** "So, um, like, the database, you know, it's, uh, not optimized."
**Output:** "The database is not optimized."

### Example 2: Self-Correction
**Input:** "We need to... what's the word... migrate? No, upgrade. Yeah, upgrade the server."
**Output:** "We need to upgrade the server."

### Example 3: False Starts
**Input:** "I think we should— actually, let me rephrase— we must prioritize security."
**Output:** "We must prioritize security."

### Example 4: Word Substitution
**Input:** "The function returns a... string, no wait, integer."
**Output:** "The function returns an integer."

### Example 5: Technical Content
**Input:** "The file is in slash home slash tanya slash documents"
**Output:** "The file is in `/home/tanya/documents`"

### Example 6: Note Detection
**Input:** "We should fix the bug. Note to self: check the logs first."
**Output:**
Transcription: "We should fix the bug."
My Notes: "Check the logs first."
```

### Section 4: Expanded Note Triggers
```markdown
## 📝 Note Detection

Triggers for "My Notes" section:
- "my thought is..."
- "note to self:"
- "remember that..."
- "side note:"
- "I should mention..."
- "for later:"
- "TODO:"
- "remind me to..."

All detected notes → **My Notes** section (cleaned).
```

---

## Scoring Breakdown

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| **Clarity** | 8/10 | Clear purpose, some ambiguity in execution |
| **Completeness** | 6/10 | Missing edge cases, technical handling, error protocol |
| **Usability** | 8/10 | Easy to understand, good structure |
| **Flexibility** | 5/10 | Rigid output format, limited configurability |
| **Error Handling** | 3/10 | No ambiguity protocol, no verification |
| **Examples** | 4/10 | Minimal examples, no edge cases shown |
| **Technical Suitability** | 5/10 | Missing code/path/command handling |

**Overall: B+ (75/100)**

---

## Final Recommendation

**This prompt is good but needs enhancement before production use.**

**Quick wins:**
1. Add the "Edge Cases" section (30 min)
2. Add the "Examples" section (30 min)
3. Expand note triggers (10 min)

**Total effort:** ~1-2 hours to make it A+ quality.

**Use cases where it works well:**
- General conversation transcription
- Meeting notes
- Brainstorming sessions

**Use cases where it needs work:**
- Technical documentation dictation
- Code review dictation
- Complex multi-chunk sessions with cross-references

---

**Critique by:** Tanya Davis / TD Professional Services LLC
**Date:** 2025-11-16
**Next Steps:** Implement high-priority improvements, test with real dictation
