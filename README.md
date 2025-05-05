# Supermarket Refrigeration Simulator

This project is an interactive AI-powered training and diagnostic tool for supermarket rack refrigeration systems. It uses real-world service logic, manuals, and AI-assisted troubleshooting to help apprentices and technicians understand complex refrigeration behavior.

---

## 📁 Project Structure

```
/refrigeration-simulator
├── main.py # Entrypoint for running the simulator
├── requirements.txt # Python dependencies (LangChain, Supabase, etc.)
├── ai_coding_guidelines.md # Ruleset for consistent, apprentice-friendly AI code
├── development_roadmap.md # Sequential build plan for all simulator modules
├── project_objectives.md # High-level purpose and long-term simulator goals
├── diagnostics_engine.py # Core logic for diagnosing refrigeration faults
├── llm_interface.py # Abstraction layer to interact with Gemini, OpenAI, etc.
├── embedding_pipeline.py # Converts manuals into searchable vector embeddings
├── vector_search.py # Retrieves relevant document chunks using Supabase
├── simulator_cli.py # Command-line interface for entering simulated values
└── component_specs.json # Structured data store for compressors, valves, alarms
---

## 🚀 Getting Started

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Supabase Vector Store**

   Create a project at Supabase.io

   Add your SUPABASE_URL and SUPABASE_ANON_KEY to a .env file:

   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-key-here

3. **Run the Simulator**

   ```bash
   python main.py
   ```

4. **Embed Documents**
   Place PDF manuals in a `/docs` folder and use `embedding_pipeline.py` to embed them:

   ```bash
   python embedding_pipeline.py --input_folder=docs
   ```

---

## 📌 Key AI Practices

* Always follow the structure in `ai_coding_guidelines.md`
* Use `development_roadmap.md` to guide module completion and integration
* When prompting AI in Cursor or elsewhere, include:

  > “Use the Refrigeration AI Coding Guidelines. Diagnose with confidence levels, cite manuals, and show safety warnings.”

---

## 💡 Future Plans

* Add FastAPI-based web UI
* Integrate live telemetry input from physical training rigs
* Develop a graphical timeline of pressure/temp data
* Train a fine-tuned model based on historical service data

---

## 📞 Contact / Support

For technical support or collaboration inquiries, contact the project maintainer.

