from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import shutil
from typing import Optional
import logging
from config import UPLOAD_DIR, MAX_FILE_SIZE, ALLOWED_EXTENSIONS, SUPPORTED_LANGUAGES
from utils.rag_engine import MultilingualRAGEngine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Multi-Language RAG System",
    description="A RAG system that can retrieve information from documents in multiple languages",
    version="1.0.0"
)

# Create upload directory
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize RAG engine
rag_engine = MultilingualRAGEngine()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main application page."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "languages": SUPPORTED_LANGUAGES
    })

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document."""
    try:
        # Validate file size
        if file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        # Validate file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process and index document
        result = rag_engine.process_and_index_document(file_path)
        
        if result['success']:
            return {
                "success": True,
                "message": result['message'],
                "data": result['data']
            }
        else:
            raise HTTPException(status_code=500, detail=result['message'])
            
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_documents(
    query: str = Form(...),
    target_language: str = Form(default="en"),
    search_language: str = Form(default="all")
):
    """Query the RAG system."""
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if target_language not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail="Unsupported target language")
        
        result = rag_engine.search_and_generate_response(
            query, target_language, search_language
        )
        
        # Return the result regardless of success/failure
        # Let the frontend handle the response appropriately
        return result
            
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return {
            "success": False,
            "message": f"Error processing query: {str(e)}",
            "response": None,
            "sources": []
        }

@app.get("/stats")
async def get_system_stats():
    """Get system statistics."""
    try:
        stats = rag_engine.get_system_stats()
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
async def clear_system_data():
    """Clear all system data."""
    try:
        result = rag_engine.clear_system_data()
        return result
    except Exception as e:
        logger.error(f"Error clearing system data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Multi-Language RAG System is running"}

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get host and port from environment variables (for production)
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8001))
    
    uvicorn.run(app, host=host, port=port) 