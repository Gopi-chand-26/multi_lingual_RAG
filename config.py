import os
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

# API Keys - Use environment variables for security
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Supported Languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'no': 'Norwegian',
    'da': 'Danish',
    'fi': 'Finnish',
    'pl': 'Polish',
    'tr': 'Turkish',
    'he': 'Hebrew'
}

# Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama3-70b-8192"

# Database Configuration
CHROMA_PERSIST_DIRECTORY = "./chroma_db"
COLLECTION_NAME = "multilingual_documents"

# File Upload Configuration
UPLOAD_DIR = "./uploads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.xlsx', '.csv'}

# Translation Configuration
TRANSLATION_CACHE_SIZE = 1000
TRANSLATION_TIMEOUT = 30

# UI Configuration
DEFAULT_LANGUAGE = "en"
DEFAULT_THEME = "light" 