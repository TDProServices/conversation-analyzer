# Conversation Analyzer - Research Report

**Date:** November 16, 2025
**Author:** TD Professional Services LLC
**Purpose:** Comprehensive research for building a local LLM-powered conversation analysis system

---

## Executive Summary

This research report evaluates tools, frameworks, models, and methodologies for building a conversation analyzer that extracts TODOs, bugs, feature requests, and project opportunities from conversations, code, and documentation using local LLMs (Ollama).

### Key Findings

1. **Best Model for Extraction:** NuExtract (phi-3-mini fine-tuned) - specialized for structured information extraction
2. **Best Testing Framework:** DeepEval - pytest-style LLM evaluation with 30+ prebuilt metrics
3. **Best Integration Framework:** LangChain with langchain-ollama package (updated Oct 2025)
4. **Recommended Approach:** Pydantic-based structured output with few-shot prompting

---

## 1. Testing Frameworks & Evaluation Tools

### 1.1 Primary Testing Framework: DeepEval

**Why DeepEval:**
- Open-source, pytest-style interface for LLM testing
- 30+ prebuilt research-backed metrics
- Native CI/CD integration
- Supports faithfulness, factual consistency, toxicity, hallucination detection
- Unit-test-like interface: `pytest test_llm_outputs.py`

**Installation:**
```bash
pip install deepeval
```

**Key Metrics Available:**
- Faithfulness (grounding in source)
- Answer Relevancy
- Hallucination Detection
- Toxicity/Profanity
- Bias Detection
- Knowledge Retention

**Example Usage:**
```python
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

def test_extraction_quality():
    test_case = LLMTestCase(
        input="User mentioned: TODO: fix the login bug",
        actual_output='{"type": "TODO", "description": "fix the login bug"}',
        expected_output='{"type": "TODO", "description": "fix the login bug"}'
    )
    metric = AnswerRelevancyMetric(threshold=0.8)
    assert_test(test_case, [metric])
```

### 1.2 Alternative Testing Tools

**Guardrails AI:**
- Validates input/output data against specific criteria
- Profanity, toxicity, compliance checks
- Real-time output validation

**Deepchecks:**
- Open-source data validation and drift detection
- Bias detection, sentiment analysis
- Supports ROUGE and METEOR metrics

**TruLens:**
- Real-time output monitoring
- Hallucination detection
- Usefulness and relevance measurement

**OpenAI Evals:**
- Community-driven evaluation framework
- Custom test design and execution

**Promptfoo:**
- A/B testing for prompts
- LLM-as-a-judge evaluations
- 51,000+ developers using it
- Simple YAML/CLI configuration

### 1.3 LangSmith Pytest Plugin

**Features:**
- Define datasets and evaluations as pytest test cases
- Track assertions in LangSmith
- Raise assertion errors locally for CI pipelines

**Installation:**
```bash
pip install langsmith pytest-langsmith
```

### 1.4 Evaluation Metrics

**Accuracy Metrics:**
- **Perplexity:** How well model predicts next word
- **BLEU:** Overlap between generated and reference text
- **ROUGE:** Recall-oriented overlap measurement
- **Lexical Similarity:** Word-level matching

**Quality & Safety Metrics:**
- **Bias Score:** Fairness across groups
- **Hallucination Detection:** Groundedness in source
- **Toxicity Detection:** Harmful content identification
- **Answer Relevancy:** Response alignment with query

**Production Metrics:**
- **Accuracy:** Correct result generation
- **Latency:** Response time
- **Scalability:** Performance under load

---

## 2. Ollama Models for Text Extraction

### 2.1 Top Recommendation: NuExtract

**Model:** nuextract (phi-3-mini fine-tuned)
**Specialization:** Information extraction from text
**Model Page:** https://ollama.com/library/nuextract

**Key Features:**
- Fine-tuned on high-quality synthetic dataset
- Purely extractive (all output is verbatim from source)
- Input limit: 2000 tokens
- JSON template-based extraction
- Perfect for TODO/bug/feature extraction

**Installation:**
```bash
ollama pull nuextract
```

