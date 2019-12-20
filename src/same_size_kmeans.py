from sklearn.cluster import KMeans
import numpy as np
import networkx as nx
from scipy.spatial import distance


def assign_clusters(points, ind, means, cl_size, nbc):
    """Input constant numbers of points to each clusters"""

    def get_dist(point):
        dist = distance.cdist(np.array([point]), np.array(means), "euclidean")
        return dist[0], np.amax(dist) - np.amin(dist)

    # Order points by the distance to their nearest cluster minus distance to the farthest cluster
    # (= biggest benefit of best over worst assignment)
    dists = list(map(lambda x: get_dist(x), points))
    ind_point = [(d[0], d[1], i) for d, i in zip(dists, ind)]

    dic = dict(zip(range(len(points)), ind_point))
    sort = sorted(dic.items(), key=lambda item: item[1][1])
    sort.reverse()

    # Assign points to their preferred cluster until this cluster is full
    clusters = {i: [] for i in range(nbc)}
    c_clusters = {i: [] for i in range(nbc)}
    for v in sort:
        dist_means = v[1][0]
        prefered_c = np.argmin(dist_means)
        while not prefered_c in c_clusters:
            np.put(dist_means, prefered_c, np.inf)
            prefered_c = np.argmin(dist_means)
        c_clusters[prefered_c] = c_clusters[prefered_c] + [(v[0], v[1][2])]
        if len(c_clusters[prefered_c]) == cl_size:
            clusters[prefered_c] = c_clusters[prefered_c]
            c_clusters.pop(prefered_c)
            if not c_clusters:
                c_clusters = clusters
    return clusters


def get_new_means(clusters, points):
    """Computes centroids of clusters"""
    means = []
    for k, v in clusters.items():
        mean = []
        for point in v:
            mean.append([points[point[0]]])
        means.append(np.mean(mean, axis=0)[0])
    return means


def eq_size_kmeans(points, ind, nbc, niter, random_state):
    """Perform variation of kmeans with equal cluster size adapted from an algorithm from
        https://elki-project.github.io/tutorial/same-size_k_means"""
    # Init
    # Compute the desired cluster size, n/k.
    n = len(points)
    cl_size = int(n / nbc)
    # Initialize means,using the means of a regular Kmeans
    means = (
        KMeans(n_clusters=nbc, random_state=random_state).fit(points).cluster_centers_
    )
    # Start iterating
    iter_ = 0
    while iter_ < niter:
        clusters = assign_clusters(points, ind, means, cl_size, nbc)
        get_new_means(clusters, points)
        iter_ += 1
    return clusters


def per_subgraph(uncon_graph, sub_cluster_num, points, random_state=0, niter=100):
    """Computes the same size kmeans variation for each connected sub graph of a graph.
        Each subgraph will have a number of clusters specified in sub_cluster_num
        """

    subgraphs = [uncon_graph.subgraph(g) for g in nx.connected_components(uncon_graph)]
    clusters_dicts = [
        eq_size_kmeans(
            points[list(graph.nodes)],
            list(graph.nodes),
            nbc,
            niter,
            random_state=random_state,
        )
        for graph, nbc in zip(subgraphs, sub_cluster_num)
    ]
    cluster_dict = {i: [] for i in range(7)}
    i = 0
    for dic in clusters_dicts:
        for k, v in dic.items():
            cluster_dict[i] = list(map(lambda x: x[1], v))
            i += 1

    clusters = np.zeros(points.shape[0])
    for k, v in cluster_dict.items():
        for ix in v:
            np.put(clusters, ix, k)
    return clusters
