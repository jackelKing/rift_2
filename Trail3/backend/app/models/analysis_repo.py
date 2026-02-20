from sqlalchemy.orm import Session
from app.models.db_models import AnalysisResult

def save_analysis(
    db: Session,
    graph_id: str,
    risk_score: float,
    cycle: int,
    smurf: int,
    shell: int
):
    record = AnalysisResult(
        graph_id=graph_id,
        risk_score=risk_score,
        cycle_detected=cycle,
        smurf_detected=smurf,
        shell_detected=shell
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record
