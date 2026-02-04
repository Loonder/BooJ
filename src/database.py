# -*- coding: utf-8 -*-
"""
Database Module - SQLite abstraction for JobPulse.
Memory-efficient replacement for CSV/TXT storage.
"""

import sqlite3
import json
import os
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

try:
    from fuzzywuzzy import fuzz
except ImportError:
    fuzz = None

logger = logging.getLogger("JobDatabase")


class JobDatabase:
    """SQLite database for job storage with efficient querying."""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            from config import DB_PATH
            db_path = db_path or DB_PATH
        
        self.db_path = db_path
        self._ensure_dir()
        self._init_db()
    
    def _ensure_dir(self):
        """Ensure data directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _get_conn(self) -> sqlite3.Connection:
        """Get a database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_db(self):
        """Initialize database schema."""
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    link TEXT UNIQUE NOT NULL,
                    titulo TEXT,
                    empresa TEXT,
                    localizacao TEXT,
                    plataforma TEXT,
                    data_publicacao TEXT,
                    data_coleta TEXT,
                    score INTEGER DEFAULT 0,
                    is_relevant BOOLEAN DEFAULT 1,
                    tags TEXT DEFAULT '[]',
                    sent_discord BOOLEAN DEFAULT 0,
                    sent_telegram BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY, 
                    email TEXT UNIQUE, 
                    name TEXT,
                    image TEXT,
                    instagram TEXT,
                    xp INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_jobs_link ON jobs(link);
                CREATE INDEX IF NOT EXISTS idx_jobs_titulo_empresa ON jobs(titulo, empresa);
                CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at);
                CREATE INDEX IF NOT EXISTS idx_jobs_sent ON jobs(sent_discord, sent_telegram);
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
            """)
            conn.commit()
    
    # ==================== JOB OPERATIONS ====================
    
    def add_job(self, job: Dict) -> bool:
        """
        Add a job to the database.
        Returns True if inserted, False if duplicate.
        """
        try:
            with self._get_conn() as conn:
                conn.execute("""
                    INSERT INTO jobs (
                        link, titulo, empresa, localizacao, plataforma,
                        data_publicacao, data_coleta, score, is_relevant, tags
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job.get('link'),
                    job.get('titulo'),
                    job.get('empresa'),
                    job.get('localizacao'),
                    job.get('plataforma'),
                    job.get('data_publicacao'),
                    job.get('data_coleta'),
                    job.get('score', 0),
                    job.get('is_relevant', True),
                    json.dumps(job.get('tags', []))
                ))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # Duplicate link
            return False
        except Exception as e:
            logger.error(f"Error adding job: {e}")
            return False
    
    def add_jobs_batch(self, jobs: List[Dict]) -> int:
        """
        Add multiple jobs in a single transaction.
        Returns number of jobs successfully inserted.
        """
        inserted = 0
        with self._get_conn() as conn:
            for job in jobs:
                try:
                    conn.execute("""
                        INSERT INTO jobs (
                            link, titulo, empresa, localizacao, plataforma,
                            data_publicacao, data_coleta, score, is_relevant, tags
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        job.get('link'),
                        job.get('titulo'),
                        job.get('empresa'),
                        job.get('localizacao'),
                        job.get('plataforma'),
                        job.get('data_publicacao'),
                        job.get('data_coleta'),
                        job.get('score', 0),
                        job.get('is_relevant', True),
                        json.dumps(job.get('tags', []))
                    ))
                    inserted += 1
                except sqlite3.IntegrityError:
                    continue  # Skip duplicates
            conn.commit()
        return inserted
    
    def job_exists(self, link: str) -> bool:
        """Check if a job with this link exists. O(1) via index."""
        with self._get_conn() as conn:
            cursor = conn.execute(
                "SELECT 1 FROM jobs WHERE link = ? LIMIT 1", 
                (link,)
            )
            return cursor.fetchone() is not None
    
    def get_job(self, link: str) -> Optional[Dict]:
        """Get a single job by link."""
        with self._get_conn() as conn:
            cursor = conn.execute(
                "SELECT * FROM jobs WHERE link = ?", 
                (link,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_recent_jobs(self, days: int = 30) -> List[Dict]:
        """Get jobs from the last N days."""
        cutoff = datetime.now() - timedelta(days=days)
        with self._get_conn() as conn:
            cursor = conn.execute("""
                SELECT * FROM jobs 
                WHERE created_at >= ? 
                ORDER BY created_at DESC
            """, (cutoff.isoformat(),))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all jobs (use sparingly - for export only)."""
        with self._get_conn() as conn:
            cursor = conn.execute("SELECT * FROM jobs ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]
    
    def count_jobs(self) -> int:
        """Get total job count."""
        with self._get_conn() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM jobs")
            return cursor.fetchone()[0]
    
    # ==================== NOTIFICATION TRACKING ====================
    
    def mark_sent_discord(self, link: str) -> bool:
        """Mark job as sent to Discord."""
        with self._get_conn() as conn:
            conn.execute(
                "UPDATE jobs SET sent_discord = 1 WHERE link = ?", 
                (link,)
            )
            conn.commit()
            return conn.total_changes > 0
    
    def mark_sent_telegram(self, link: str) -> bool:
        """Mark job as sent to Telegram."""
        with self._get_conn() as conn:
            conn.execute(
                "UPDATE jobs SET sent_telegram = 1 WHERE link = ?", 
                (link,)
            )
            conn.commit()
            return conn.total_changes > 0
    
    def mark_sent(self, link: str) -> bool:
        """Mark job as sent to both Discord and Telegram."""
        with self._get_conn() as conn:
            conn.execute(
                "UPDATE jobs SET sent_discord = 1, sent_telegram = 1 WHERE link = ?", 
                (link,)
            )
            conn.commit()
            return conn.total_changes > 0
    
    def is_sent(self, link: str) -> bool:
        """Check if job was already sent (Discord)."""
        with self._get_conn() as conn:
            cursor = conn.execute(
                "SELECT sent_discord FROM jobs WHERE link = ?", 
                (link,)
            )
            row = cursor.fetchone()
            return bool(row and row[0])
    
    def get_unsent_jobs(self) -> List[Dict]:
        """Get jobs that haven't been sent yet."""
        with self._get_conn() as conn:
            cursor = conn.execute("""
                SELECT * FROM jobs 
                WHERE sent_discord = 0 
                ORDER BY score DESC, created_at DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== DUPLICATE DETECTION ====================
    
    def find_similar_jobs(self, titulo: str, empresa: str, limit: int = 10) -> List[Dict]:
        """
        Find potentially similar jobs for fuzzy matching.
        Uses SQL LIKE for initial filtering, then fuzzy in Python.
        """
        # Extract first significant word for SQL pre-filter
        titulo_words = titulo.lower().split()[:2]
        empresa_word = empresa.lower().split()[0] if empresa else ""
        
        with self._get_conn() as conn:
            # Broad SQL filter
            cursor = conn.execute("""
                SELECT link, titulo, empresa FROM jobs 
                WHERE (titulo LIKE ? OR titulo LIKE ? OR empresa LIKE ?)
                LIMIT ?
            """, (
                f"%{titulo_words[0]}%" if titulo_words else "%",
                f"%{titulo_words[1]}%" if len(titulo_words) > 1 else "%",
                f"%{empresa_word}%",
                limit * 5  # Get more for fuzzy filtering
            ))
            
            candidates = [dict(row) for row in cursor.fetchall()]
        
        return candidates[:limit]
    
    def is_fuzzy_duplicate(self, job: Dict, threshold: int = 90) -> bool:
        """
        Check if job is a fuzzy duplicate of existing jobs.
        More efficient than O(n) - uses SQL pre-filtering.
        """
        titulo = job.get('titulo', '')
        empresa = job.get('empresa', '')
        link = job.get('link', '')
        
        # 1. Exact link match (fastest)
        if self.job_exists(link):
            return True
        
        # 2. Fuzzy match on title+company
        if not fuzz:
            return False
            
        candidates = self.find_similar_jobs(titulo, empresa)
        current_sig = f"{titulo} {empresa}".lower()
        
        for candidate in candidates:
            candidate_sig = f"{candidate['titulo']} {candidate['empresa']}".lower()
            ratio = fuzz.token_set_ratio(current_sig, candidate_sig)
            if ratio > threshold:
                return True
        
        return False
    
    # ==================== MIGRATION HELPERS ====================
    
    def import_sent_jobs(self, sent_jobs_file: str) -> int:
        """
        Import sent_jobs.txt into the database.
        Marks existing jobs as sent.
        """
        if not os.path.exists(sent_jobs_file):
            return 0
        
        count = 0
        with open(sent_jobs_file, 'r') as f:
            links = [line.strip() for line in f if line.strip()]
        
        with self._get_conn() as conn:
            for link in links:
                # First check if job exists
                cursor = conn.execute(
                    "SELECT 1 FROM jobs WHERE link = ?", 
                    (link,)
                )
                if cursor.fetchone():
                    conn.execute(
                        "UPDATE jobs SET sent_discord = 1, sent_telegram = 1 WHERE link = ?",
                        (link,)
                    )
                    count += 1
            conn.commit()
        
        return count
    
    def export_to_csv(self, filepath: str) -> bool:
        """Export all jobs to CSV for backup."""
        import csv
        try:
            jobs = self.get_all_jobs()
            if not jobs:
                return False
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
                writer.writeheader()
                writer.writerows(jobs)
            return True
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return False
