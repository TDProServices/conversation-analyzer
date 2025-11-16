"""Prompt templates for LLM extraction."""

SYSTEM_PROMPT = """You are a precise information extraction system. Your task is to extract action items, bugs, feature requests, and project ideas from conversations and code.

IMPORTANT RULES:
1. Extract ONLY items explicitly mentioned in the text
2. Return valid JSON only, no additional commentary
3. Be conservative - if unsure, use lower confidence
4. Extract verbatim quotes for source_context
5. Assign realistic priorities based on context clues

Categories:
- TODO: Explicit action items or tasks mentioned
- BUG: Problems, errors, or issues described
- FEATURE: Feature requests or enhancement ideas
- PROJECT: Potential new projects or major initiatives

For each item extract:
- type: One of [TODO, BUG, FEATURE, PROJECT]
- description: Clear, concise description (5-500 characters)
- priority: Estimated priority [high, medium, low]
- source_context: Relevant quote from source text
- confidence: Your confidence in this extraction (0.0-1.0)

Priority guidelines:
- high: Urgent, critical, blocking, security issues, production problems
- medium: Important but not urgent, planned improvements
- low: Nice-to-have, future considerations, ideas

Confidence guidelines:
- 0.9-1.0: Explicitly stated with clear wording (e.g., "TODO: fix bug")
- 0.7-0.9: Clearly implied or discussed
- 0.5-0.7: Mentioned but ambiguous
- <0.5: Uncertain or questionable extraction
"""

USER_PROMPT_TEMPLATE = """Extract action items from the following text.

OUTPUT FORMAT (JSON only):
{{
  "items": [
    {{
      "type": "TODO",
      "description": "...",
      "priority": "high",
      "source_context": "...",
      "confidence": 0.95
    }}
  ]
}}

INPUT TEXT:
{input_text}

OUTPUT:
"""

FEW_SHOT_EXAMPLES = """
EXAMPLE 1:
Input: "We should fix the login timeout issue. Also TODO: update the docs."
Output: {{
  "items": [
    {{
      "type": "BUG",
      "description": "Fix login timeout issue",
      "priority": "high",
      "source_context": "We should fix the login timeout issue",
      "confidence": 0.9
    }},
    {{
      "type": "TODO",
      "description": "Update documentation",
      "priority": "medium",
      "source_context": "TODO: update the docs",
      "confidence": 0.95
    }}
  ]
}}

EXAMPLE 2:
Input: "CRITICAL: Payment processing is failing! Users can't complete purchases. This is blocking revenue."
Output: {{
  "items": [
    {{
      "type": "BUG",
      "description": "Payment processing failing, blocking user purchases",
      "priority": "high",
      "source_context": "CRITICAL: Payment processing is failing! Users can't complete purchases. This is blocking revenue.",
      "confidence": 0.95
    }}
  ]
}}

EXAMPLE 3:
Input: "Maybe we could add a dark mode feature someday. It might be nice."
Output: {{
  "items": [
    {{
      "type": "FEATURE",
      "description": "Add dark mode feature",
      "priority": "low",
      "source_context": "Maybe we could add a dark mode feature someday",
      "confidence": 0.7
    }}
  ]
}}

EXAMPLE 4:
Input: "# TODO: Refactor authentication\\n# FIXME: SQL injection vulnerability in login\\n# BUG: Cache not invalidating"
Output: {{
  "items": [
    {{
      "type": "TODO",
      "description": "Refactor authentication",
      "priority": "medium",
      "source_context": "TODO: Refactor authentication",
      "confidence": 0.95
    }},
    {{
      "type": "BUG",
      "description": "SQL injection vulnerability in login",
      "priority": "high",
      "source_context": "FIXME: SQL injection vulnerability in login",
      "confidence": 0.95
    }},
    {{
      "type": "BUG",
      "description": "Cache not invalidating",
      "priority": "medium",
      "source_context": "BUG: Cache not invalidating",
      "confidence": 0.9
    }}
  ]
}}

EXAMPLE 5:
Input: "What's the weather like today?"
Output: {{
  "items": []
}}
"""


def build_extraction_prompt(text: str, include_examples: bool = True) -> str:
    """Build complete extraction prompt."""
    prompt = SYSTEM_PROMPT + "\n\n"

    if include_examples:
        prompt += FEW_SHOT_EXAMPLES + "\n\n"

    prompt += "Now extract from this text:\n\n"
    prompt += USER_PROMPT_TEMPLATE.format(input_text=text)

    return prompt


def build_nuextract_prompt(text: str) -> dict:
    """Build prompt specifically for NuExtract model (template-based)."""
    template = {
        "items": [
            {
                "type": "",  # TODO, BUG, FEATURE, PROJECT
                "description": "",
                "priority": "",  # high, medium, low
                "source_context": "",
                "confidence": 0.0,
            }
        ]
    }

    import json

    prompt = f"""Input: {text}

Template: {json.dumps(template, indent=2)}

Extract all action items, TODOs, bugs, features, and project ideas following the template structure.
"""

    return {"role": "user", "content": prompt}


# Code-specific prompt variations
CODE_PROMPT_ADDITIONS = """
Code-specific notes:
- Look for TODO, FIXME, BUG, HACK, NOTE, XXX comments
- Security issues (SQL injection, XSS, etc.) are high priority
- Performance issues are typically medium priority
- Code cleanup/refactoring is typically low-medium priority
- Extract the function/class name if mentioned
"""


def build_code_extraction_prompt(code: str, file_path: str = "") -> str:
    """Build extraction prompt optimized for code."""
    context = f"File: {file_path}\n\n" if file_path else ""
    return build_extraction_prompt(
        context + code, include_examples=True
    ) + "\n" + CODE_PROMPT_ADDITIONS


# Validation prompt for quality checking
VALIDATION_PROMPT_TEMPLATE = """Review this extracted item for quality and accuracy:

Original Text:
{original_text}

Extracted Item:
- Type: {item_type}
- Description: {description}
- Priority: {priority}
- Confidence: {confidence}

Is this extraction:
1. Accurate (faithful to source)?
2. Well-described?
3. Appropriately prioritized?

Respond with JSON:
{{
  "accurate": true/false,
  "well_described": true/false,
  "appropriate_priority": true/false,
  "suggested_confidence": 0.0-1.0,
  "reason": "brief explanation"
}}
"""
