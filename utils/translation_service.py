import asyncio
from typing import Dict, Optional, List
import logging
import time
from functools import lru_cache
from langdetect import detect, LangDetectException

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
    
    def detect_language(self, text: str) -> str:
        """Detect the language of the text."""
        try:
            if not text.strip():
                return 'en'
            return detect(text)
        except LangDetectException:
            return 'en'
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return 'en'
    
    def translate_text(self, text: str, target_lang: str, source_lang: str = 'auto') -> str:
        """Simple translation placeholder - in production, use a proper translation service."""
        # For now, return the original text with a note about translation
        if source_lang != 'auto' and source_lang != target_lang:
            return f"[Translated from {source_lang} to {target_lang}] {text}"
        return text
    
    def translate_chunks(self, chunks: List[str], target_lang: str, source_lang: str = 'auto') -> List[str]:
        """Translate a list of text chunks."""
        translated_chunks = []
        for chunk in chunks:
            translated_chunk = self.translate_text(chunk, target_lang, source_lang)
            translated_chunks.append(translated_chunk)
        return translated_chunks
    
    def get_cultural_context_prompt(self, source_lang: str, target_lang: str) -> str:
        """Generate cultural context preservation prompt."""
        cultural_contexts = {
            ('en', 'ja'): "Please provide the answer in Japanese, maintaining cultural sensitivity and using appropriate honorifics when relevant.",
            ('en', 'ko'): "Please provide the answer in Korean, maintaining cultural sensitivity and using appropriate honorifics when relevant.",
            ('en', 'zh'): "Please provide the answer in Chinese, maintaining cultural sensitivity and using appropriate formal language when relevant.",
            ('en', 'ar'): "Please provide the answer in Arabic, maintaining cultural sensitivity and using appropriate formal language when relevant.",
            ('en', 'hi'): "Please provide the answer in Hindi, maintaining cultural sensitivity and using appropriate formal language when relevant.",
            ('en', 'ru'): "Please provide the answer in Russian, maintaining cultural sensitivity and using appropriate formal language when relevant.",
            ('en', 'de'): "Please provide the answer in German, maintaining cultural sensitivity and using appropriate formal language when relevant.",
            ('en', 'fr'): "Please provide the answer in French, maintaining cultural sensitivity and using appropriate formal language when relevant.",
            ('en', 'es'): "Please provide the answer in Spanish, maintaining cultural sensitivity and using appropriate formal language when relevant.",
            ('en', 'it'): "Please provide the answer in Italian, maintaining cultural sensitivity and using appropriate formal language when relevant.",
            ('en', 'pt'): "Please provide the answer in Portuguese, maintaining cultural sensitivity and using appropriate formal language when relevant.",
        }
        
        return cultural_contexts.get((source_lang, target_lang), 
                                  f"Please provide the answer in {target_lang}, maintaining cultural sensitivity.")
    
    def create_multilingual_prompt(self, query: str, target_lang: str, source_lang: str = 'en') -> str:
        """Create a multilingual prompt that preserves cultural context."""
        cultural_prompt = self.get_cultural_context_prompt(source_lang, target_lang)
        
        base_prompt = f"""
You are a multilingual AI assistant. The user has asked a question in {source_lang}, and you should respond in {target_lang}.

{cultural_prompt}

Question: {query}

Please provide a comprehensive and culturally appropriate answer in {target_lang}.
"""
        return base_prompt
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get translation cache statistics."""
        return {
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_size': len(self.cache)
        }
    
    def clear_cache(self):
        """Clear the translation cache."""
        self.cache.clear()
        self.cache_hits = 0
        self.cache_misses = 0 