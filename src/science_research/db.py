from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

import sqlite3


def _resolve_db_path() -> Path:
    database_url = os.getenv("DATABASE_URL", "sqlite:///./research.db")
    if database_url.startswith("sqlite:///"):
        raw_path = database_url.replace("sqlite:///", "", 1)
        if raw_path.startswith("./"):
            return Path.cwd() / raw_path[2:]
        if raw_path.startswith("/"):
            return Path(raw_path)
        return Path.cwd() / raw_path
    return Path(database_url)


DB_PATH = _resolve_db_path()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def connect_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = connect_db()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                domain TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'draft',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                authors TEXT,
                year INTEGER,
                journal TEXT,
                doi TEXT,
                url TEXT,
                abstract TEXT,
                keywords TEXT,
                source TEXT,
                peer_reviewed INTEGER DEFAULT 1,
                full_text_available INTEGER DEFAULT 0,
                access_type TEXT,
                citation_count INTEGER,
                metadata_json TEXT,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS research_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                rationale TEXT,
                novelty_score REAL,
                priority INTEGER DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS methodologies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                question_id INTEGER,
                design_type TEXT,
                data_sources TEXT,
                analysis_methods TEXT,
                validation_strategy TEXT,
                assumptions TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                topic TEXT,
                domain TEXT,
                summary_json TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            )
            """
        )

        conn.commit()
    finally:
        conn.close()


def create_project(title: str, domain: str, description: str = "") -> Dict[str, Any]:
    init_db()
    conn = connect_db()
    try:
        cursor = conn.execute(
            "INSERT INTO projects (title, domain, description, status) VALUES (?, ?, ?, 'draft')",
            (title, domain, description),
        )
        project_id = cursor.lastrowid
        conn.commit()
        return {
            "id": project_id,
            "title": title,
            "domain": domain,
            "description": description,
            "status": "draft",
        }
    finally:
        conn.close()


def list_projects() -> List[Dict[str, Any]]:
    init_db()
    conn = connect_db()
    try:
        rows = conn.execute(
            "SELECT id, title, domain, description, status, created_at, updated_at FROM projects ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def save_paper(project_id: int, paper: Dict[str, Any]) -> None:
    conn = connect_db()
    try:
        conn.execute(
            """
            INSERT INTO papers (
                project_id, title, authors, year, journal, doi, url, abstract,
                keywords, source, peer_reviewed, full_text_available, access_type,
                citation_count, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                project_id,
                paper.get("title"),
                json.dumps(paper.get("authors", [])),
                paper.get("year"),
                paper.get("journal"),
                paper.get("doi"),
                paper.get("url"),
                paper.get("abstract"),
                json.dumps(paper.get("keywords", [])),
                paper.get("source"),
                int(bool(paper.get("peer_reviewed", True))),
                int(bool(paper.get("full_text_available", False))),
                paper.get("access_type"),
                paper.get("citation_count"),
                json.dumps(paper),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def save_question(project_id: int, question: Dict[str, Any]) -> None:
    conn = connect_db()
    try:
        conn.execute(
            "INSERT INTO research_questions (project_id, text, rationale, novelty_score, priority) VALUES (?, ?, ?, ?, ?)",
            (
                project_id,
                question.get("text"),
                question.get("rationale", ""),
                question.get("novelty_score", 0.0),
                question.get("priority", 1),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def save_methodology(project_id: int, methodology: Dict[str, Any]) -> None:
    conn = connect_db()
    try:
        conn.execute(
            "INSERT INTO methodologies (project_id, design_type, data_sources, analysis_methods, validation_strategy, assumptions) VALUES (?, ?, ?, ?, ?, ?)",
            (
                project_id,
                methodology.get("design_type", "observational"),
                json.dumps(methodology.get("data_sources", [])),
                json.dumps(methodology.get("methods", [])),
                json.dumps(methodology.get("validation_strategy", [])),
                json.dumps(methodology.get("assumptions", [])),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def save_analysis_run(project_id: int, topic: str, domain: str, summary: Dict[str, Any]) -> None:
    conn = connect_db()
    try:
        conn.execute(
            "INSERT INTO analysis_runs (project_id, topic, domain, summary_json) VALUES (?, ?, ?, ?)",
            (project_id, topic, domain, json.dumps(summary)),
        )
        conn.commit()
    finally:
        conn.close()


__all__ = [
    "connect_db",
    "init_db",
    "create_project",
    "list_projects",
    "save_paper",
    "save_question",
    "save_methodology",
    "save_analysis_run",
]
