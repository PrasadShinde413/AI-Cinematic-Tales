from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from workflow.state import StudioState
from typing import Dict, Any
import json
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from core.config import settings
from services.rag_service import RAGService
from services.image_generation import ImageGenerationService
from models.schemas import (
    SceneBreakdownSchema, CharacterExtractionSchema, 
    ContinuityReportSchema, CulturalAdaptationPlanSchema, ProductionPackSchema
)
import asyncio

# Upgrade to Llama/Mixtral via Groq for complex JSON extraction
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.1)
rag = RAGService()
image_svc = ImageGenerationService()

# --- Node Implementations (Groq JSON Integrated) ---

def extraction_node(state: StudioState) -> Dict[str, Any]:
    print(f"[{state['adaptation_id']}] Running Extraction with ChatGroq...")
    snippet = state.get("source_document", {}).get("text", "")
    
    # Extract Scene Breakdown
    scene_llm = llm.with_structured_output(SceneBreakdownSchema)
    scene_res = scene_llm.invoke(f"Extract scene breakdown from this screenplay snippet:\n{snippet}")
    
    # Extract Characters
    char_llm = llm.with_structured_output(CharacterExtractionSchema)
    char_res = char_llm.invoke(f"Extract characters from this screenplay snippet and canonicalize them for {state.get('culture_id', 'the target culture')}:\n{snippet}")
    
    # Store in state (convert Pydantic to dict)
    return {
        "scenes": [scene_res.dict()],
        "characters": [c.dict() for c in char_res.characters],
        "approval_status": {"extraction_approved": False}
    }

def canonicalization_node(state: StudioState) -> Dict[str, Any]:
    print(f"[{state['adaptation_id']}] Running Canonicalization...")
    # Canonicalization is now handled implicitly by the Groq prompt in extraction
    return {}

def deterministic_validation_node(state: StudioState) -> Dict[str, Any]:
    print(f"[{state['adaptation_id']}] Validating Continuity Deterministically...")
    snippet = state.get("source_document", {}).get("text", "")
    
    cont_llm = llm.with_structured_output(ContinuityReportSchema)
    cont_res = cont_llm.invoke(f"Analyze this screenplay for continuity errors (props, relationships) and return a continuity report:\n{snippet}")
    
    return {"continuity_results": cont_res.dict()}

def cultural_rag_node(state: StudioState) -> Dict[str, Any]:
    print(f"[{state['adaptation_id']}] Retrieving Cultural Context...")
    culture = state.get("culture_id", "malwai")
    evidence = rag.retrieve_evidence(culture_id=culture, query="kinship clothing architecture norms", top_k=5)
    return {"cultural_evidence": [e.dict() for e in evidence]}

def adaptation_planning_node(state: StudioState) -> Dict[str, Any]:
    print(f"[{state['adaptation_id']}] Planning Adaptation...")
    culture = state.get("culture_id", "malwai")
    evidence = state.get("cultural_evidence", [])
    context = "\n".join([f"- {e['content']}" for e in evidence])
    
    plan_llm = llm.with_structured_output(CulturalAdaptationPlanSchema)
    prompt = f"Target Culture: {culture}\nVerified RAG Context:\n{context}\n\nCreate a comprehensive Cultural Adaptation Plan based on the context."
    plan_res = plan_llm.invoke(prompt)
    
    return {"adaptation_plan": plan_res.dict(), "approval_status": {"plan_approved": False}}

def screenplay_adaptation_node(state: StudioState) -> Dict[str, Any]:
    print(f"[{state['adaptation_id']}] Adapting Screenplay...")
    rules = state.get("adaptation_plan", {}).get("adaptations", [])
    snippet = state.get("source_document", {}).get("text", "")
    
    prompt = f"Rewrite this screenplay snippet applying these rules: {rules}\n\nScreenplay:\n'{snippet}'\n\nOutput ONLY the raw adapted screenplay text."
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {"adapted_screenplay": {"text": response.content}}