**Usage Pattern:**
```python
import ollama

template = {
    "items": [
        {
            "type": "",  # TODO, BUG, FEATURE, PROJECT
            "description": "",
            "priority": "",  # high, medium, low
            "source_location": "",
            "confidence": 0.0
        }
    ]
}

response = ollama.chat(
    model='nuextract',
    messages=[{
        'role': 'user',
        'content': f'Input: {text}\n\nTemplate: {json.dumps(template)}'
    }]
)
```

### 2.2 Alternative Models

**For General Text Processing:**

1. **Llama 3.1 (70B)**
   - Large context window: 128K tokens
   - Excellent for long document analysis
   - Competitive with closed-source models
   - High resource requirements

2. **DeepSeek-R1**
   - Strong reasoning capabilities
   - Competitive performance
   - Good for complex extraction

**For Vision/Document Processing (if needed later):**

1. **Llama 3.2 Vision**
   - High accuracy for complex documents
   - OCR capabilities
   - Document layout analysis

2. **Granite3.2-vision**
   - Visual document understanding
   - Tables, charts, diagrams extraction
   - Compact and efficient

3. **Qwen-VL**
   - Advanced document layout analysis
   - OCR capabilities

### 2.3 Model Selection Criteria

**System Requirements:**
- 8GB RAM minimum (for 7B models)
- 16GB+ RAM recommended (for better models)
- GPU optional but improves performance
- Models range from 1-50GB storage

**Performance Considerations:**
- NuExtract: Best accuracy for extraction tasks
- Llama 3.1 8B: Good balance of speed and quality
- Llama 3.1 70B: Best quality, slower, more resources

**Recommendation for This Project:**
Start with **nuextract** for extraction, fallback to **llama3.1:8b** for analysis/summarization.

---

## 3. Ollama Installation & Setup

### 3.1 Installation

**System Requirements:**
- OS: macOS, Linux, or Windows
- RAM: 16GB recommended
- Storage: 50GB+ for models
- GPU: Optional (NVIDIA/AMD)

**Installation Steps:**

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

**Verify Installation:**
```bash
ollama --version
ollama serve  # Start the server
```

### 3.2 Python Integration

**Install Python Package:**
```bash
pip install ollama
```

**Basic Usage:**
```python
import ollama

# Pull a model
ollama.pull('nuextract')

# Generate response
response = ollama.generate(
    model='nuextract',
    prompt='Extract TODOs from: TODO: Fix login bug'
)

# Chat interface
response = ollama.chat(
    model='nuextract',
    messages=[
        {'role': 'user', 'content': 'Extract items from this text...'}
    ]
)
```

### 3.3 Best Practices

**Configuration Management:**
```python
import os

class OllamaConfig:
    HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    MODEL = os.getenv('OLLAMA_MODEL', 'nuextract')
    TEMPERATURE = float(os.getenv('OLLAMA_TEMPERATURE', '0.1'))
    MAX_TOKENS = int(os.getenv('OLLAMA_MAX_TOKENS', '2048'))
```

**Performance Optimization:**
- Set `stream=False` for complete responses
- Adjust `max_tokens` based on expected output
- Use temperature=0.1 for consistent extraction
- Batch requests when possible

**Memory Management:**
- Monitor RAM usage with `ollama ps`
- Unload models when not needed: `ollama stop <model>`
- Use smaller models for development/testing

**Privacy & Security:**
- All processing happens locally
- No data sent to external APIs
- Perfect for sensitive conversations/code

---

## 4. Prompt Engineering for Structured Extraction

### 4.1 Current State (2025)

**Key Techniques:**
1. **Structured Output APIs** - Pass JSON schema to guide output
2. **Few-Shot Learning** - Provide examples in prompt
3. **Schema-Based Prompting** - Define exact fields to extract
4. **Template-Based Extraction** - Use structured templates

### 4.2 Research Findings

**Recent Performance Data (May 2025):**
- Prompt-based extraction with APE: 95.5% precision
- Document information extraction: 91.5% accuracy
- Low training cost, high effectiveness

**Prompt Style Considerations:**
- JSON format: Best for structured data
- YAML format: More readable, slightly slower
- Hybrid CSV/Prefix: Good for simple extractions

### 4.3 Recommended Prompt Pattern

