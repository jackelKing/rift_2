def save_analysis(
    db: Session,
    risk_score: float,
    cycle: int,
    smurf: int,
    shell: int
):
    record = AnalysisResult(
        risk_score=risk_score,
        cycle_detected=cycle,
        smurf_detected=smurf,
        shell_detected=shell
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    # Auto-assign graph_id based on DB id
    record.graph_id = record.id
    db.commit()

    return record
