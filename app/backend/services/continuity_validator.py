from typing import List, Dict, Any
from models.schemas import ContinuityEventSchema
from pydantic import ValidationError

class ContinuityValidator:
    def __init__(self):
        # In memory state cache for the current validation run
        self.entity_states: Dict[str, Dict[str, Any]] = {}
        self.validation_errors: List[Dict[str, Any]] = []

    def validate_scene_transitions(self, events: List[ContinuityEventSchema]) -> List[Dict[str, Any]]:
        """
        Deterministically validate state transitions across continuity events.
        """
        for event in events:
            entity_id = event.entity_id
            
            # Initialize entity state if not seen yet
            if entity_id not in self.entity_states:
                self.entity_states[entity_id] = {
                    "current_holder": event.previous_holder,
                    "current_state": event.previous_state,
                    "last_scene_id": None
                }
            
            current_tracker = self.entity_states[entity_id]
            
            # Check for contradiction: Does the event's declared previous state match our known current state?
            # We ignore None checks for initial states.
            if event.previous_holder and current_tracker["current_holder"] and event.previous_holder != current_tracker["current_holder"]:
                self._add_error(
                    event.scene_id, 
                    entity_id, 
                    f"Contradiction: {entity_id} was held by {current_tracker['current_holder']}, but event claims it was held by {event.previous_holder}"
                )
                
            if event.previous_state and current_tracker["current_state"] and event.previous_state != current_tracker["current_state"]:
                self._add_error(
                    event.scene_id,
                    entity_id,
                    f"Contradiction: {entity_id} state was {current_tracker['current_state']}, but event claims it was {event.previous_state}"
                )
                
            # Transition state
            if event.new_holder:
                current_tracker["current_holder"] = event.new_holder
            if event.new_state:
                current_tracker["current_state"] = event.new_state
                
            current_tracker["last_scene_id"] = event.scene_id
            
        return self.validation_errors

    def _add_error(self, scene_id: str, entity_id: str, message: str):
        self.validation_errors.append({
            "scene_id": scene_id,
            "entity_id": entity_id,
            "error": message,
            "type": "continuity_contradiction"
        })
