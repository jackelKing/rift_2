def detect_shell_layers(graph, cycle_nodes):

    rings = []
    ring_index = 500
    degree_map = dict(graph.degree())

    visited_mid = set()

    for start in graph.nodes():

        if start in cycle_nodes:
            continue

        if degree_map[start] <= 2:
            continue

        for mid1 in graph.successors(start):

            if mid1 in cycle_nodes:
                continue

            if degree_map[mid1] != 2:
                continue

            if mid1 in visited_mid:
                continue

            succ1 = list(graph.successors(mid1))
            if len(succ1) != 1:
                continue

            mid2 = succ1[0]

            if mid2 in cycle_nodes:
                continue

            if degree_map[mid2] != 2:
                continue

            succ2 = list(graph.successors(mid2))
            if len(succ2) != 1:
                continue

            end = succ2[0]

            if end in cycle_nodes:
                continue

            if graph.has_edge(end, start):
                continue

            rings.append({
                "ring_id": f"RING_L_{ring_index}",
                "members": [start, mid1, mid2, end],
                "pattern_type": "shell_layering",
                "risk_score": 88.0
            })

            visited_mid.add(mid1)
            visited_mid.add(mid2)
            ring_index += 1

    return rings