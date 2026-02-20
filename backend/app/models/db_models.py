from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.core.database import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    graph_id = Column(String, nullable=False)
    risk_score = Column(Float)
    cycle_detected = Column(Integer)
    smurf_detected = Column(Integer)
    shell_detected = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


# -----------------------------
# Frequent Fraudsters Table
# -----------------------------
class FraudAccount(Base):
    __tablename__ = "fraud_accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, unique=True, index=True)
    total_times_flagged = Column(Integer, default=1)
    highest_score_seen = Column(Float)
    last_pattern_type = Column(String)
    last_flagged_at = Column(DateTime, default=datetime.utcnow)
