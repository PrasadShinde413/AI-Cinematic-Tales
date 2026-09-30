import os
import json
import zipfile
from io import BytesIO
from typing import Dict, Any, List

class ExportService:
    def __init__(self, state_data: Dict[str, Any]):
        self.state = state_data
        
    def generate_export_zip(self) -> BytesIO:
        """
        Generates the strictly formatted submission_export.zip file.
        Includes complete audit trails, metadata, reports, and generated images.
        """
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            
            # 1. Core Documents (PDFs mocked as text files for this example)
            zip_file.writestr("adapted_screenplay.txt", str(self.state.get("adapted_screenplay", {})))
            zip_file.writestr("scene_breakdown.json", json.dumps(self.state.get("scenes", []), indent=2))
            zip_file.writestr("continuity_report.txt", str(self.state.get("continuity_results", [])))
            
            # 2. Audit Trail
            zip_file.writestr("adaptation_plan.json", json.dumps(self.state.get("adaptation_plan", {}), indent=2))
            zip_file.writestr("cultural_evidence.json", json.dumps(self.state.get("cultural_evidence", []), indent=2))
            zip_file.writestr("generation_manifest.json", json.dumps(self.state.get("generated_assets", []), indent=2))
            
            # 3. Visual Assets (Mocked image files)
            for asset in self.state.get("generated_assets", []):
                asset_id = asset.get("asset_id", "UNKNOWN")
                
                # We would normally write the actual bytes from image_path here.
                # Here we drop a tiny metadata marker in the correct folder based on its contents.
                if "CHAR" in asset_id:
                    zip_file.writestr(f"character_bible/{asset_id}.json", json.dumps(asset, indent=2))
                    zip_file.writestr(f"character_bible/{asset_id}.txt", f"Mock Image Data for {asset_id}")
                elif "COST" in asset_id:
                    zip_file.writestr(f"costume_bible/{asset_id}.json", json.dumps(asset, indent=2))
                    zip_file.writestr(f"costume_bible/{asset_id}.txt", f"Mock Image Data for {asset_id}")
                elif "SC" in asset_id:
                    zip_file.writestr(f"scene_keyframes/{asset_id}.json", json.dumps(asset, indent=2))
                    zip_file.writestr(f"scene_keyframes/{asset_id}.txt", f"Mock Image Data for {asset_id}")
                else:
                    zip_file.writestr(f"other/{asset_id}.json", json.dumps(asset, indent=2))
                    
        zip_buffer.seek(0)
        return zip_buffer
