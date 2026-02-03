"""
FastAPI Backend para BooJ Dashboard
Conecta ao banco SQLite do hunter.py
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import sqlite3
from datetime import datetime
import os

app = FastAPI(
    title="BooJ API",
    description="API para dashboard de vagas BooJ",
    version="2.0.0"
)

# CORS para permitir requests do Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path para o banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "jobs.db")


def get_db():
    """Conexão com SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def read_root():
    return {
        "app": "BooJ API",
        "version": "2.0.0",
        "mascot": "👻 Boo"
    }


@app.get("/api/jobs")
def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    platform: Optional[str] = None,
    search: Optional[str] = None,
    remote_only: bool = False
):
    """
    Retorna lista de vagas com filtros
    
    Params:
    - skip: Pular N vagas (paginação)
    - limit: Limite de vagas por página
    - platform: Filtrar por plataforma (ex: "JobSpy (Linkedin)")
    - search: Buscar no título ou empresa
    - remote_only: Somente vagas remotas
    """
    
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
    
    # Filtros
    if platform:
        query += " AND plataforma LIKE ?"
        params.append(f"%{platform}%")
    
    if search:
        query += " AND (titulo LIKE ? OR empresa LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    
    if remote_only:
        query += " AND (localizacao LIKE '%remoto%' OR localizacao LIKE '%REMOTO%' OR localizacao LIKE '%🏠%')"
    
    # Ordenar por score e data
    query += " ORDER BY score DESC, data_publicacao DESC"
    
    # Paginação
    query += f" LIMIT {limit} OFFSET {skip}"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    # Contar total
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
    
    # Converter para dict
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
    
    return {
        "total": total,
        "jobs": jobs,
        "skip": skip,
        "limit": limit
    }


@app.get("/api/stats")
def get_stats():
    """Estatísticas gerais"""
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Total de vagas
    cursor.execute("SELECT COUNT(*) as total FROM jobs")
    total = cursor.fetchone()["total"]
    
    # Vagas hoje
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*) as today FROM jobs WHERE data_publicacao = ?", (today,))
    jobs_today = cursor.fetchone()["today"]
    
    # Top empresas
    cursor.execute("""
        SELECT empresa, COUNT(*) as count 
        FROM jobs 
        GROUP BY empresa 
        ORDER BY count DESC 
        LIMIT 5
    """)
    top_companies = [{"name": row["empresa"], "count": row["count"]} for row in cursor.fetchall()]
    
    # Top plataformas
    cursor.execute("""
        SELECT plataforma, COUNT(*) as count 
        FROM jobs 
        GROUP BY plataforma 
        ORDER BY count DESC 
        LIMIT 5
    """)
    top_platforms = [{"name": row["plataforma"], "count": row["count"]} for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        "total_jobs": total,
        "jobs_today": jobs_today,
        "top_companies": top_companies,
        "top_platforms": top_platforms
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
