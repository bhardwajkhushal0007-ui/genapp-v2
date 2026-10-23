from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import hashlib
from datetime import datetime
import os

app = FastAPI(title="GenApp Version 2 Enterprise DVI Backend")

DB_FILE = "genapp.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT,
                    role TEXT,
                    full_name TEXT
                )''')
    # Cases table
    c.execute('''CREATE TABLE IF NOT EXISTS cases (
                    case_id TEXT PRIMARY KEY,
                    incident TEXT,
                    location TEXT,
                    date TEXT,
                    status TEXT,
                    created_by TEXT
                )''')
    # Audit trail table (eCoC)
    c.execute('''CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    action TEXT,
                    user TEXT,
                    details TEXT,
                    sha256 TEXT
                )''')
    
    # Insert default expert user if not exists
    default_pass = hashlib.sha256("GenApp2026!".encode()).hexdigest()
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", 
              ("expert@genapp.gov.in", default_pass, "Senior Forensic Biologist", "Dr. A. Sharma"))
    
    # Insert default initial case if none exist
    c.execute("SELECT COUNT(*) FROM cases")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?)",
                  ("CASE-2026-DVI-091", "Commercial Aircraft Incident - Flight AI-502", "New Delhi Sector 4", "2026-10-23", "Active Investigation", "expert@genapp.gov.in"))
    
    conn.commit()
    conn.close()

init_db()

# Models
class LoginRequest(BaseModel):
    username: str
    password: str

class CaseCreate(BaseModel):
    case_id: str
    incident: str
    location: str
    date: str
    created_by: str

class AuditLogCreate(BaseModel):
    action: str
    user: str
    details: str

# API Routes
@app.post("/api/login")
def login(creds: LoginRequest):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    pass_hash = hashlib.sha256(creds.password.encode()).hexdigest()
    c.execute("SELECT username, role, full_name FROM users WHERE username = ? AND password_hash = ?", (creds.username, pass_hash))
    user = c.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials. Use expert@genapp.gov.in / GenApp2026!")
    return {"status": "success", "username": user[0], "role": user[1], "full_name": user[2]}

@app.get("/api/cases")
def get_cases():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT case_id, incident, location, date, status, created_by FROM cases")
    rows = c.fetchall()
    conn.close()
    return [{"case_id": r[0], "incident": r[1], "location": r[2], "date": r[3], "status": r[4], "created_by": r[5]} for r in rows]

@app.post("/api/cases")
def create_case(case: CaseCreate):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?)", 
                  (case.case_id, case.incident, case.location, case.date, "Active Investigation", case.created_by))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Case ID already exists.")
    conn.close()
    return {"status": "success", "case_id": case.case_id}

@app.get("/api/audit")
def get_audit_logs():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT timestamp, action, user, details, sha256 FROM audit_logs ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [{"timestamp": r[0], "action": r[1], "user": r[2], "details": r[3], "sha256": r[4]} for r in rows]

@app.post("/api/audit")
def add_audit_log(log: AuditLogCreate):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    raw_data = f"{timestamp}|{log.action}|{log.user}|{log.details}"
    sha256_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO audit_logs (timestamp, action, user, details, sha256) VALUES (?, ?, ?, ?, ?)",
              (timestamp, log.action, log.user, log.details, sha256_hash))
    conn.commit()
    conn.close()
    return {"status": "success", "sha256": sha256_hash}

# Serve Frontend static files
if not os.path.exists("static"):
    os.makedirs("static")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")
