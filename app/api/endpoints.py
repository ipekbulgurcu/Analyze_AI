import os
import shutil
import tempfile
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List

from app.models.schemas import HealthCheck, IngestResponse, AskRequest, AskResponse
from app.services.llm_service import LLMService
from app.services.vector_store_service import VectorStoreService
from app.services.ingestion_service import IngestionService
from app.api.dependencies import get_llm_service, get_vector_store_service, get_ingestion_service
from app.core.exceptions import BaseAppException
from app.core.logging import logger

router = APIRouter()

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return HealthCheck(status="ok")

@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(...),
    ingestion_service: IngestionService = Depends(get_ingestion_service),
    vector_store_service: VectorStoreService = Depends(get_vector_store_service)
):
    """
    Uploads a file, splits it into chunks, and stores embeddings in the vector database.
    """
    logger.info(f"Received file upload: {file.filename}")
    
    # Create a temporary file to save the upload
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_path = tmp_file.name

    try:
        # Process the file
        documents = await ingestion_service.process_file(tmp_path)
        
        # Add to vector store
        vector_store_service.add_documents(documents)
        
        return IngestResponse(
            message="Document ingested successfully.",
            filename=file.filename,
            chunks_count=len(documents)
        )
        
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error during ingestion: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    llm_service: LLMService = Depends(get_llm_service),
    vector_store_service: VectorStoreService = Depends(get_vector_store_service)
):
    """
    Answers a question based on the ingested documents.
    """
    query = request.query
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    logger.info(f"Received query: {query}")
    
    try:
        # 1. Retrieve relevant documents
        # Note: ChromaDB persists automatically in new versions, but ensure data is there.
        relevant_docs = vector_store_service.similarity_search(query)
        
        if not relevant_docs:
            return AskResponse(
                query=query,
                answer="No relevant context found in documents.",
                source_documents=[]
            )
            
        # 2. Prepare context
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # 3. Generate answer
        answer = llm_service.generate_response(query, context)
        
        # Extract source names
        sources = list(set([doc.metadata.get("source", "unknown") for doc in relevant_docs]))
        
        return AskResponse(
            query=query,
            answer=answer,
            source_documents=sources
        )

    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error during QA: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
