# Architecture Overview

## The 5-Node Agentic Pipeline

The core architectural triumph of this platform is the `StudioState` LangGraph orchestrator. By modeling the creative pipeline as a strict deterministic state machine, we enforce robust continuity and guarantee human oversight.

### 1. Extraction Node
The LLM processes the source document and extracts Canonical Entities. A deterministic python wrapper standardizes these entities into dictionaries containing `id`, `name`, `aliases`, and `role`. 

### 2. Deterministic Validation Node
Rather than relying on the LLM to hallucinate state transitions, the system utilizes a deterministic `ContinuityValidator` Python class to track object possession across scenes and surface contradictions as warnings.

### 3. Cultural RAG Node & Planning
The system bypasses generic LLM hallucinations by embedding curated cultural handbooks into a local **ChromaDB**. We execute semantic queries (`all-MiniLM-L6-v2`) against the database to fetch highly specific cultural rules (Wardrobe, Kinship, Architecture) and inject them into the Adaptation Planning prompt.

### 4. Adaptation Node
Using the human-approved Cultural Plan, the LLM rewrites the screenplay snippet.

### 5. Visual Prompt Node & Generation
The LLM generates a visual prompt combining the approved Scene context with Canonical Character rules. The `ImageGenerationService` fires an HTTP POST request to a Stable Diffusion API to generate the asset.

## Technology Stack
- **State Machine**: LangGraph (Python)
- **API Layer**: FastAPI (Uvicorn)
- **Vector Store**: ChromaDB 
- **LLM Engine**: Ollama (Qwen 2.5)
- **Frontend**: Vue.js, Tailwind CSS, Vue Router
