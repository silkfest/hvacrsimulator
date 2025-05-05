# AI Coding Rules for Refrigeration Diagnostic Tool

## 1. Code Design Principles

* Use modular function design (e.g., `def diagnose_low_suction_pressure(data):`)
* Maintain clean, readable code with inline comments suitable for apprentice-level understanding
* Group logic into cohesive classes or modules (e.g., `CompressorDiagnostics`, `SuperheatAnalysis`)
* Keep code responsibilities separated: parsing, transformation, storage, search, and UI

## 2. Domain Logic Integration

* Translate flowcharts and service manual logic into `if/else` or decision-tree structures
* Apply domain-specific terminology consistently and correctly (e.g., "liquid line restriction", "superheat too high")
* Automatically raise safety warnings when known dangerous conditions are detected:

```python
if discharge_temp_f > 275:
    raise Warning("High discharge temp > 275°F may damage compressor. Shut down if persistent.")
```

## 3. Manual and Data Sheet Usage

* Use structured JSON templates for component specs with embedded source references:

```json
{
  "model": "ZB58KCE-TFD",
  "type": "Compressor",
  "refrigerant": "R-448A",
  "max_discharge_temp_f": 275,
  "oil_type": "POE 32",
  "alarm_conditions": ["high_discharge_temp", "locked rotor"],
  "manual_reference": "Copeland AE4-1327"
}
```

* When citing thresholds or steps, include the manual source and section if available

## 4. Diagnostic Behavior

* Support multi-symptom analysis using weighted logic:

```python
if low_suction and high_superheat and compressor_hot:
    return {
        "diagnosis": "Possible low refrigerant charge or restriction",
        "confidence": 0.85,
        "next_steps": ["Check sight glass", "Verify subcooling", "Inspect TXV"]
    }
```

* Include the following in every diagnostic response:

  * Primary diagnosis
  * Confidence level (0–1.0)
  * Suggested next steps
  * Safety warnings (when applicable)

## 5. Vector Search & LLM Integration

* Use LangChain to retrieve context from Supabase embeddings
* Always ground LLM answers in retrieved document content when diagnosing
* Fallback message when uncertain or insufficient data exists:

> “Cannot confirm root cause. More data on condenser fan status and ambient temp is needed.”

## 6. RAG and MCP Alignment

* Use **Retrieval-Augmented Generation (RAG)** for grounding AI responses in manual-based vector search.
* Format prompts and document contexts using **Model Context Protocol (MCP)** where possible for LLM compatibility and future-proofing.
* Store component specs and alarm thresholds in MCP-compliant or easily convertible JSON format.
* Ensure any LLM (Gemini, OpenAI, Claude) is wrapped through a unified interface so switching providers is seamless.

---

## Enforcing These Rules in Cursor

1. **Pin This File:** Keep `ai_coding_guidelines.md` open and pinned during development.

2. **Include Prompts with Context:** When using AI autocomplete or chat, prepend prompts with:

> “Use the Refrigeration AI Coding Guidelines. Diagnose with confidence levels, cite manuals, and show safety warnings.”

3. **Preload Context:** Use Cursor's embedded context window (upper right) to include this ruleset as context.

4. **Refactor Suggestions:** When the AI suggests code, ask:

> “Refactor this per the Refrigeration Diagnostic AI rules. Add inline comments, confidence levels, and source references.”

5. **Automate With Snippets:** Create a snippet or prompt template in Cursor like:

```markdown
### Refrigeration Diagnostic Coding Prompt
- Follow AI Coding Guidelines
- Use structured JSON or modular Python
- Add inline apprentice-level comments
- Include source if referencing manuals
- Return confidence levels and next steps
```
