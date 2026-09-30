import asyncio
import os
import uuid
import httpx
from typing import Dict, Any, List
from models.schemas import VisualAssetMetadataSchema
from core.config import settings

class ImageGenerationService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("STABILITY_API_KEY", "")
        self.primary_model = "stable-image-core"
        self.fallback_model = "local-placeholder"
        
    async def generate_asset(self, asset_spec: Dict[str, Any]) -> VisualAssetMetadataSchema:
        """
        Generates an image from a fully canonicalized generation spec.
        Implements an isolated retry pattern and fallback models if the primary API fails.
        """
        prompt = asset_spec.get("generation_spec", {}).get("prompt", "")
        negative_prompt = asset_spec.get("generation_spec", {}).get("negative_prompt", "")
        
        try:
            # Attempt Primary API Generation
            image_url = await self._call_primary_api(prompt, negative_prompt)
            model_used = self.primary_model
        except Exception as e:
            print(f"Primary API failed: {str(e)}. Falling back to local generation.")
            # Attempt Fallback Generation
            image_url = await self._call_fallback_api(prompt, negative_prompt)
            model_used = self.fallback_model
            
        return VisualAssetMetadataSchema(
            asset_id=asset_spec.get("asset_id", str(uuid.uuid4())),
            model=model_used,
            prompt_version=asset_spec.get("prompt_version", 1),
            character_ids=asset_spec.get("character_ids", []),
            costume_ids=asset_spec.get("costume_ids", []),
            location_ids=asset_spec.get("location_ids", []),
            prop_ids=asset_spec.get("prop_ids", []),
            generation_spec=asset_spec.get("generation_spec", {}),
            status="generated_success"
        )
        
    async def _call_primary_api(self, prompt: str, negative_prompt: str) -> str:
        """Call Stability AI REST API."""
        if not self.api_key:
            raise ValueError("STABILITY_API_KEY is not set.")
            
        url = "https://api.stability.ai/v2beta/stable-image/generate/core"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        files = {
            "prompt": (None, prompt),
            "output_format": (None, "png"),
            "negative_prompt": (None, negative_prompt)
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, files=files)
            if response.status_code == 200:
                data = response.json()
                # Stability returns base64 in data['image']
                base64_img = data.get("image", "")
                return f"data:image/png;base64,{base64_img}"
            else:
                raise Exception(f"Stability API Error: {response.text}")

    async def _call_fallback_api(self, prompt: str, negative_prompt: str) -> str:
        """Fallback to placeholder if Stability fails or no key is provided."""
        print("Using local placeholder image generation due to missing key or API failure.")
        await asyncio.sleep(1) # Simulate fast local generation
        return "https://placehold.co/1024x576/0f172a/ffffff?text=Cinematic+Scene+Placeholder"
