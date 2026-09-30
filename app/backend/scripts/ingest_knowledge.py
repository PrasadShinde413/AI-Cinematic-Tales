import os
import sys
from pathlib import Path

# Add backend directory to sys.path so we can import services
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from services.rag_service import RAGService
import uuid

def ingest_malwai_culture():
    print("Initializing RAG Service...")
    rag = RAGService()
    
    data_path = backend_dir / "data" / "malwai_culture.txt"
    if not data_path.exists():
        print(f"Error: {data_path} not found.")
        return
        
    with open(data_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    print("Splitting text into chunks...")
    # Split by section natively to avoid heavy imports crashing
    chunks = [c.strip() for c in text.split("Section") if c.strip()]
    
    print(f"Generated {len(chunks)} semantic chunks. Upserting to ChromaDB...")
    
    evidence_list = []
    for i, chunk in enumerate(chunks):
        category = "general"
        if "Kinship" in chunk or "greeting" in chunk.lower():
            category = "kinship"
        elif "Wardrobe" in chunk or "wear" in chunk.lower():
            category = "wardrobe"
        elif "Architecture" in chunk or "setting" in chunk.lower():
            category = "setting"
            
        print(f"Loop {i}: appending chunk")
        evidence_list.append({
            "evidence_id": f"KB_MALWAI_{i+1:03d}",
            "content": chunk.strip(),
            "category": category,
            "source": "malwai_culture.txt",
            "verification_status": "verified"
        })
        
    print(f"Calling add_cultural_evidence with {len(evidence_list)} items...")
    rag.add_cultural_evidence("malwai", evidence_list)
    print(f"Successfully ingested {len(chunks)} verified facts into the 'culture_malwai' vector collection.")

if __name__ == "__main__":
    print("Starting script...")
    ingest_malwai_culture()
    print("Script finished!")
