import pandas as pd


def build_node_features(graph, df):

    sent_agg = df.groupby("sender_id")["amount"].sum().rename("sent")
    received_agg = df.groupby("receiver_id")["amount"].sum().rename("received")

    in_degrees = dict(graph.in_degree())
    out_degrees = dict(graph.out_degree())

    all_nodes = list(graph.nodes())

    data = []

    for node in all_nodes:
        data.append([
            node,
            in_degrees.get(node, 0),
            out_degrees.get(node, 0),
            sent_agg.get(node, 0),
            received_agg.get(node, 0)
        ])

    return pd.DataFrame(
        data,
        columns=["account_id", "in_degree", "out_degree", "sent", "received"]
    )
