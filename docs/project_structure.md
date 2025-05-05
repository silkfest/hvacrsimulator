# Refrigeration Simulator Project Structure

## Directory Structure
```
simulator/
├── config/                     # Configuration files
│   ├── manual_config.json     # Manual processing configuration
│   └── component_specs.json   # Component specifications
│
├── docs/                      # Documentation
│   └── project_structure.md   # This file
│
├── embeddings/                # Vector search and embedding
│   ├── vector_search.py      # Supabase vector search implementation
│   └── embedding_pipeline.py # PDF processing pipeline
│
├── manuals/                   # Refrigeration manuals
│   ├── raw/                  # Unprocessed PDFs
│   ├── organized/            # Organized by component type
│   └── processed/            # Processed files
│
├── scripts/                   # Utility scripts
│   ├── manual_processor.py   # Manual organization and processing
│   └── validate_mappings.py  # Mapping validation and correction
│
├── diagnostics/              # Diagnostic modules
│   └── engine.py            # Diagnostic engine implementation
│
├── simulator/               # Simulation modules
│   └── rack_simulator.py   # Rack simulation implementation
│
├── llm/                    # Language model interface
│   └── interface.py       # LLM communication interface
│
└── ui/                    # User interface
    └── cli.py            # Command-line interface
```

## Key Files

### Configuration Files
- `config/manual_config.json`: Contains:
  - Manufacturer mappings
  - Component type definitions
  - Model number patterns
  - Keywords for component identification

- `config/component_specs.json`: Contains:
  - Component specifications
  - Operating ranges
  - Safety thresholds
  - Diagnostic rules

### Embedding System
- `embeddings/vector_search.py`:
  - Supabase vector store integration
  - Semantic search implementation
  - Component-specific search
  - Diagnostic context search

- `embeddings/embedding_pipeline.py`:
  - PDF processing
  - Document chunking
  - Vector embedding
  - Supabase storage

### Manual Processing
- `scripts/manual_processor.py`:
  - Manual organization
  - Component mapping
  - File processing
  - Configuration management

- `scripts/validate_mappings.py`:
  - Mapping validation
  - Interactive correction
  - Error reporting
  - File path verification

### Core Components
- `diagnostics/engine.py`:
  - Diagnostic rule processing
  - Symptom analysis
  - Confidence scoring
  - Next steps generation

- `simulator/rack_simulator.py`:
  - Rack system simulation
  - Component interaction
  - Performance modeling
  - State management

- `llm/interface.py`:
  - Language model communication
  - Query processing
  - Response generation
  - Context management

- `ui/cli.py`:
  - Command-line interface
  - User interaction
  - Input processing
  - Output formatting

## Manual Organization

### Component Types
1. Compressors
   - Semi-hermetic
   - Scroll
   - Reciprocating
   - Screw

2. Valves
   - Expansion
   - Solenoid
   - Check
   - Pressure

3. Fans
   - Condenser
   - Evaporator
   - EC
   - AC

4. Evaporators
   - DX
   - Flooded
   - Plate
   - Shell and tube

5. Controls
   - Electronic
   - Mechanical
   - Digital

6. Condensers
   - Air-cooled
   - Water-cooled
   - Evaporative

7. Receivers
   - Liquid
   - Suction

8. Filters
   - Liquid
   - Suction
   - Oil

9. Racks
   - Parallel
   - Distributed
   - Centralized
   - Modular

10. Cases
    - Reach-in
    - Walk-in
    - Display
    - Prep

11. Heaters
    - Defrost
    - Anti-sweat
    - Case
    - Evaporator

### Manufacturers
1. Component Manufacturers
   - Copeland
   - Danfoss
   - Ebm-papst
   - Bitzer
   - Sporlan
   - Ziehl-Abegg
   - Alco
   - Emerson
   - Carel
   - Honeywell
   - Johnson Controls
   - Refcomp
   - Tecumseh
   - Dixell
   - Kelvion
   - LU-VE
   - Frick
   - Vilter
   - York
   - Trane

2. Rack System Manufacturers
   - Hillphoenix
   - Hussmann
   - KeepRite
   - Heatcraft
   - Larkin
   - Zero Zone
   - Arneg
   - MetalFrio
   - Carrier
   - Lennox
   - KE2

## Usage

1. Place PDF manuals in `manuals/raw/`
2. Run manual processor:
   ```bash
   python scripts/manual_processor.py
   ```
3. Validate mappings:
   ```bash
   python scripts/validate_mappings.py
   ```

## Environment Variables
Required environment variables:
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_ANON_KEY`: Supabase anonymous key
- `OPENAI_API_KEY`: OpenAI API key for embeddings 