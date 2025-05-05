# Supermarket Refrigeration Rack Simulator — Objectives & System Design

## 🌟 Project Objectives

* Simulate a realistic rack system (medium + low temp) using R-448A.
* Accept manual input of sensor values and alarm conditions.
* Diagnose issues using AI grounded in refrigeration manuals.
* Provide:

  * Root cause suggestions
  * Confidence scores
  * Suggested next steps
  * Safety warnings
* Train apprentices by mapping real-world symptoms to decision trees.

## 🧠 AI Integration

* Retrieval-Augmented Generation (RAG) using LangChain.
* Free vector database: **Supabase**.
* Documents embedded: service manuals, datasheets, flowcharts.
* Use **Model Context Protocol (MCP)** for structured prompt formatting.
* Modular LLM support for Gemini (default), OpenAI, Anthropic.

## 🔍 Data Sources

* Technical PDFs converted to text/JSON.
* Structured component specs and alarm codes.
* Input from simulated or real field scenarios.
* Diagnostic thresholds and flowchart logic.

## ⚙️ Core System Modules

* `RackSimulator`: Simulates sensor behavior + equipment states.
* `DiagnosticsEngine`: Rule-based + AI-enhanced fault detection.
* `VectorSearch`: Embeds and retrieves relevant manual data.
* `LLMInterface`: Abstracts provider access (Gemini/OpenAI/etc.).
* `UI/CLI`: Interface for manual input and diagnostic feedback.

## 📆 Milestones

1. Scaffold simulator environment + CLI.
2. Build manual ingestion and vector embedding.
3. Connect diagnostics to sensor data + AI.
4. Test with simulated field conditions.
5. Deploy MVP to apprentice testers.

## 📂 Proposed File Structure

```
/simulator
  ├── diagnostics/         # Rules + AI-powered fault detection
  ├── embeddings/          # Vector DB storage + loaders
  ├── llm/                # LLM interface (Gemini, OpenAI)
  ├── manuals/            # Parsed manuals + specs
  ├── ui/                 # CLI or web front-end
  ├── config/             # Environment, constants, LLM keys
  ├── main.py             # Entrypoint
  └── simulator_objectives.md
```

---
