from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ContinuityEventSchema(BaseModel):
    event_id: str
    entity_id: str
    entity_type: str
    scene_id: str
    previous_holder: Optional[str] = None
    new_holder: Optional[str] = None
    previous_state: Optional[str] = None
    new_state: Optional[str] = None
    reason: str
    status: str

class RAGEvidenceSchema(BaseModel):
    evidence_id: str
    content: str
    category: str
    source: str
    retrieval_score: float
    verification_status: str

class AdaptationDecisionSchema(BaseModel):
    scene_id: str
    adapted_text: str
    adaptation_reason: str
    cultural_evidence: List[RAGEvidenceSchema]
    confidence_level: str # HIGH, MEDIUM, LOW

class VisualAssetMetadataSchema(BaseModel):
    asset_id: str
    model: str
    prompt_version: int
    character_ids: List[str] = []
    costume_ids: List[str] = []
    location_ids: List[str] = []
    prop_ids: List[str] = []
    generation_spec: Dict[str, Any]
    status: str

# --- NEW GROQ JSON SCHEMAS FOR CHALLENGE COMPLIANCE ---

class SceneBreakdownSchema(BaseModel):
    scene_id: str = Field(description="Unique ID like SC01")
    scene_number: int
    type: str = Field(description="INT or EXT")
    location: str
    time: str
    weather: str
    mood: str
    summary: str
    dramatic_purpose: str
    characters: List[str] = Field(description="List of Canonical Character IDs in this scene")
    props: List[str] = Field(description="List of Prop IDs in this scene")

class CanonicalCharacterSchema(BaseModel):
    character_id: str = Field(description="Canonical ID like CHAR_GURPREET")
    canonical_name: str = Field(description="The culturally adapted name")
    source_identity: str = Field(description="The original name from the source text")
    age: int = Field(description="Estimated or adapted age")
    role: str
    aliases: List[str]
    relationships: List[str]
    dialect: str
    emotional_state: Dict[str, str] = Field(description="Mapping of Scene IDs to emotional states")

class CharacterExtractionSchema(BaseModel):
    characters: List[CanonicalCharacterSchema]

class ContinuityIssueSchema(BaseModel):
    type: str
    severity: str = Field(description="HIGH, MEDIUM, LOW")
    scene: str
    message: str

class ContinuityReportSchema(BaseModel):
    continuity_status: str = Field(description="PASS, PASS_WITH_WARNINGS, or FAIL")
    issues: List[ContinuityIssueSchema]

class CulturalAdaptationRuleSchema(BaseModel):
    category: str = Field(description="CHARACTER, DIALOGUE, KINSHIP, ENVIRONMENT, CLOTHING, etc.")
    source: Optional[str] = None
    adapted: str
    reason: str

class CulturalAdaptationPlanSchema(BaseModel):
    culture: str
    region: str
    setting: str
    adaptations: List[CulturalAdaptationRuleSchema]

class CharacterBibleAppearanceSchema(BaseModel):
    face: str
    hair: str
    facial_hair: str
    build: str

class CharacterBibleCostumeSchema(BaseModel):
    primary: str
    footwear: str

class CharacterBibleSchema(BaseModel):
    character_id: str
    name: str
    age: int
    gender: str
    appearance: CharacterBibleAppearanceSchema
    costume: CharacterBibleCostumeSchema
    visual_reference: str

class ProductionPackSchema(BaseModel):
    character_bibles: List[CharacterBibleSchema]
