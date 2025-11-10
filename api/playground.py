"""
Playground API Router

FastAPI router for playground-specific session management endpoints.
This module provides session lifecycle management for the interactive playground.

Endpoints:
- POST /api/playground/session - Create a new playground session
- GET /api/playground/session/{session_id} - Get session information
- DELETE /api/playground/session/{session_id} - Delete a session
- GET /api/playground/sessions - List all sessions
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import uuid
import logging

logger = logging.getLogger("api.playground")

# Router instance
router = APIRouter(prefix="/api/playground", tags=["playground"])

# In-memory session storage (use Redis/DB in production)
playground_sessions: Dict[str, Dict[str, Any]] = {}


class SessionCreate(BaseModel):
    """Request model for creating a new session"""
    name: Optional[str] = "Playground Session"
    metadata: Optional[Dict[str, Any]] = {}


class SessionInfo(BaseModel):
    """Response model for session information"""
    session_id: str
    name: str
    created_at: str
    updated_at: str
    message_count: int
    metadata: Dict[str, Any]


class SessionList(BaseModel):
    """Response model for session listing"""
    sessions: List[SessionInfo]
    total: int
    limit: int
    offset: int


@router.post("/session", response_model=SessionInfo, status_code=201)
async def create_session(request: SessionCreate):
    """
    Create a new playground session.
    
    Args:
        request: SessionCreate - Session creation parameters
        
    Returns:
        SessionInfo - Created session information
        
    Example:
        POST /api/playground/session
        {
            "name": "My Playground Session",
            "metadata": {"user": "demo"}
        }
    """
    session_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    
    session = {
        "session_id": session_id,
        "name": request.name,
        "created_at": now,
        "updated_at": now,
        "message_count": 0,
        "metadata": request.metadata or {}
    }
    
    playground_sessions[session_id] = session
    logger.info(f"Created playground session: {session_id}")
    
    return SessionInfo(**session)


@router.get("/session/{session_id}", response_model=SessionInfo)
async def get_session(session_id: str):
    """
    Get information about a specific session.
    
    Args:
        session_id: str - The session ID to retrieve
        
    Returns:
        SessionInfo - Session information
        
    Raises:
        HTTPException: 404 if session not found
        
    Example:
        GET /api/playground/session/123e4567-e89b-12d3-a456-426614174000
    """
    if session_id not in playground_sessions:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    session = playground_sessions[session_id]
    return SessionInfo(**session)


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a playground session.
    
    Args:
        session_id: str - The session ID to delete
        
    Returns:
        dict - Deletion confirmation message
        
    Raises:
        HTTPException: 404 if session not found
        
    Example:
        DELETE /api/playground/session/123e4567-e89b-12d3-a456-426614174000
    """
    if session_id not in playground_sessions:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    del playground_sessions[session_id]
    logger.info(f"Deleted playground session: {session_id}")
    
    return {"message": f"Session {session_id} deleted successfully"}


@router.get("/sessions", response_model=SessionList)
async def list_sessions(
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of sessions to return"),
    offset: int = Query(default=0, ge=0, description="Number of sessions to skip")
):
    """
    List all playground sessions with pagination.
    
    Args:
        limit: int - Maximum number of sessions to return (1-100, default 50)
        offset: int - Number of sessions to skip (default 0)
        
    Returns:
        SessionList - List of sessions with pagination info
        
    Example:
        GET /api/playground/sessions?limit=10&offset=0
    """
    all_sessions = list(playground_sessions.values())
    total = len(all_sessions)
    
    # Apply pagination
    paginated_sessions = all_sessions[offset:offset + limit]
    
    session_infos = [SessionInfo(**session) for session in paginated_sessions]
    
    return SessionList(
        sessions=session_infos,
        total=total,
        limit=limit,
        offset=offset
    )


@router.put("/session/{session_id}/message-count")
async def update_message_count(session_id: str, count: int = Query(..., ge=0)):
    """
    Update the message count for a session (internal use).
    
    Args:
        session_id: str - The session ID
        count: int - New message count
        
    Returns:
        dict - Updated session info
        
    Raises:
        HTTPException: 404 if session not found
    """
    if session_id not in playground_sessions:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    playground_sessions[session_id]["message_count"] = count
    playground_sessions[session_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    logger.info(f"Updated message count for session {session_id}: {count}")
    
    return SessionInfo(**playground_sessions[session_id])


# Health check endpoint for playground
@router.get("/health")
async def playground_health():
    """
    Health check endpoint for playground API.
    
    Returns:
        dict - Health status and session count
    """
    return {
        "status": "healthy",
        "active_sessions": len(playground_sessions),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
