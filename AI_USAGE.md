# AI Usage & Verification Log

## AI Assistants Utilized
This project was developed with the assistance of **Google Antigravity (Agentic AI)**.

## Role of the AI
The AI acted as a pair-programming senior engineer. It was responsible for:
- Scaffolding the initial Vite/Vue frontend and FastAPI backend.
- Writing the underlying LangGraph state machine definitions (`StateGraph`, `MemorySaver`).
- Wiring the frontend fetch requests to the backend APIs.
- Designing the ChromaDB RAG abstraction layer.

## Verification & Correction
- **Issue**: The AI initially built the `AdaptationView.vue` by mocking hardcoded JSON field wrappers (`confidence: HIGH`) around simple LLM strings. 
- **Verification**: Manual UI auditing revealed the static nature of the UI.
- **Correction**: The AI was instructed to refactor the Python `orchestrator.py` to intelligently parse the LLM strings into full dictionaries, removing all mocked logic from the Vue components.

- **Issue**: The AI used a native `placehold.co` image URL for the Image Generation node, which failed to render due to browser privacy policies.
- **Correction**: The AI refactored the image generation service to seamlessly integrate with `image.pollinations.ai`, providing true, keyless dynamic Stable Diffusion imagery.
