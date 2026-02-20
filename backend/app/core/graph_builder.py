import networkx as nx


def build_graph(df):
    return nx.from_pandas_edgelist(
        df,
        source="sender_id",
        target="receiver_id",
        edge_attr=["amount", "timestamp"],
        create_using=nx.DiGraph()
    )
