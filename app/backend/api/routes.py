from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import uuid
import uuid
import io
import zipfile
import json
from fastapi.responses import StreamingResponse
from workflow.orchestrator import studio_graph

router = APIRouter()

# Memory store for active runs
active_sessions = {}

class ApprovalRequest(BaseModel):
    gate_name: str
    approved: bool
    modifications: dict = {}

@router.post("/upload")
async def upload_screenplay(file: UploadFile = File(...), culture_id: str = "malwai"):
    """
    Ingests the file and kicks off the LangGraph workflow up to Gate 1 (extract).
    """
    content = await file.read()
    project_id = str(uuid.uuid4())
    
    # Initialize State
    initial_state = {
        "project_id": project_id,
        "adaptation_id": f"ADAPT_{project_id[:8]}",
        "culture_id": culture_id,
        "source_document": {"filename": file.filename, "text": content.decode("utf-8", errors="ignore")},
        "characters": [],
        "scenes": [],
        "adaptation_plan": {},
        "adapted_screenplay": {},
        "visual_prompts": []
    }
    
    # Configure graph thread for MemorySaver
    config = {"configurable": {"thread_id": project_id}}
    
    # Run the graph until the first interrupt (Gate 1)
    for event in studio_graph.stream(initial_state, config=config):
        pass # Stream executes the graph
        
    active_sessions[project_id] = config
    return {"project_id": project_id, "status": "waiting_for_gate_1"}

@router.get("/state/{project_id}")
async def get_state(project_id: str):
    """
    Retrieves the current state of the LangGraph execution.
    """
    config = active_sessions.get(project_id)
    if not config:
        raise HTTPException(status_code=404, detail="Project not found")
        
    state = studio_graph.get_state(config)
    return state.values

@router.post("/approve/{project_id}")
async def approve_gate(project_id: str, req: ApprovalRequest):
    """
    Approves a gate and resumes the LangGraph workflow.
    """
    config = active_sessions.get(project_id)
    if not config:
        raise HTTPException(status_code=404, detail="Project not found")
        
    # Apply any human modifications to the state before resuming
    if req.modifications:
        studio_graph.update_state(config, req.modifications)
        
    # Resume the graph by passing None to the interrupted node
    for event in studio_graph.stream(None, config=config):
        pass
        
    return {"status": "resumed", "gate": req.gate_name}

@router.get("/export/{project_id}")
async def export_project(project_id: str):
    """
    Builds the final submission_export.zip containing all required artifacts.
    """
    config = active_sessions.get(project_id)
    if not config:
        raise HTTPException(status_code=404, detail="Project not found")
        
    state = studio_graph.get_state(config).values
    
    # Create in-memory ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        
        # 1. Adapted Screenplay
        adapted_text = state.get("adapted_screenplay", {}).get("text", "")
        zip_file.writestr("adapted_screenplay.txt", adapted_text)
        
        # 2. Scene Breakdown
        scenes = state.get("scenes", [])
        zip_file.writestr("scene_breakdown.json", json.dumps({"scenes": scenes}, indent=2))
        
        # 3. Continuity Report
        continuity = state.get("continuity_results", {})
        zip_file.writestr("continuity_report.json", json.dumps(continuity, indent=2))
        
        # 4. Adaptation Plan
        plan = state.get("adaptation_plan", {})
        zip_file.writestr("adaptation_plan.json", json.dumps(plan, indent=2))
        
        # 5. Cultural Evidence
        evidence = state.get("cultural_evidence", [])
        zip_file.writestr("cultural_evidence.json", json.dumps({"evidence": evidence}, indent=2))
        
        # 6. Character Bibles
        characters = state.get("characters", [])
        for char in characters:
            char_id = char.get("character_id", "UNKNOWN")
            zip_file.writestr(f"character_bible/{char_id}.json", json.dumps(char, indent=2))
            
        # 7. Visual Prompts & Manifest
        prompts = state.get("visual_prompts", [])
        zip_file.writestr("generation_manifest.json", json.dumps({"prompts": prompts}, indent=2))

    zip_buffer.seek(0)
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=submission_export.zip"}
    )
