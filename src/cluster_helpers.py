from sklearn.cluster import KMeans
import numpy as np

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
