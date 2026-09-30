# Known Limitations

While this MVP fully proves the viability of an agentic adaptation studio, there are a few intentional architectural shortcuts taken to fit within local processing constraints and the 48-hour challenge window.

## 1. Context Window & LLM Size (`qwen2.5:0.5b`)
This application operates entirely locally on extremely restricted hardware, utilizing a 0.5 billion parameter model. 
- **JSON Schema Frailty**: Qwen 0.5b severely struggles to output deeply nested, strict JSON arrays. Because of this, the `extraction_node` is currently limited to extracting Character Names only, rather than attempting to extract highly complex state objects like Props and Costumes.
- **Mitigation Strategy**: The architecture of the `ContinuityValidator` is fully written and tested to handle strict Costume/Prop state transitions. When a larger production model (e.g., `gpt-4o` or `claude-3.5-sonnet`) is slotted into `llm = ChatOpenAI()`, the extraction node can immediately output the required schema to unlock full continuity tracking.

## 2. RAG Evaluation Stubbing
The `run_evals.py` suite contains fully written tests for **DeepEval** (`FaithfulnessMetric`) and **Ragas** (`context_precision`). 
- However, since these frameworks inherently mandate OpenAI API keys to perform LLM-as-a-judge scoring, the script includes graceful exception handling to prevent hard crashes when executed locally. 
- In a production cloud environment, these evals would run asynchronously on every pipeline execution.

## 3. Simplified PDF Generation
Currently, the Export view provides a downloadable ZIP (`submission_export.zip`) containing static representations of the required output files to demonstrate the final user flow. Server-side PDF generation tools (like ReportLab or WeasyPrint) were excluded from this MVP to minimize dependency bloat.
