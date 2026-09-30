import pytest
from services.continuity_validator import ContinuityValidator
from models.schemas import ContinuityEventSchema

def test_continuity_contradiction():
    validator = ContinuityValidator()
    
    # Event 1: Amar carries letter in SC01
    event1 = ContinuityEventSchema(
        event_id="E1",
        entity_id="PROP_LETTER",
        entity_type="prop",
        scene_id="SC01",
        previous_holder=None,
        new_holder="CHAR_AMAR",
        previous_state=None,
        new_state="carried",
        reason="Amar receives letter",
        status="valid"
    )
    
    # Event 2: Amar gives letter to Bebe in SC02
    event2 = ContinuityEventSchema(
        event_id="E2",
        entity_id="PROP_LETTER",
        entity_type="prop",
        scene_id="SC02",
        previous_holder="CHAR_AMAR",
        new_holder="CHAR_BEBE",
        previous_state="carried",
        new_state="carried",
        reason="Amar hands it to Bebe",
        status="valid"
    )
    
    # Event 3: Amar somehow has the letter again in SC03 WITHOUT a transfer
    event3 = ContinuityEventSchema(
        event_id="E3",
        entity_id="PROP_LETTER",
        entity_type="prop",
        scene_id="SC03",
        previous_holder="CHAR_AMAR", # CONTRADICTION: Should be Bebe
        new_holder=None,
        previous_state="carried",
        new_state="destroyed",
        reason="Amar burns letter",
        status="valid"
    )
    
    errors = validator.validate_scene_transitions([event1, event2, event3])
    
    assert len(errors) == 1
    assert errors[0]["scene_id"] == "SC03"
    assert "Contradiction" in errors[0]["error"]
    assert "held by CHAR_BEBE" in errors[0]["error"]
