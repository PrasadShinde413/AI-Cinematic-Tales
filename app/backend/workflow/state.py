from typing import TypedDict, List, Dict, Any, Optional

class StudioState(TypedDict):
    project_id: str
    adaptation_id: str
    culture_id: str

    source_document: Dict[str, Any]
    
    scenes: List[Dict[str, Any]]
    characters: List[Dict[str, Any]]
    locations: List[Dict[str, Any]]
    props: List[Dict[str, Any]]
    costumes: List[Dict[str, Any]]
    
    continuity_state: Dict[str, Any]
    
    selected_culture: Dict[str, Any]
    cultural_evidence: List[Dict[str, Any]]
    adaptation_plan: Dict[str, Any]
    
    approval_status: Dict[str, Any]
    
    adapted_screenplay: Dict[str, Any]
    
    visual_prompts: List[Dict[str, Any]]
    generated_assets: List[Dict[str, Any]]
    
    continuity_results: List[Dict[str, Any]]
    visual_validation_results: List[Dict[str, Any]]
    
    errors: List[Dict[str, Any]]
