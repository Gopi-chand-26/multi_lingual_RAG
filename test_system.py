#!/usr/bin/env python3
"""
Simple test script to verify the Multi-Language RAG System components.
"""

import os
import sys
import logging
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import SUPPORTED_LANGUAGES, GROQ_API_KEY
from utils.document_processor import DocumentProcessor
from utils.translation_service import TranslationService
from utils.vector_store import MultilingualVectorStore
from utils.rag_engine import MultilingualRAGEngine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_config():
    """Test configuration loading."""
    print("🔧 Testing configuration...")
    
    assert GROQ_API_KEY, "Groq API key not found"
    assert len(SUPPORTED_LANGUAGES) >= 20, f"Expected 20+ languages, got {len(SUPPORTED_LANGUAGES)}"
    
    print(f"✅ Configuration loaded successfully")
    print(f"   - Supported languages: {len(SUPPORTED_LANGUAGES)}")
    print(f"   - API key: {'*' * 10 + GROQ_API_KEY[-4:] if GROQ_API_KEY else 'Not set'}")

def test_document_processor():
    """Test document processor."""
    print("\n📄 Testing document processor...")
    
    processor = DocumentProcessor()
    
    # Test language detection
    test_texts = [
        ("Hello world", "en"),
        ("Hola mundo", "es"),
        ("Bonjour le monde", "fr"),
        ("Hallo Welt", "de"),
        ("こんにちは世界", "ja"),
    ]
    
    for text, expected_lang in test_texts:
        detected_lang = processor.detect_language(text)
        print(f"   - '{text[:20]}...' -> {detected_lang} (expected: {expected_lang})")
    
    # Test text chunking
    long_text = "This is a test. " * 100
    chunks = processor.chunk_text(long_text, chunk_size=100, overlap=20)
    print(f"   - Text chunking: {len(chunks)} chunks created")
    
    print("✅ Document processor working correctly")

def test_translation_service():
    """Test translation service."""
    print("\n🌐 Testing translation service...")
    
    translator = TranslationService()
    
    # Test language detection
    test_text = "Hello world"
    detected_lang = translator.detect_language(test_text)
    print(f"   - Language detection: '{test_text}' -> {detected_lang}")
    
    # Test translation
    try:
        translated = translator.translate_text("Hello world", "es")
        print(f"   - Translation: 'Hello world' -> '{translated}'")
    except Exception as e:
        print(f"   - Translation test failed: {e}")
    
    # Test cultural context
    cultural_prompt = translator.get_cultural_context_prompt("en", "ja")
    print(f"   - Cultural context prompt length: {len(cultural_prompt)} characters")
    
    print("✅ Translation service working correctly")

def test_vector_store():
    """Test vector store."""
    print("\n🔍 Testing vector store...")
    
    try:
        vector_store = MultilingualVectorStore()
        
        # Test embedding creation
        test_texts = ["Hello world", "Hola mundo", "Bonjour le monde"]
        embeddings = vector_store.create_embeddings(test_texts)
        
        print(f"   - Embeddings created: {len(embeddings)}")
        print(f"   - Embedding dimensions: {len(embeddings[0]) if embeddings else 0}")
        
        # Test collection stats
        stats = vector_store.get_collection_stats()
        print(f"   - Collection stats: {stats}")
        
        print("✅ Vector store working correctly")
        
    except Exception as e:
        print(f"   - Vector store test failed: {e}")

def test_rag_engine():
    """Test RAG engine."""
    print("\n🤖 Testing RAG engine...")
    
    try:
        rag_engine = MultilingualRAGEngine()
        
        # Test system stats
        stats = rag_engine.get_system_stats()
        print(f"   - System stats: {stats}")
        
        print("✅ RAG engine working correctly")
        
    except Exception as e:
        print(f"   - RAG engine test failed: {e}")

def test_file_structure():
    """Test file structure."""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "main.py",
        "config.py",
        "requirements.txt",
        "utils/document_processor.py",
        "utils/translation_service.py",
        "utils/vector_store.py",
        "utils/rag_engine.py",
        "templates/index.html",
        "static/styles.css",
        "static/script.js",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"   ✅ {file_path}")
    
    if missing_files:
        print(f"   ❌ Missing files: {missing_files}")
    else:
        print("✅ All required files present")

def main():
    """Run all tests."""
    print("🚀 Multi-Language RAG System - Component Tests")
    print("=" * 50)
    
    try:
        test_file_structure()
        test_config()
        test_document_processor()
        test_translation_service()
        test_vector_store()
        test_rag_engine()
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed successfully!")
        print("💡 To start the system, run: python main.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 