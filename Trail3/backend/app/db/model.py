from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class Upload(Base):
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    uploaded_at = Column(DateTime)
    status = Column(String)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(Integer, ForeignKey("uploads.id"))
    transaction_id = Column(String)
    sender_id = Column(String)
    receiver_id = Column(String)
    amount = Column(Float)
    timestamp = Column(DateTime)

class Account(Base):
    __tablename__ = "accounts"
    id = Column(String, primary_key=True, index=True)
    first_seen = Column(DateTime)
    last_seen = Column(DateTime)
    type = Column(String)

class FraudRing(Base):
    __tablename__ = "fraud_rings"
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(Integer, ForeignKey("uploads.id"))
    ring_id = Column(String)
    pattern_type = Column(String)
    risk_score = Column(Float)

class RingMember(Base):
    __tablename__ = "ring_members"
    id = Column(Integer, primary_key=True, index=True)
    ring_fk = Column(Integer, ForeignKey("fraud_rings.id"))
    account_id = Column(String)

class SuspiciousAccount(Base):
    __tablename__ = "suspicious_accounts"
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(Integer, ForeignKey("uploads.id"))
    account_id = Column(String)
    suspicion_score = Column(Float)
    detected_patterns = Column(Text)
    ring_id = Column(String)
