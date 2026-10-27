from datetime import datetime, date, timezone
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Text, Date, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

APP_ENV = os.getenv("APP_ENV", "development")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./creditstrike_demo.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

class Case(Base):
    __tablename__ = "cases"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    creditor: Mapped[str] = mapped_column(String(200), index=True)
    bureau: Mapped[str] = mapped_column(String(30), default="unknown")
    account_reference: Mapped[str] = mapped_column(String(80), default="")  # Never store full account numbers.
    issue_type: Mapped[str] = mapped_column(String(80), default="needs_review")
    allegation: Mapped[str] = mapped_column(Text, default="")
    evidence_notes: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(40), default="new")
    next_action: Mapped[str] = mapped_column(Text, default="Review report and identify a specific factual issue.")
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

Base.metadata.create_all(bind=engine)
app = FastAPI(title="CreditStrike AI API", version="0.1.0",
              description="Prototype case tracker. Not production-secure; do not upload real reports yet.")

class CaseCreate(BaseModel):
    creditor: str = Field(min_length=1, max_length=200)
    bureau: str = Field(default="unknown", max_length=30)
    account_reference: str = Field(default="", max_length=80, description="Use a masked reference only.")
    issue_type: str = Field(default="needs_review", max_length=80)
    allegation: str = Field(default="", max_length=5000)
    evidence_notes: str = Field(default="", max_length=10000)
    status: str = Field(default="new", max_length=40)
    next_action: str = Field(default="Review report and identify a specific factual issue.", max_length=3000)
    deadline: Optional[date] = None

class CaseOut(CaseCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

@app.get("/")
def root():
    return {"name": "CreditStrike AI API", "status": "prototype",
            "warning": "Demo only. Authentication and production data safeguards are not yet implemented."}

@app.get("/health")
def health():
    return {"status": "ok", "environment": APP_ENV}

@app.get("/api/cases", response_model=list[CaseOut])
def list_cases():
    # Prototype only: this endpoint is intentionally not suitable for real personal data
    # until authentication and per-user authorization are implemented.
    with SessionLocal() as db:
        return db.query(Case).order_by(Case.created_at.desc()).all()

@app.post("/api/cases", response_model=CaseOut, status_code=201)
def create_case(payload: CaseCreate):
    with SessionLocal() as db:
        row = Case(**payload.model_dump())
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

@app.get("/api/cases/{case_id}", response_model=CaseOut)
def get_case(case_id: int):
    with SessionLocal() as db:
        row = db.get(Case, case_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Case not found")
        return row

@app.patch("/api/cases/{case_id}", response_model=CaseOut)
def update_case(case_id: int, payload: CaseCreate):
    with SessionLocal() as db:
        row = db.get(Case, case_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Case not found")
        for key, value in payload.model_dump().items():
            setattr(row, key, value)
        db.commit()
        db.refresh(row)
        return row

@app.delete("/api/cases/{case_id}", status_code=204)
def delete_case(case_id: int):
    with SessionLocal() as db:
        row = db.get(Case, case_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Case not found")
        db.delete(row)
        db.commit()
