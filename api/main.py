"""
FastAPI Backend para BooJ Dashboard - Production Ready
Conecta ao banco SQLite do hunter.py
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import sqlite3
from datetime import datetime
import os
import logging

# ========================================
# ENVIRONMENT VARIABLES
# ========================================
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,https://booj.vercel.app,https://boo.paulomoraes.cloud"
).split(",")

DB_PATH = os.getenv(
    "DATABASE_PATH",
    os.path.join(os.path.dirname(__file__), "..", "data", "jobs.db")
)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", None)

# ========================================
# LOGGING CONFIGURATION
# ========================================
handlers = [logging.StreamHandler()]
if LOG_FILE:
    handlers.append(logging.FileHandler(LOG_FILE))

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=handlers
)
logger = logging.getLogger(__name__)

# ========================================
# FASTAPI APP
# ========================================
app = FastAPI(
    title="BooJ API",
    description="API for BooJ - Intelligent Job Aggregator",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ========================================
# CORS MIDDLEWARE (Production-Ready)
# ========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

logger.info(f"CORS configured for origins: {ALLOWED_ORIGINS}")
logger.info(f"Database path: {DB_PATH}")


# ========================================
# DATABASE CONNECTION
# ========================================
def get_db():
    """Conexão com SQLite com logging"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")


# ========================================
# HEALTH CHECK ENDPOINT
# ========================================
@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring and load balancers
    """
    try:
        # Test database connection
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM jobs")
        job_count = cursor.fetchone()[0]
        conn.close()
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        db_status = "unhealthy"
        job_count = 0
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.now().isoformat(),
        "database": db_status,
        "total_jobs": job_count,
        "version": "1.0.0"
    }


# ========================================
# ROOT ENDPOINT
# ========================================
@app.get("/")
def read_root():
    """Root endpoint with API info"""
    return {
        "app": "BooJ API",
        "version": "1.0.0",
        "mascot": "👻 Boo",
        "docs": "/docs",
        "health": "/health"
    }


# ========================================
# JOBS ENDPOINT
# ========================================
@app.get("/api/v1/jobs")
def get_jobs(
    skip: int = Query(0, ge=0, description="Number of jobs to skip"),
    limit: int = Query(50, ge=1, le=100, description="Max jobs to return"),
    platform: Optional[str] = Query(None, description="Filter by platform (e.g., 'LinkedIn')"),
    search: Optional[str] = Query(None, description="Search in title or company"),
    remote_only: bool = Query(False, description="Only remote jobs")
):
    """
    Get list of jobs with filters
    
    Returns:
        - total: Total number of jobs matching filters
        - jobs: List of job objects
        - skip: Current skip value
        - limit: Current limit value
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Base query
        query = """
            SELECT 
                id,
                titulo,
                empresa,
                localizacao,
                link,
                plataforma,
                data_publicacao,
                data_coleta,
                score
            FROM jobs
            WHERE 1=1
        """
        params = []
        
        # Filters
        if platform:
            query += " AND plataforma LIKE ?"
            params.append(f"%{platform}%")
        
        if search:
            query += " AND (titulo LIKE ? OR empresa LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        if remote_only:
            query += " AND (localizacao LIKE '%remoto%' OR localizacao LIKE '%REMOTO%' OR localizacao LIKE '%🏠%')"
        
        # Order by score and date
        query += " ORDER BY score DESC, data_publicacao DESC"
        
        # Pagination
        query += f" LIMIT {limit} OFFSET {skip}"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Count total
        count_query = "SELECT COUNT(*) as total FROM jobs WHERE 1=1"
        if platform:
            count_query += " AND plataforma LIKE ?"
        if search:
            count_query += " AND (titulo LIKE ? OR empresa LIKE ?)"
        if remote_only:
            count_query += " AND (localizacao LIKE '%remoto%' OR localizacao LIKE '%REMOTO%' OR localizacao LIKE '%🏠%')"
        
        cursor.execute(count_query, params)
        total = cursor.fetchone()["total"]
        
        conn.close()
        
        # Convert to dict
        jobs = []
        for row in rows:
            jobs.append({
                "id": row["id"],
                "titulo": row["titulo"],
                "empresa": row["empresa"],
                "localizacao": row["localizacao"],
                "link": row["link"],
                "plataforma": row["plataforma"],
                "data_publicacao": row["data_publicacao"],
                "data_coleta": row["data_coleta"],
                "score": row["score"] or 0
            })
        
        logger.info(f"Fetched {len(jobs)} jobs (total: {total})")
        
        return {
            "total": total,
            "jobs": jobs,
            "skip": skip,
            "limit": limit
        }
    
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        raise HTTPException(status_code=500, detail="Error fetching jobs")


# ========================================
# STATS ENDPOINT
# ========================================
@app.get("/api/v1/stats")
def get_stats():
    """
    Get general statistics
    
    Returns:
        - total_jobs: Total number of jobs
        - jobs_today: Jobs posted today
        - top_companies: Top 5 companies
        - top_platforms: Top 5 platforms
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Total jobs
        cursor.execute("SELECT COUNT(*) as total FROM jobs")
        total = cursor.fetchone()["total"]
        
        # Jobs today
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("SELECT COUNT(*) as today FROM jobs WHERE data_publicacao = ?", (today,))
        jobs_today = cursor.fetchone()["today"]
        
        # Top companies
        cursor.execute("""
            SELECT empresa, COUNT(*) as count 
            FROM jobs 
            GROUP BY empresa 
            ORDER BY count DESC 
            LIMIT 5
        """)
        top_companies = [{"name": row["empresa"], "count": row["count"]} for row in cursor.fetchall()]
        
        # Top platforms
        cursor.execute("""
            SELECT plataforma, COUNT(*) as count 
            FROM jobs 
            GROUP BY plataforma 
            ORDER BY count DESC 
            LIMIT 5
        """)
        top_platforms = [{"name": row["plataforma"], "count": row["count"]} for row in cursor.fetchall()]
        
        conn.close()
        
        logger.info(f"Stats fetched: {total} total jobs, {jobs_today} today")
        
        return {
            "total_jobs": total,
            "jobs_today": jobs_today,
            "top_companies": top_companies,
            "top_platforms": top_platforms
        }
    
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail="Error fetching stats")


# ========================================
# STARTUP EVENT
# ========================================
@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info("=" * 50)
    logger.info("BooJ API Starting...")
    logger.info(f"Version: 1.0.0")
    logger.info(f"Database: {DB_PATH}")
    logger.info(f"Allowed Origins: {ALLOWED_ORIGINS}")
    logger.info("=" * 50)


# ========================================
# MAIN (for local development)
# ========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
