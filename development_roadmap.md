# Supermarket Refrigeration Simulator — Development Roadmap & AI Instructions

This document provides a sequenced list of modules, files, and components to build the Supermarket Refrigeration Rack Simulator using the AI Coding Guidelines. It is designed to be pinned in Cursor to guide step-by-step execution with context.

---

## ✅ Existing Documents

* `ai_coding_guidelines.md`: Enforces apprentice-readable, modular, domain-aware AI diagnostic code
* `requirements.txt`: Lists core dependencies (LangChain, Supabase, LLMs, PDF parsing, FastAPI, etc.)
* `main.py`: Entrypoint scaffold linking CLI input, diagnostic engine, vector search, and LLMs
* `project_objectives.md`: High-level design goals, simulator purpose, and long-term vision

---

## 🔧 Next Files to Build

### 1. `diagnostics_engine.py`

* Modular functions for evaluating symptoms, calculating confidence, issuing safety warnings
* Follows section 2 and 4 of the AI Coding Guidelines
* Returns:

  * `diagnosis`
  * `confidence`
  * `next_steps`
  * `safety_warnings`

### 2. `llm_interface.py`

* Wraps Gemini API (initial) and optionally OpenAI/Claude using a single class interface
* Responsible for formatting prompts in MCP or structured JSON
* Abstracts model switching behind a clean `ask_llm(prompt, context)` function

### 3. `embedding_pipeline.py`

* Script/module to process PDF manuals or datasheets into embeddings using LangChain + Supabase
* Store chunked documents by component (e.g., Copeland compressors, Danfoss EPR valves)
* Use `unstructured`, `pypdf`, or custom loaders

### 4. `vector_search.py`

* Load Supabase DB
* Accept component names or symptoms as input, return relevant document chunks
* Used by diagnostics engine and LLM interface

### 5. `component_specs.json`

* MCP-compatible component metadata store
* Compressor models, fan curves, valve ranges, alarm thresholds
* Use this format to cross-reference structured diagnostic rules

### 6. `simulator_cli.py`

* Simple CLI for user to enter simulated values (e.g., suction pressure, superheat, discharge temp)
* Outputs diagnosis, confidence, warnings, and LLM-powered summary
* Eventually extend with TUI using `rich`

---

## 📌 Integration Points

* `main.py` should tie together:

  * `SimulatorCLI → DiagnosticsEngine → VectorSearch → LLMInterface`
* Prompts passed to LLM must include context from vector search + structured data from `component_specs.json`
* All output must include confidence levels, next steps, and warnings

---

## 🧠 When Using Cursor AI

Always prepend prompts with:

> "Use the Refrigeration AI Coding Guidelines. Diagnose with confidence levels, cite manuals, and show safety warnings."

Keep the following files pinned:

* `ai_coding_guidelines.md`
* `project_objectives.md`
* `development_roadmap.md`

Ensure AI-generated code follows:

* Modular format
* Inline apprentice-level comments
* Source references from documents/manuals

---

## ✅ Future Ideas (Optional)

* Add FastAPI endpoints for web version of simulator
* Integrate real-time MQTT or Modbus input from physical trainer rig
* Add visual graphing for pressures and temperatures over time
* Train a custom LoRA or fine-tuned model with service manual logic

---

> This roadmap is a living document. Update as architecture evolves.
