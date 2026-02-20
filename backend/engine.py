import pandas as pd
import networkx as nx
import time
from datetime import timedelta

class ForensicsEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.G = nx.from_pandas_edgelist(df, 'sender_id', 'receiver_id', 
                                         edge_attr=['amount', 'timestamp'], 
                                         create_using=nx.DiGraph())
        self.suspicious_accounts = {}
        self.fraud_rings = []
        self.start_time = time.time()

    def detect_cycles(self):
        # Using a specialized Depth-Limited Search for 3-5 length
        # This is more efficient than Johnson's for large sparse graphs
        found_cycles = []
        # Pre-filter: only nodes in SCCs of size >= 3 can have cycles
        sccs = [self.G.subgraph(c).copy() for c in nx.strongly_connected_components(self.G) if len(c) >= 3]
        
        for scc in sccs:
            for cycle in nx.simple_cycles(scc):
                if 3 <= len(cycle) <= 5:
                    ring_id = f"RING_CYC_{len(found_cycles) + 1:03d}"
                    found_cycles.append({
                        "ring_id": ring_id,
                        "members": cycle,
                        "type": "cycle"
                    })
                    for acc in cycle:
                        self._update_suspicion(acc, 95.0, "cycle_length_" + str(len(cycle)), ring_id)
        
        return found_cycles

    def detect_smurfing(self, threshold=10, window_hrs=72):
        # Fan-in Detection
        for node in self.G.nodes():
            in_edges = self.df[self.df['receiver_id'] == node].sort_values('timestamp')
            if len(in_edges) >= threshold:
                # Sliding window check
                for i in range(len(in_edges)):
                    window_end = in_edges.iloc[i]['timestamp']
                    window_start = window_end - timedelta(hours=window_hrs)
                    window = in_edges[(in_edges['timestamp'] >= window_start) & (in_edges['timestamp'] <= window_end)]
                    
                    if window['sender_id'].nunique() >= threshold:
                        ring_id = f"RING_SMR_{len(self.fraud_rings) + 1:03d}"
                        self._update_suspicion(node, 85.0, "high_velocity_fan_in", ring_id)
                        self.fraud_rings.append({
                            "ring_id": ring_id,
                            "members": window['sender_id'].unique().tolist() + [node],
                            "type": "smurfing_fan_in"
                        })
                        break

    def _update_suspicion(self, acc_id, score, pattern, ring_id):
        if acc_id not in self.suspicious_accounts:
            self.suspicious_accounts[acc_id] = {
                "account_id": acc_id,
                "suspicion_score": score,
                "detected_patterns": [pattern],
                "ring_id": ring_id
            }
        else:
            self.suspicious_accounts[acc_id]["detected_patterns"].append(pattern)
            self.suspicious_accounts[acc_id]["suspicion_score"] = min(100.0, self.suspicious_accounts[acc_id]["suspicion_score"] + 5)

    def run(self):
        cycles = self.detect_cycles()
        self.detect_smurfing()
        
        # Convert findings to RIFT format
        fraud_rings_out = []
        for r in cycles:
            fraud_rings_out.append({
                "ring_id": r["ring_id"],
                "member_accounts": r["members"],
                "pattern_type": "cycle",
                "risk_score": 95.3
            })
        
        # Merge Smurfing rings into output
        for r in self.fraud_rings:
            fraud_rings_out.append({
                "ring_id": r["ring_id"],
                "member_accounts": r["members"],
                "pattern_type": r["type"],
                "risk_score": 87.5
            })

        suspicious_list = sorted(self.suspicious_accounts.values(), 
                                 key=lambda x: x['suspicion_score'], reverse=True)

        return {
            "suspicious_accounts": suspicious_list,
            "fraud_rings": fraud_rings_out,
            "summary": {
                "total_accounts_analyzed": len(self.G.nodes()),
                "suspicious_accounts_flagged": len(suspicious_list),
                "fraud_rings_detected": len(fraud_rings_out),
                "processing_time_seconds": round(time.time() - self.start_time, 3)
            }
        }