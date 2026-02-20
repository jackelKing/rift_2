from sqlalchemy.orm import Session
from datetime import datetime
from app.models.db_models import FraudAccount


def update_fraud_account(db: Session, account_data: dict):

    account_id = account_data["account_id"]
    score = account_data["suspicion_score"]
    pattern = account_data["detected_patterns"][0]

    existing = db.query(FraudAccount).filter(
        FraudAccount.account_id == account_id
    ).first()

    if existing:
        existing.total_times_flagged += 1
        existing.highest_score_seen = max(existing.highest_score_seen, score)
        existing.last_pattern_type = pattern
        existing.last_flagged_at = datetime.utcnow()
    else:
        new_account = FraudAccount(
            account_id=account_id,
            total_times_flagged=1,
            highest_score_seen=score,
            last_pattern_type=pattern
        )
        db.add(new_account)

    db.commit()
