from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from services.export_service import ExportService
from api.routes import router as workflow_router

app = FastAPI(
    title="Cultural Screenplay and Visual Adaptation Studio",
    description="Agentic MVP for Screenplay Adaptation",
    version="1.0.0"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the LangGraph Workflow Routes
app.include_router(workflow_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the Cultural Screenplay Adaptation Studio API"}

@app.get("/api/export")
async def export_zip():
    # Provide mock state for the export service to zip up
    mock_state = {
        "adapted_screenplay": "Mock Screenplay Text",
        "scenes": [{"scene_id": "SC01", "summary": "Initial Scene"}],
        "continuity_results": [{"status": "PASS"}],
        "adaptation_plan": {"culture": "malwai", "decisions": []},
        "cultural_evidence": [],
        "generated_assets": [
            {"asset_id": "CHAR_AMAR_01", "model": "mock"},
            {"asset_id": "SC01_IMG01", "model": "mock"}
        ]
    }
    export_svc = ExportService(mock_state)
    zip_buffer = export_svc.generate_export_zip()
    
    return StreamingResponse(
        zip_buffer, 
        media_type="application/zip", 
        headers={"Content-Disposition": "attachment; filename=submission_export.zip"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