**Structure:**
```
SYSTEM PROMPT:
You are a precise information extraction system. Extract only items that are explicitly mentioned. Return valid JSON only.

USER PROMPT:
Extract action items from the following conversation.

Categories:
- TODO: Explicit action items or tasks mentioned
- BUG: Problems, errors, or issues described
- FEATURE: Feature requests or enhancement ideas
- PROJECT: Potential new projects or major initiatives

For each item extract:
- type: One of [TODO, BUG, FEATURE, PROJECT]
- description: Clear, concise description
- priority: Estimated priority [high, medium, low]
- source_context: Relevant quote from source
- confidence: Your confidence (0.0-1.0)

Output JSON format:
{
  "items": [
    {
      "type": "TODO",
      "description": "...",
      "priority": "high",
      "source_context": "...",
      "confidence": 0.95
    }
  ]
}

INPUT TEXT:
[conversation text here]

OUTPUT:
```

**Few-Shot Example:**
```
EXAMPLE 1:
Input: "We should fix the login timeout issue. Also TODO: update the docs."
Output: {
  "items": [
    {
      "type": "BUG",
      "description": "Login timeout issue",
      "priority": "high",
      "source_context": "fix the login timeout issue",
      "confidence": 0.9
    },
    {
      "type": "TODO",
      "description": "Update documentation",
      "priority": "medium",
      "source_context": "TODO: update the docs",
      "confidence": 0.95
    }
  ]
}

Now extract from this text:
[actual input]
```

### 4.4 Validation with Pydantic

```python
from pydantic import BaseModel, Field, validator
from typing import List, Literal

class ExtractedItem(BaseModel):
    type: Literal["TODO", "BUG", "FEATURE", "PROJECT"]
    description: str = Field(..., min_length=5, max_length=500)
    priority: Literal["high", "medium", "low"]
    source_context: str
    confidence: float = Field(..., ge=0.0, le=1.0)

    @validator('description')
    def description_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()

class ExtractionResult(BaseModel):
    items: List[ExtractedItem]
```

---

## 5. Framework Comparison: LangChain vs LlamaIndex

### 5.1 LangChain

**Current Version:** langchain-ollama updated October 2025

**Strengths:**
- Mature ecosystem with extensive integrations
- LangGraph for complex agent orchestration
- Strong community support
- Excellent for conversational workflows
- Good prompt templating system

**For This Project:**
- ✅ Easy Ollama integration
- ✅ Structured output parsing
- ✅ Chain composition for multi-step extraction
- ✅ LangSmith for monitoring/debugging

**Installation:**
```bash
pip install langchain langchain-ollama pydantic
```

**Example:**
```python
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="nuextract", temperature=0.1)
parser = JsonOutputParser(pydantic_object=ExtractionResult)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an extraction assistant."),
    ("user", "{input}")
])

chain = prompt | llm | parser
result = chain.invoke({"input": conversation_text})
```

### 5.2 LlamaIndex

**Current Evolution:** LlamaCloud with schema-driven extraction

**Strengths:**
- Excellent for RAG (Retrieval-Augmented Generation)
- Document indexing and search
- Schema-driven data extraction
- Agentic Document Workflows
- Strong document processing

**For This Project:**
- ✅ Good for indexing past conversations
- ✅ Multi-modal support (if we add image analysis)
- ✅ LlamaExtract for structured data
- ⚠️ More complex than needed for simple extraction

### 5.3 Recommendation

**Use LangChain for:**
- ✅ Primary extraction pipeline
- ✅ Prompt engineering and testing
- ✅ Chain composition
- ✅ Simple, straightforward integration

**Consider LlamaIndex later for:**
- Indexing large conversation archives
- Semantic search across conversations
- If we need RAG capabilities

---

## 6. Conversation Analysis Tools

### 6.1 Existing Tools & Patterns

**DocMind AI:**
- Streamlit app with LlamaIndex + Ollama
- Multi-format document analysis
- Outputs: summaries, insights, action items, open questions
- Export: JSON or Markdown
- **Relevance:** Similar architecture to our needs

**Graph Analysis Pattern:**
- Load conversations into graph structure
- Analyze actual vs expected patterns
- Find bugs and improvement opportunities
- **Relevance:** Could use for advanced analytics phase

**PostHog-LLM:**
- Conversation analysis with funnels
- Local LLM integration with Docker
- **Relevance:** Automation patterns applicable

