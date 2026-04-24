import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from chromadb import PersistentClient, Collection
from langchain_openai import OpenAIEmbeddings

class ShortTermMemory:
    """Sliding window of recent messages."""
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.capacity:
            self.messages = self.messages[-self.capacity:]

    def get_messages(self) -> List[Dict[str, str]]:
        return self.messages

class LongTermProfile:
    """KV store for user attributes with conflict handling."""
    def __init__(self, file_path: str = "user_profile.json"):
        self.file_path = file_path
        self.profile = self._load()

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.profile, f, indent=4, ensure_ascii=False)

    def update_fact(self, key: str, value: Any):
        # Direct update handles conflict by overwriting
        self.profile[key] = value
        self.save()

    def get_profile(self) -> Dict[str, Any]:
        return self.profile

class EpisodicMemory:
    """Log of key interactions and outcomes."""
    def __init__(self, file_path: str = "episodes.json"):
        self.file_path = file_path
        self.episodes = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.episodes, f, indent=4, ensure_ascii=False)

    def add_episode(self, summary: str, outcome: str):
        self.episodes.append({
            "summary": summary,
            "outcome": outcome,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save()

    def get_episodes(self, limit: int = 5) -> List[Dict[str, Any]]:
        return self.episodes[-limit:]

class SemanticMemory:
    """Vector store for factual retrieval."""
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = PersistentClient(path=persist_directory)
        self.embeddings = OpenAIEmbeddings() 
        self.collection = self.client.get_or_create_collection(name="facts")

    def add_fact(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        # In a real app, we would embed the text
        # For this lab, we can simulate or use real embeddings if API key works
        # Since I have the key, I'll use real embeddings
        embedding = self.embeddings.embed_query(text)
        self.collection.add(
            ids=[str(self.collection.count() + 1)],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata] if metadata else None
        )

    def search(self, query: str, limit: int = 3) -> List[str]:
        embedding = self.embeddings.embed_query(query)
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=limit
        )
        return results['documents'][0] if results['documents'] else []
