import time
import pandas as pd

from app.core.graph_builder import build_graph
from app.core.cycle_detector import detect_cycles
from app.core.smurf_detector import detect_smurfing
from app.core.shell_detector import detect_shell_layers
from app.core.feature_engineering import build_node_features
from app.core.scoring_model import compute_anomaly_scores


# -----------------------------
# Merchant / Payroll Shield
# -----------------------------
def is_legitimate_hub(node, graph, cycle_nodes):

    in_deg = graph.in_degree(node)
    out_deg = graph.out_degree(node)

    # Payroll / structured merchant pattern
    if (
        out_deg >= 100 and
        in_deg <= 5 and
        node not in cycle_nodes
    ):
        return True
    
    # High-volume receiver (merchant pattern)
    if (
        in_deg >= 100 and
        out_deg <= 5 and
        node not in cycle_nodes
    ):
        return True
    
        return False
    

# -----------------------------
# Velocity Bonus
# -----------------------------
def compute_velocity_bonus(account_id, df):

    user_tx = df[
        (df["sender_id"] == account_id) |
        (df["receiver_id"] == account_id)
    ]

    if len(user_tx) < 5:
        return 0

    time_span = (
        user_tx["timestamp"].max() -
        user_tx["timestamp"].min()
    ).total_seconds() / 3600

    if time_span < 24:
        return 3
    elif time_span < 72:
        return 1
    else:
        return 0


# -----------------------------
# Main Engine
# -----------------------------
import time
import pandas as pd

from app.core.graph_builder import build_graph
from app.core.cycle_detector import detect_cycles
from app.core.smurf_detector import detect_smurfing
from app.core.shell_detector import detect_shell_layers
from app.core.feature_engineering import build_node_features
from app.core.scoring_model import compute_anomaly_scores


# -----------------------------
# Merchant / Payroll Shield
# -----------------------------
def is_legitimate_hub(node, graph, cycle_nodes):

    in_deg = graph.in_degree(node)
    out_deg = graph.out_degree(node)

    if out_deg >= 100 and in_deg <= 5 and node not in cycle_nodes:
        return True

    return False


# -----------------------------
# Velocity Bonus
# -----------------------------
def compute_velocity_bonus(account_id, df):

    user_tx = df[
        (df["sender_id"] == account_id) |
        (df["receiver_id"] == account_id)
    ]

    if len(user_tx) < 5:
        return 0

    time_span = (
        user_tx["timestamp"].max() -
        user_tx["timestamp"].min()
    ).total_seconds() / 3600

    if time_span < 24:
        return 3
    elif time_span < 72:
        return 1
    else:
        return 0


# -----------------------------
# MAIN ENGINE
# -----------------------------
def run_analysis(df: pd.DataFrame):

    from app.core.database import SessionLocal
    from app.repositories.analysis_repo import save_analysis
    from app.repositories.fraud_account_repo import update_fraud_account

    start_time = time.time()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    graph = build_graph(df)

    # -------- 1️⃣ Cycles --------
    cycle_rings = detect_cycles(graph)

    cycle_nodes = set()
    for ring in cycle_rings:
        cycle_nodes.update(ring["members"])

    # -------- 2️⃣ Smurf --------
    smurf_rings = detect_smurfing(df)

    # -------- 3️⃣ Shell --------
    shell_rings = detect_shell_layers(graph, cycle_nodes)

    all_rings = cycle_rings + smurf_rings + shell_rings

    ring_lookup = {}
    repetition_count = {}

    for ring in all_rings:
        for member in ring["members"]:
            ring_lookup.setdefault(member, ring)
            repetition_count[member] = repetition_count.get(member, 0) + 1

    # -------- 4️⃣ ML Scoring --------
    feature_df = build_node_features(graph, df)
    ml_scores = compute_anomaly_scores(feature_df)

    suspicious_accounts = []

    for _, row in ml_scores.iterrows():

        account_id = row["account_id"]
        ml_score = float(row["ml_score"])

        if is_legitimate_hub(account_id, graph, cycle_nodes):
            continue

        structural_score = 0
        pattern_type = None
        ring_id = ""

        if account_id in ring_lookup:
            ring = ring_lookup[account_id]
            pattern_type = ring["pattern_type"]
            ring_id = ring["ring_id"]

            if "cycle_length_3" in pattern_type:
                structural_score = 90
            elif "cycle_length_4" in pattern_type:
                structural_score = 93
            elif "cycle_length_5" in pattern_type:
                structural_score = 97
            elif "smurf" in pattern_type:
                structural_score = 94
            elif "shell" in pattern_type:
                structural_score = 88

        else:
            if ml_score < 97:
                continue
            pattern_type = "ml_anomaly"
            ring_id = f"RING_ML_{account_id}"

        velocity_bonus = compute_velocity_bonus(account_id, df)
        repetition_bonus = 2 if repetition_count.get(account_id, 0) > 1 else 0

        final_score = (
            0.8 * structural_score +
            0.2 * ml_score +
            velocity_bonus +
            repetition_bonus
        )

        final_score = min(round(final_score, 2), 100)

        suspicious_accounts.append({
            "account_id": account_id,
            "suspicion_score": final_score,
            "detected_patterns": [pattern_type],
            "ring_id": ring_id
        })

    suspicious_accounts = sorted(
        suspicious_accounts,
        key=lambda x: x["suspicion_score"],
        reverse=True
    )

    # -----------------------------
    # METRIC CALCULATION (if ground truth exists)
    # -----------------------------
    precision = None
    recall = None
    false_positive_rate = None
    
    if "is_fraud" in df.columns:
        flagged_ids = set([a["account_id"] for a in suspicious_accounts])
        true_fraud_ids = set(df[df["is_fraud"] == 1]["sender_id"].unique())
    
        tp = len(flagged_ids & true_fraud_ids)
        fp = len(flagged_ids - true_fraud_ids)
        fn = len(true_fraud_ids - flagged_ids)
    
        precision = round(tp / (tp + fp + 1e-8), 3)
        recall = round(tp / (tp + fn + 1e-8), 3)
        false_positive_rate = round(fp / (tp + fp + 1e-8), 3)
    
    summary = {
        "total_accounts_analyzed": graph.number_of_nodes(),
        "suspicious_accounts_flagged": len(suspicious_accounts),
        "fraud_rings_detected": len(all_rings),
        "processing_time_seconds": round(time.time() - start_time, 3),
        "precision": precision,
        "recall": recall,
        "false_positive_rate": false_positive_rate
    }

    # -----------------------------
    # DATABASE SAVE
    # -----------------------------
    db = SessionLocal()

    try:
        # Save summary
        record = save_analysis(
            db=db,
            graph_id="AUTO",
            risk_score=float(summary["suspicious_accounts_flagged"]),
            cycle=len(cycle_rings),
            smurf=len(smurf_rings),
            shell=len(shell_rings)
        )

        # Save / update repeat fraudsters
        for account in suspicious_accounts:
            update_fraud_account(db, account)

        print("Saved Analysis ID:", record.id)

    finally:
        db.close()

    # -----------------------------
    # RETURN RESPONSE
    # -----------------------------
    return {
        "suspicious_accounts": suspicious_accounts,
        "fraud_rings": [
            {
                "ring_id": r["ring_id"],
                "member_accounts": r["members"],
                "pattern_type": r["pattern_type"],
                "risk_score": r["risk_score"]
            } for r in all_rings
        ],
        "summary": summary
    }