### 6.2 Key Insights

1. **Markdown Export Standard:** Most tools export to Markdown for reports
2. **JSON for Processing:** Structured data stored as JSON
3. **Action Item Focus:** Common pattern is extracting action items
4. **Context Window Challenges:** Need to handle long conversations
5. **Graph Analysis:** Useful for finding patterns across conversations

---

## 7. Deduplication & Intelligence

### 7.1 Deduplication Strategies

**Embedding-Based Similarity:**
```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')  # Local, lightweight

def find_duplicates(items, threshold=0.85):
    descriptions = [item['description'] for item in items]
    embeddings = model.encode(descriptions)

    similarity_matrix = cosine_similarity(embeddings)

    duplicates = []
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            if similarity_matrix[i][j] > threshold:
                duplicates.append((items[i], items[j], similarity_matrix[i][j]))

    return duplicates
```

**Exact Match Detection:**
```python
import difflib

def fuzzy_match(str1, str2, threshold=0.9):
    ratio = difflib.SequenceMatcher(None, str1, str2).ratio()
    return ratio >= threshold
```

### 7.2 Priority Scoring Algorithm

**Factors:**
- Urgency keywords: "urgent", "critical", "asap", "immediately"
- Impact indicators: "breaks", "blocks", "prevents", "security"
- Explicit priority: "high priority", "important"
- Recurrence: Mentioned multiple times
- Timeframe: "today", "this week" vs "someday"

**Implementation:**
```python
def calculate_priority_score(item, context):
    score = 0.5  # Base score

    # Urgency keywords
    urgency_terms = ['urgent', 'critical', 'asap', 'immediately', 'blocker']
    for term in urgency_terms:
        if term in item['description'].lower():
            score += 0.2

    # Impact indicators
    impact_terms = ['breaks', 'blocks', 'prevents', 'security', 'data loss']
    for term in impact_terms:
        if term in item['description'].lower():
            score += 0.15

    # Explicit priority
    if item.get('priority') == 'high':
        score += 0.3
    elif item.get('priority') == 'medium':
        score += 0.1

    # Recurrence (if mentioned multiple times)
    if context.get('mention_count', 1) > 1:
        score += 0.1 * min(context['mention_count'] - 1, 3)

    # Normalize to 0-1
    return min(score, 1.0)

def assign_priority(score):
    if score >= 0.75:
        return "high"
    elif score >= 0.45:
        return "medium"
    else:
        return "low"
```

### 7.3 Linking Related Items

**Approach:**
1. Extract entities (file names, function names, components)
2. Build entity → items mapping
3. Link items sharing entities

**Implementation:**
```python
import re

def extract_entities(text):
    entities = {
        'files': re.findall(r'\b[\w/]+\.\w+\b', text),
        'functions': re.findall(r'\b\w+\(\)', text),
        'components': re.findall(r'\b[A-Z][a-zA-Z]+Component\b', text)
    }
    return entities

def link_related_items(items):
    entity_map = {}

    for item in items:
        entities = extract_entities(item['description'] + ' ' + item['source_context'])
        item['entities'] = entities

        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                if entity not in entity_map:
                    entity_map[entity] = []
                entity_map[entity].append(item['id'])

    # Add related_to field
    for item in items:
        related = set()
        for entity_list in item['entities'].values():
            for entity in entity_list:
                related.update(entity_map.get(entity, []))
        related.discard(item['id'])  # Remove self
        item['related_to'] = list(related)

    return items
```

---

## 8. Recommendations & Next Steps

### 8.1 Technology Stack

**Core:**
- Python 3.11+
- Ollama with nuextract model
- LangChain for orchestration
- Pydantic for validation
- SQLite for storage

**Testing:**
- pytest for unit tests
- DeepEval for LLM evaluation
- Custom fixtures for test data

**Additional:**
- sentence-transformers for deduplication
- ripgrep for file scanning
- rich for CLI output
- pandas for data manipulation

### 8.2 Architecture Approach

**Phase 1 (MVP):**
1. Simple conversation parser (Markdown/JSON)
2. NuExtract-based extraction
3. Pydantic validation
4. Basic SQLite storage
5. Simple Markdown reports

