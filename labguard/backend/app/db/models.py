from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="staff")
    created_at = Column(DateTime, default=datetime.utcnow)


class Lab(Base):
    __tablename__ = "labs"

    id = Column(Integer, primary_key=True)
    lab_id = Column(String, unique=True, index=True)
    rtsp_url = Column(String)


class EntryLog(Base):
    __tablename__ = "entry_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    lab_id = Column(String)
    compliant = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)


class SDKCommand(Base):
    __tablename__ = "sdk_commands"

    id = Column(Integer, primary_key=True)
    sdk_id = Column(String, index=True)
    lab_id = Column(String, index=True)

    command = Column(String, nullable=False)
    status = Column(String, default="PENDING")  # PENDING | IN_PROGRESS | DONE | FAILED

    payload = Column(String)  # JSON
    result = Column(String)   # JSON

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