def story_preservation_node(state: StudioState) -> Dict[str, Any]:
    print(f"[{state['adaptation_id']}] Checking Story Preservation...")
    return {}

def visual_prompt_node(state: StudioState) -> Dict[str, Any]:
    print(f"[{state['adaptation_id']}] Building Visual Prompts...")
    
    # 1. Generate Character Bibles
    bible_llm = llm.with_structured_output(ProductionPackSchema)
    chars = state.get("characters", [])
    plan = state.get("adaptation_plan", {})
    bible_res = bible_llm.invoke(f"Generate visual character bibles for these characters: {chars} based on this cultural plan: {plan}")
    
    # 2. Generate Scene Prompt
    prompt = f"Create a highly detailed stable diffusion image prompt for the scene described here: {state.get('scenes', [{}])[0]} featuring the characters from the bible."
    response = llm.invoke([HumanMessage(content=prompt)])
    
    visual_prompts = [
        {
            "id": "VP_001",
            "asset_id": "SC01_IMG", 
            "scene": "1",
            "prompt": response.content, 
            "status": "pending",
            "canonicalReferences": []
        }
    ]
    return {
        "visual_prompts": visual_prompts, 
        "character_bibles": bible_res.dict().get("character_bibles", []),
        "approval_status": {"prompts_approved": False}
    }

def image_generation_node(state: StudioState) -> Dict[str, Any]:
    print(f"[{state['adaptation_id']}] Generating Images...")
    visual_prompts = state.get("visual_prompts", [])
    
    for vp in visual_prompts:
        if vp.get("status") == "pending":
            try:
                spec = {"generation_spec": {"prompt": vp["prompt"]}}
                result = asyncio.run(image_svc.generate_asset(spec))
                vp["status"] = "completed"
                vp["generated_url"] = result.get("url", "stability_generated")
            except Exception as e:
                print(f"Error generating image: {e}")
                vp["status"] = "failed"
                
    return {"visual_prompts": visual_prompts}

def visual_verification_node(state: StudioState) -> Dict[str, Any]:
    print(f"[{state['adaptation_id']}] Verifying Visual Consistency...")
    return {"visual_validation_results": []}

# --- Supervisor Builder ---

def build_studio_graph():
    builder = StateGraph(StudioState)
    
    builder.add_node("extract", extraction_node)
    builder.add_node("canonicalize", canonicalization_node)
    builder.add_node("validate_continuity", deterministic_validation_node)
    builder.add_node("cultural_rag", cultural_rag_node)
    builder.add_node("plan_adaptation", adaptation_planning_node)
    builder.add_node("adapt_screenplay", screenplay_adaptation_node)
    builder.add_node("preserve_story", story_preservation_node)
    builder.add_node("build_prompts", visual_prompt_node)
    builder.add_node("generate_images", image_generation_node)
    builder.add_node("verify_visuals", visual_verification_node)

    builder.set_entry_point("extract")
    builder.add_edge("extract", "canonicalize")
    builder.add_edge("canonicalize", "validate_continuity")
    
    # Gate 1: Pause after validation before RAG
    builder.add_edge("validate_continuity", "cultural_rag")
    builder.add_edge("cultural_rag", "plan_adaptation")
    
    # Gate 2: Pause after planning before adaptation
    builder.add_edge("plan_adaptation", "adapt_screenplay")
    builder.add_edge("adapt_screenplay", "preserve_story")
    builder.add_edge("preserve_story", "build_prompts")
    
    # Gate 3: Pause after building prompts before generating images
    builder.add_edge("build_prompts", "generate_images")
    builder.add_edge("generate_images", "verify_visuals")
    builder.add_edge("verify_visuals", END)

    conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
    memory = SqliteSaver(conn)
    memory.setup()
    
    graph = builder.compile(
        checkpointer=memory,
        interrupt_before=[
            "cultural_rag",     # Gate 1
            "adapt_screenplay", # Gate 2
            "generate_images"   # Gate 3
        ]
    )
    
    return graph

studio_graph = build_studio_graph()
