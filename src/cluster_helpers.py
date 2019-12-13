from sklearn.cluster import KMeans
import numpy as np
import embed_helpers
import networkx as nx
from matplotlib import pyplot as plt

def get_kmeans_clusters(pc, k=4):
    cl = KMeans(n_clusters=k).fit(pc)
    return cl.labels_

def inertia_plot(pc, cluster_range=np.arange(2,15)):
    kmeans_fit = []
    inertia = []
    for nc in cluster_range:
        cl = KMeans(n_clusters=nc).fit(pc)
        kmeans_fit.append(cl)
        inertia.append(cl.inertia_)
        
    plt.plot(cluster_range, inertia)
    plt.ylabel("Within-cluster variance")
    plt.xlabel("Number Clusters")

def spectral_gap(evals):
    n_evals = len(evals)
    if n_evals==1:
        return 1
    return np.argmax(evals[1:] - evals[:-1]) + 1
    
def spectral_cluster(G, subsplit_thresh=15):
    subgraphs = [G.subgraph(cc) for cc in nx.connected_components(G)]
    evals, evecs = zip(*[embed_helpers.spectral_embedding(g) for g in subgraphs])
    max_clusters_allowed = [len(sg)//subsplit_thresh+1 for sg in subgraphs]
    n_clusters = [spectral_gap(ev[:m]) for ev, m in zip(evals, max_clusters_allowed)]
    do_subcluster = [len(sg)/nc > subsplit_thresh and nc>1 for sg, nc in zip(subgraphs, n_clusters)]
    
    cd = dict() # Dict from node to its cluster
    nextval = 1
    for i, sg in enumerate(subgraphs):
        if do_subcluster[i]:
            nc = n_clusters[i]
            evec = evecs[i]
            cl = get_kmeans_clusters(evec[:,:nc], nc)
            cd.update(dict(zip(list(sg.nodes), cl+nextval)))
            nextval +=nc
        else:
            cd.update(dict.fromkeys(list(sg.nodes), nextval))
            nextval +=1
            
    # Sort by nodes
    nodes, cluster = zip(*cd.items())
    return np.array(cluster)[np.argsort(nodes)]
    