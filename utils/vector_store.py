import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging
import os
from config import CHROMA_PERSIST_DIRECTORY, COLLECTION_NAME, EMBEDDING_MODEL

logger = logging.getLogger(__name__)

class MultilingualVectorStore:
    def __init__(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIRECTORY,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        try:
            collection = self.client.get_collection(COLLECTION_NAME)
            logger.info(f"Using existing collection: {COLLECTION_NAME}")
        except:
            collection = self.client.create_collection(
                name=COLLECTION_NAME,
                metadata={"description": "Multilingual document embeddings"}
            )
            logger.info(f"Created new collection: {COLLECTION_NAME}")
        return collection
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        try:
            embeddings = self.embedding_model.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error creating embeddings: {e}")
            return []
    
    def add_documents(self, documents: List[Dict]) -> bool:
        try:
            all_texts = []
            all_metadatas = []
            all_ids = []
            
            for doc in documents:
                chunks = doc.get('chunks', [])
                language = doc.get('language', 'en')
                file_name = doc.get('file_name', 'unknown')
                file_path = doc.get('file_path', '')
                
                for i, chunk in enumerate(chunks):
                    all_texts.append(chunk)
                    all_metadatas.append({
                        'language': language,
                        'file_name': file_name,
                        'file_path': file_path,
                        'chunk_index': i,
                        'total_chunks': len(chunks)
                    })
                    all_ids.append(f"{file_name}_{language}_{i}")
            
            if not all_texts:
                return False
            
            embeddings = self.create_embeddings(all_texts)
            
            if embeddings:
                self.collection.add(
                    embeddings=embeddings,
                    documents=all_texts,
                    metadatas=all_metadatas,
                    ids=all_ids
                )
                return True
            return False
                
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False
    
    def search_documents(self, query: str, language: str = 'en', top_k: int = 5) -> List[Dict]:
        try:
            query_embedding = self.create_embeddings([query])
            
            if not query_embedding:
                return []
            
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=top_k,
                where={"language": language} if language != 'all' else None
            )
            
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    distance = results['distances'][0][i] if 'distances' in results else 1.0
                    
                    # More lenient threshold for single language search
                    if distance < 2.0:
                        formatted_results.append({
                            'content': results['documents'][0][i],
                            'metadata': results['metadatas'][0][i],
                            'distance': distance,
                            'id': results['ids'][0][i] if 'ids' in results else None
                        })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []
    
    def search_multilingual(self, query: str, target_language: str = 'en', top_k: int = 5) -> List[Dict]:
        try:
            query_embedding = self.create_embeddings([query])
            
            if not query_embedding:
                return []
            
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=top_k * 2,
                where=None
            )
            
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    distance = results['distances'][0][i] if 'distances' in results else 1.0
                    
                    # Lower threshold to allow more results
                    if distance < 2.0:
                        formatted_results.append({
                            'content': results['documents'][0][i],
                            'metadata': results['metadatas'][0][i],
                            'distance': distance,
                            'id': results['ids'][0][i] if 'ids' in results else None
                        })
            
            return formatted_results[:top_k]
            
        except Exception as e:
            logger.error(f"Error in multilingual search: {e}")
            return []
    
    def get_collection_stats(self) -> Dict:
        try:
            count = self.collection.count()
            all_metadatas = self.collection.get()['metadatas']
            languages = set()
            file_names = set()
            
            for metadata in all_metadatas:
                if metadata and 'language' in metadata:
                    languages.add(metadata['language'])
                if metadata and 'file_name' in metadata:
                    file_names.add(metadata['file_name'])
            
            return {
                'total_documents': count,
                'unique_languages': list(languages),
                'unique_files': list(file_names),
                'language_count': len(languages),
                'file_count': len(file_names)
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}
    
    def clear_collection(self) -> bool:
        """Clear all documents from the collection."""
        try:
            # Delete the collection and recreate it
            self.client.delete_collection(COLLECTION_NAME)
            self.collection = self.client.create_collection(
                name=COLLECTION_NAME,
                metadata={"description": "Multilingual document embeddings"}
            )
            logger.info("Collection cleared successfully")
            return True
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")
            return False 