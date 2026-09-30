from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Adaptation(Base):
    __tablename__ = "adaptations"
    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"))
    culture_id = Column(String, index=True)  # e.g., "MALWAI"
    status = Column(String, default="planning")
    
    project = relationship("Project")

class Scene(Base):
    __tablename__ = "scenes"
    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"))
    adaptation_id = Column(String, ForeignKey("adaptations.id"), nullable=True) # None for source scenes
    scene_number = Column(Integer)
    int_ext = Column(String)
    location_desc = Column(String)
    time_desc = Column(String)
    summary = Column(String)
    dramatic_purpose = Column(String)

class CanonicalEntity(Base):
    __tablename__ = "canonical_entities"
    id = Column(String, primary_key=True) # e.g., CHAR_AMAR
    project_id = Column(String, ForeignKey("projects.id"))
    adaptation_id = Column(String, ForeignKey("adaptations.id"), nullable=True)
    entity_type = Column(String) # "character", "location", "prop", "costume"
    name = Column(String)
    metadata_json = Column(JSON) # age, role, relationships, etc.

class CharacterAlias(Base):
    __tablename__ = "character_aliases"
    id = Column(String, primary_key=True, default=generate_uuid)
    canonical_id = Column(String, ForeignKey("canonical_entities.id"))
    alias_name = Column(String)

class ContinuityEvent(Base):
    __tablename__ = "continuity_events"
    id = Column(String, primary_key=True, default=generate_uuid)
    adaptation_id = Column(String, ForeignKey("adaptations.id"))
    scene_id = Column(String, ForeignKey("scenes.id"))
    entity_id = Column(String, ForeignKey("canonical_entities.id"))
    entity_type = Column(String)
    previous_holder = Column(String, nullable=True)
    new_holder = Column(String, nullable=True)
    previous_state = Column(String, nullable=True)
    new_state = Column(String, nullable=True)
    reason = Column(String)
    status = Column(String) # valid, warning, contradiction

class VisualAsset(Base):
    __tablename__ = "visual_assets"
    id = Column(String, primary_key=True, default=generate_uuid)
    adaptation_id = Column(String, ForeignKey("adaptations.id"))
    asset_type = Column(String) # character, costume, scene
    scene_id = Column(String, ForeignKey("scenes.id"), nullable=True)
    character_ids = Column(JSON) # List of canonical IDs
    costume_ids = Column(JSON)
    location_ids = Column(JSON)
    prop_ids = Column(JSON)
    prompt_version = Column(Integer, default=1)
    generation_spec = Column(JSON) # prompt, negative_prompt, model
    image_path = Column(String)
    status = Column(String, default="pending") # pending, approved, rejected
