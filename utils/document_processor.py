import os
import PyPDF2
from docx import Document
from langdetect import detect, LangDetectException
import re
from typing import List, Dict, Tuple
import logging

# Try to import pandas, but don't fail if it's not available
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    logging.warning("pandas not available - Excel and CSV processing will be limited")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.supported_extensions = {'.pdf', '.docx', '.txt', '.xlsx', '.csv'}
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {e}")
            return ""
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            logger.error(f"Error extracting text from TXT: {e}")
            return ""
    
    def extract_text_from_excel(self, file_path: str) -> str:
        """Extract text from Excel file."""
        if not PANDAS_AVAILABLE:
            logger.warning("pandas not available - cannot process Excel files")
            return f"Excel file detected but pandas is not available: {os.path.basename(file_path)}"
        
        try:
            df = pd.read_excel(file_path)
            text = ""
            for column in df.columns:
                text += f"{column}: " + " ".join(df[column].astype(str)) + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from Excel: {e}")
            return ""
    
    def extract_text_from_csv(self, file_path: str) -> str:
        """Extract text from CSV file."""
        if not PANDAS_AVAILABLE:
            logger.warning("pandas not available - cannot process CSV files")
            return f"CSV file detected but pandas is not available: {os.path.basename(file_path)}"
        
        try:
            df = pd.read_csv(file_path)
            text = ""
            for column in df.columns:
                text += f"{column}: " + " ".join(df[column].astype(str)) + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from CSV: {e}")
            return ""
    
    def detect_language(self, text: str) -> str:
        """Detect the language of the text."""
        try:
            # Clean text for better detection
            clean_text = re.sub(r'[^\w\s]', '', text[:1000])  # Use first 1000 chars
            if not clean_text.strip():
                return 'en'  # Default to English
            return detect(clean_text)
        except LangDetectException:
            return 'en'  # Default to English
        except Exception as e:
            logger.error(f"Error detecting language: {e}")
            return 'en'
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks."""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                for i in range(end, max(start, end - 100), -1):
                    if text[i] in '.!?':
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def process_document(self, file_path: str) -> Dict[str, any]:
        """Process a document and extract text with metadata."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        # Extract text based on file type
        if file_extension == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            text = self.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            text = self.extract_text_from_txt(file_path)
        elif file_extension == '.xlsx':
            text = self.extract_text_from_excel(file_path)
        elif file_extension == '.csv':
            text = self.extract_text_from_csv(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        if not text.strip():
            raise ValueError("No text content found in the document")
        
        # Detect language
        detected_language = self.detect_language(text)
        
        # Chunk text
        chunks = self.chunk_text(text)
        
        return {
            'original_text': text,
            'chunks': chunks,
            'language': detected_language,
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'file_size': os.path.getsize(file_path),
            'chunk_count': len(chunks)
        } 