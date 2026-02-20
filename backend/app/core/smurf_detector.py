
def detect_smurfing(df, threshold=10, window_hours=72):

    suspicious = []

    df = df.sort_values("timestamp")

    grouped_out = df.groupby("sender_id")

    for sender, group in grouped_out:

        if len(group) < threshold:
            continue

        distinct_receivers = group["receiver_id"].nunique()

        if distinct_receivers < threshold:
            continue

        group = group.sort_values("timestamp")

        # Check burst window
        time_span = (
            group["timestamp"].max() -
            group["timestamp"].min()
        ).total_seconds() / 3600

        if time_span > window_hours:
            continue  # Not bursty → likely payroll

        # Check prior fan-in (aggregation required)
        incoming = df[df["receiver_id"] == sender]

        if len(incoming) < 5:
            continue  # No aggregation → payroll-like

        # Fragmentation check (small deposits then big dispersal)
        avg_in = incoming["amount"].mean()
        avg_out = group["amount"].mean()

        if avg_in > avg_out * 0.6:
            continue  # Not fragmented → payroll

        suspicious.append({
            "ring_id": f"RING_S_{sender}",
            "members": list(group["receiver_id"].unique()) + [sender],
            "pattern_type": "smurfing",
            "risk_score": 93.0
        })

    return suspicious
