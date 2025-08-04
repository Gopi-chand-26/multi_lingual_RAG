# 🌍 Multi-Language RAG System

A powerful Retrieval-Augmented Generation (RAG) system that can process documents in multiple languages and provide answers in the user's preferred language, with cultural context preservation.

## ✨ Features

- **🌐 Multi-Language Support**: Process documents in 20+ languages
- **🔍 Cross-Language Search**: Search across all indexed documents regardless of language
- **🎯 Cultural Context Preservation**: Maintain cultural sensitivity in translations
- **📄 Multiple File Formats**: Support for PDF, DOCX, TXT, Excel, CSV
- **⚡ Fast Processing**: Powered by Groq LLM and ChromaDB
- **🎨 Beautiful UI**: Modern, responsive interface with glass-morphism effects
- **📊 Real-time Statistics**: Monitor system performance and document statistics

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API Key (already configured)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd nervsparks
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python main.py
```

4. **Access the system:**
   - Open your browser and go to `http://localhost:8000`
   - Start uploading documents and asking questions!

## 📁 Project Structure

```
nervsparks/
├── main.py                 # FastAPI application
├── config.py              # Configuration and API keys
├── requirements.txt        # Dependencies
├── utils/
│   ├── document_processor.py  # Document parsing
│   ├── vector_store.py        # ChromaDB integration
│   ├── translation_service.py # Translation with cultural context
│   └── rag_engine.py         # Main RAG orchestrator
├── templates/
│   └── index.html            # Beautiful UI template
└── static/
    ├── styles.css            # Modern CSS styling
    └── script.js             # Frontend JavaScript
```

## 🎯 Usage Guide

### 1. Upload Documents

- **Drag & Drop**: Simply drag files onto the upload area
- **Click to Browse**: Click the upload area to select files
- **Supported Formats**: PDF, DOCX, TXT, Excel (.xlsx), CSV
- **Multi-Language**: Upload documents in any supported language

### 2. Ask Questions

- **Any Language**: Ask questions in any supported language
- **Target Language**: Choose your preferred answer language
- **Search Scope**: Search across all languages or specific languages
- **Cultural Context**: Answers maintain cultural sensitivity

### 3. System Features

- **Statistics**: View system stats and document information
- **Clear Data**: Reset the system when needed
- **Real-time Processing**: See upload progress and results

## 🌍 Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| English | en | Spanish | es |
| French | fr | German | de |
| Italian | it | Portuguese | pt |
| Russian | ru | Japanese | ja |
| Korean | ko | Chinese | zh |
| Arabic | ar | Hindi | hi |
| Dutch | nl | Swedish | sv |
| Norwegian | no | Danish | da |
| Finnish | fi | Polish | pl |
| Turkish | tr | Hebrew | he |

## 🔧 Technical Architecture

### Core Components

1. **Document Processor**
   - Multi-format text extraction
   - Automatic language detection
   - Intelligent text chunking
   - Metadata preservation

2. **Vector Store (ChromaDB)**
   - Cross-lingual embeddings
   - Similarity search
   - Metadata indexing
   - Persistent storage

3. **Translation Service**
   - Google Translate integration
   - Cultural context preservation
   - Caching for performance
   - Language-specific prompts

4. **RAG Engine**
   - Groq LLM integration
   - Context-aware responses
   - Source attribution
   - Multi-language orchestration

### API Endpoints

- `GET /` - Main application interface
- `POST /upload` - Upload and process documents
- `POST /query` - Query the RAG system
- `GET /stats` - Get system statistics
- `POST /clear` - Clear all system data
- `GET /health` - Health check

## 🎨 UI Features

- **Modern Design**: Glass-morphism effects and gradients
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Drag & Drop**: Intuitive file upload
- **Real-time Feedback**: Progress indicators and notifications
- **Interactive Modals**: Statistics and system information
- **Smooth Animations**: Professional user experience

## 🚀 Deployment

### Local Development

```bash
python main.py
```

### Production Deployment

1. **Using Gunicorn:**
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

2. **Using Docker:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

3. **Environment Variables:**
```bash
export GROQ_API_KEY="your_groq_api_key"
export UPLOAD_DIR="./uploads"
export CHROMA_PERSIST_DIRECTORY="./chroma_db"
```

## 📊 Performance Features

- **Caching**: Translation cache for improved performance
- **Chunking**: Intelligent text chunking for better retrieval
- **Embeddings**: Efficient cross-lingual embeddings
- **Async Processing**: Non-blocking file uploads
- **Memory Management**: Optimized for large document collections

## 🔒 Security Features

- **File Validation**: Type and size checking
- **Input Sanitization**: Safe text processing
- **Error Handling**: Graceful error management
- **API Key Protection**: Secure configuration management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review the error logs
3. Open an issue on GitHub

## 🎉 Acknowledgments

- **Groq**: For fast LLM inference
- **ChromaDB**: For vector storage
- **Google Translate**: For translation services
- **Sentence Transformers**: For embeddings
- **FastAPI**: For the web framework

---

**Built with ❤️ for multilingual knowledge management** 