**Phase 2 (Intelligence):**
1. Deduplication with embeddings
2. Priority scoring algorithm
3. Entity linking
4. Enhanced reports with grouping

**Phase 3 (Automation):**
1. Watch folders for new conversations
2. Auto-update existing items
3. Notification system for high-priority items
4. Integration with task trackers

### 8.3 Development Priorities

**Critical Path:**
1. ✅ Research (COMPLETED)
2. ⏭️ Set up Ollama and test nuextract
3. ⏭️ Design database schema
4. ⏭️ Create test fixtures
5. ⏭️ Build extraction pipeline
6. ⏭️ Implement testing suite
7. ⏭️ Add intelligence features
8. ⏭️ Polish and document

### 8.4 Testing Strategy

**Unit Tests:**
- Parser functions
- Entity extraction
- Priority scoring
- Deduplication logic

**Integration Tests:**
- Full extraction pipeline
- Database operations
- Report generation

**LLM Evaluation Tests:**
- Extraction accuracy
- Consistency across runs
- Edge case handling
- Hallucination detection

**Test Data:**
- Sample conversations (real anonymized data)
- Edge cases (empty, malformed, very long)
- Known good outputs for regression testing

### 8.5 Success Metrics

**Quality Metrics:**
- Extraction accuracy > 90%
- False positive rate < 10%
- Deduplication accuracy > 85%
- Processing speed < 5 sec per conversation

**Usability Metrics:**
- Setup time < 5 minutes
- Clear, actionable reports
- Easy to customize prompts
- Stable, reproducible results

---

## 9. Open Questions & Risks

### 9.1 Questions to Address

1. **Input Format:** Focus on Claude Code conversation exports or also support other formats?
2. **Real-time vs Batch:** Process conversations as they happen or batch analysis?
3. **Report Format:** Markdown only, or also support HTML/PDF?
4. **Integration:** Should we integrate with GitHub Issues, Jira, etc.?

### 9.2 Known Risks

1. **Context Window Limits:** Very long conversations may need chunking
2. **Model Hallucinations:** Need robust validation and confidence scoring
3. **Ollama Setup:** User must install and run Ollama service
4. **Resource Requirements:** May be slow on low-end hardware

### 9.3 Mitigation Strategies

1. **Context Window:** Implement smart chunking with overlap
2. **Hallucinations:** Use DeepEval metrics + confidence thresholds
3. **Ollama Setup:** Provide clear installation guide + Docker option
4. **Performance:** Support multiple model sizes, optimize prompts

---

## 10. Research Citations

### Testing Frameworks
- DeepEval: https://github.com/confident-ai/deepeval
- Promptfoo: https://www.promptfoo.dev/
- LangSmith: https://docs.langchain.com/langsmith/

### Ollama Models
- NuExtract: https://ollama.com/library/nuextract
- Ollama Library: https://ollama.com/library

### Frameworks
- LangChain: https://python.langchain.com/
- LangChain-Ollama: https://pypi.org/project/langchain-ollama/

### Research Papers
- "Prompt Patterns for Structured Data Extraction" (2025)
- "Evaluation of Prompt Engineering on LLM Document Extraction" (May 2025)

### Best Practices
- Ollama Python Integration Guide: https://www.gcptutorials.com/
- LLM Testing Guide 2025: https://www.confident-ai.com/blog/

---

## Conclusion

This research provides a solid foundation for building the conversation analyzer. The recommended stack (Python + Ollama + NuExtract + LangChain + DeepEval) offers:

- ✅ **Privacy:** Fully local processing
- ✅ **Performance:** Optimized for extraction tasks
- ✅ **Testing:** Comprehensive evaluation framework
- ✅ **Maintainability:** Standard tools and patterns
- ✅ **Extensibility:** Easy to add features

**Next Steps:**
1. Install and test Ollama with nuextract
2. Design database schema and data models
3. Create test fixtures and evaluation criteria
4. Build MVP extraction pipeline
5. Iterate based on real data

**Estimated Timeline:**
- Research: ✅ Completed (3 hours)
- Setup & Design: 2-3 hours
- MVP Development: 4-5 hours
- Testing & Intelligence: 3-4 hours
- Documentation & Polish: 1-2 hours

**Total: 13-17 hours of high-quality development**
