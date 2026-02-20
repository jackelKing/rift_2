import networkx as nx

def detect_cycles(graph, min_len=3, max_len=5):

    rings = []
    ring_index = 1

    for component in nx.strongly_connected_components(graph):
        size = len(component)

        if min_len <= size <= max_len:
            rings.append({
                "ring_id": f"RING_{ring_index:03d}",
                "members": list(component),
                "pattern_type": f"cycle_length_{size}",
                "risk_score": 95.0
            })
            ring_index += 1

    return rings
