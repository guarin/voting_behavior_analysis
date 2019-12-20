from matplotlib import pyplot as plt
import holoviews as hv
from matplotlib.pyplot import figure
import numpy as np
import networkx as nx
import operator
import plot
import embed_helpers


def by_legislature(plot_fctn, vals):
    """
    Create a plot per legislature, using the specified plot_function 
    """
    plt.figure(figsize=(16, 4))
    for i, v in enumerate(vals):
        plt.subplot(1, 3, i + 1)
        plot_fctn(v)
        plt.title("Legislature " + str(i + 1))


def hv_by_legislature(plot_fctn, vals):
    """
    Create a Holoviews plot per legislature
    """
    plots = []
    for i, v in enumerate(vals):
        plt = plot_fctn(v)
        plt = plt.opts(frame_height=300)
        plt = plt.opts(frame_width=250)
        plots.append(plt.relabel("Legislature " + str(i + 1)))
    layout = hv.Layout(plots).opts(shared_axes=False)
    return layout


def write_names(name, party):
    return name + " (" + party + ")"


def plot_closeness(graph, councelor_df, selected_councelor_df, title, methods):
    """
        Plot ranking of harmonic centrality for a given list of graph
    """
    fig = figure(figsize=(20, 10))
    num = len(graph)
    axes = [fig.add_subplot(num, num, ix + 1) for ix in range(num)]
    for ix, ax in enumerate(axes):
        closeness = np.array(
            list(map(lambda x: round(x[1], 2), methods(graph[ix]).items()))
        )
        names = [
            write_names(x["FullName"], x["PartyAbbreviation"])
            for i, x in councelor_df[ix].iterrows()
        ]
        name_close_dict = dict(zip(names, (closeness)))
        s = np.asarray(sorted(name_close_dict.items(), key=operator.itemgetter(1)))
        name_new_pos = {k: i for i, k in enumerate(s[:, 0])}
        labels = [
            write_names(x["FullName"], x["PartyAbbreviation"])
            for i, x in selected_councelor_df[ix].iterrows()
        ]
        pos = [name_new_pos[name] for name in labels]
        y_val = list(map(float, s[:, 1]))
        ax.bar(s[:, 0], y_val)
        ax.set_xticks(pos)
        ax.set_xticklabels(labels)
        ax.set_ylim(min(y_val), max(y_val))
        for tick in ax.get_xticklabels():
            tick.set_rotation(80)
        ax.set_xlabel("Councillors Ranking")
        ax.set_ylabel("Harmonic centrality")
        ax.set_title(title[ix])
    return fig


def get_closeness(graph, councillor_df, selected_councillor_df, method):
    closeness = np.array(list(map(lambda x: round(x[1], 2), method(graph).items())))
    names = [
        write_names(x["FullName"], x["PartyAbbreviation"])
        for i, x in councillor_df.iterrows()
    ]
    name_close_dict = dict(zip(names, closeness))
    s = np.asarray(sorted(name_close_dict.items(), key=operator.itemgetter(1)))
    name_new_pos = {k: i for i, k in enumerate(s[:, 0])}
    labels = [
        write_names(x["FullName"], x["PartyAbbreviation"])
        for i, x in councillor_df.iterrows()
    ]
    selected_labels = [
        write_names(x["FullName"], x["PartyAbbreviation"])
        for i, x in selected_councillor_df.iterrows()
    ]
    pos = [name_new_pos[name] for name in labels]
    selected_pos = [name_new_pos[name] for name in selected_labels]
    y_val = list(map(float, s[:, 1]))
    return pos, selected_pos, y_val


def plot_clusters(cluster, color, graph, clusters, ncm, knn_graph_plot_pos):
    """
        Colors the clusters in graph
    """
    cluster_idx = [i for i, x in enumerate(clusters == cluster) if x]
    cluster_info = ncm.iloc[cluster_idx]
    cluster_pos = np.asarray([knn_graph_plot_pos[i] for i in cluster_idx])
    cluster_point = plot.nodes(cluster_pos, cluster_info)
    cluster_graph = cluster_point.options(color=color)
    return cluster_graph


def party_centrality_ranking(party_name, ncm, pc, federal_counsilor_info):
    info = ncm.loc[ncm["PartyAbbreviation"] == party_name]
    fc_info = federal_counsilor_info.loc[
        federal_counsilor_info["PartyAbbreviation"] == party_name
    ]
    party_pc = pc[info.index]
    party_knn_graph = embed_helpers.get_knn_graph(party_pc, k=5)
    return party_knn_graph, info, fc_info
