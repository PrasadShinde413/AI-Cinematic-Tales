import chromadb
from chromadb.config import Settings
from models.schemas import RAGEvidenceSchema
from core.config import settings
from typing import List, Dict, Any

class RAGService:
    def __init__(self):
        # Initialize ChromaDB client using the persist directory from settings
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        
    def get_or_create_collection(self, culture_id: str):
        """
        Collections are strictly isolated by culture_id to prevent any accidental leakage.
        """
        # We use a simple local embedding function by default
        return self.client.get_or_create_collection(name=f"culture_{culture_id.lower()}")

    def add_cultural_evidence(self, culture_id: str, evidence_list: List[Dict[str, Any]]):
        """
        Ingest cultural facts with exact source citations and categories.
        """
        collection = self.get_or_create_collection(culture_id)
        
        ids = []
        documents = []
        metadatas = []
        
        for ev in evidence_list:
            ids.append(ev["evidence_id"])
            documents.append(ev["content"])
            metadatas.append({
                "category": ev["category"],
                "source": ev["source"],
                "verification_status": ev.get("verification_status", "unverified")
            })
            
        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def retrieve_evidence(self, culture_id: str, query: str, category: str = None, top_k: int = 3) -> List[RAGEvidenceSchema]:
        """
        Retrieves cultural evidence with strict category filtering and retrieval scores.
        """
        collection = self.get_or_create_collection(culture_id)
        
        where_clause = {}
        if category:
            where_clause["category"] = category
            
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where_clause if where_clause else None
        )
        
        extracted_evidence = []
        if results and results.get("ids") and len(results["ids"]) > 0:
            for idx, doc_id in enumerate(results["ids"][0]):
                meta = results["metadatas"][0][idx]
                distance = results["distances"][0][idx] if "distances" in results else 0.0
                
                # Convert distance to a pseudo-confidence score (1 - normalized distance)
                # Note: This is an approximation; Chroma uses L2/Cosine. 
                retrieval_score = round(max(0.0, 1.0 - (distance / 2.0)), 2)
                
                doc = results["documents"][0][idx] if "documents" in results else ""
                
                extracted_evidence.append(
                    RAGEvidenceSchema(
                        evidence_id=doc_id,
                        content=doc,
                        category=meta.get("category", "general"),
                        source=meta.get("source", "unknown"),
                        retrieval_score=retrieval_score,
                        verification_status=meta.get("verification_status", "unverified")
                    )
                )
                
        return extracted_evidence
