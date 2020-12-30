import pandas as pd 
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from sklearn.metrics import silhouette_samples
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import linkage
import scipy.cluster.hierarchy as shc
from sklearn.cluster import KMeans, DBSCAN

from sklearn.cluster import AgglomerativeClustering


def knee_val(data):
    distortions = []
    for i in range(1, 11):
        km = KMeans(n_clusters=i, 
                    init='k-means++', 
                    n_init=10, 
                    max_iter=300, 
                    random_state=0)
        km.fit(data)
        distortions.append(km.inertia_)
    plt.plot(range(1,11), distortions, marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.show()

def siluete_val(data, y):    
    cluster_labels = np.unique(y)
    n_clusters = cluster_labels.shape[0]
    silhouette_vals = silhouette_samples(data, 
                                        y, 
                                        metric='euclidean')
    y_ax_lower, y_ax_upper = 0, 0
    yticks = []
    for i, c in enumerate(cluster_labels):
        c_silhouette_vals = silhouette_vals[y == c]
        c_silhouette_vals.sort()
        y_ax_upper += len(c_silhouette_vals)
        color = cm.jet(i / n_clusters)
        plt.barh(range(y_ax_lower, y_ax_upper), 
                c_silhouette_vals, 
                height=1.0, 
                edgecolor='none', 
                color=color)
        yticks.append((y_ax_lower + y_ax_upper) / 2)
        y_ax_lower += len(c_silhouette_vals)
    silhouette_avg = np.mean(silhouette_vals)
    plt.axvline(silhouette_avg,
                color="red", 
                linestyle="--") 
    plt.yticks(yticks, cluster_labels + 1)
    plt.ylabel('Cluster')
    plt.xlabel('Silhouette coefficient')
    plt.show()



zoo_data = pd.read_csv("zoo_data-1.csv", encoding = 'utf-8', 
                              index_col = ["animal_name"]) 




clusters = 5
  
kmeans = KMeans(n_clusters = clusters) # .fit(zoo_data) 
y_km = kmeans.fit_predict(zoo_data)

dbscan = DBSCAN(eps=1.5, min_samples=3) # .fit(zoo_data)
y_db = dbscan.fit_predict(zoo_data)

# siluete_val(zoo_data, y_km)
# siluete_val(zoo_data, y_db)


row_clusters = linkage(zoo_data.values, method='complete', metric='euclidean')
l = list(zoo_data.index.values)
# row_dendr = dendrogram(row_clusters, labels=l)

# row_dendr = shc.dendrogram(shc.linkage(zoo_data, method='ward'), labels=l)
row_dendr = shc.dendrogram(shc.linkage(zoo_data, method='ward', metric='euclidean'), labels=l)

plt.tight_layout()
plt.ylabel('Euclidean distance')
plt.show()

cluster = AgglomerativeClustering(n_clusters=4, affinity='euclidean', linkage='ward')
y_hc = cluster.fit_predict(zoo_data)


siluete_val(zoo_data, y_km)
siluete_val(zoo_data, y_db)
siluete_val(zoo_data, y_hc)


