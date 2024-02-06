import pandas
import matplotlib.pyplot as plot
from math import sqrt
import seaborn

#b) K-means clustering algorithm
def kmeans(K, dataset):

    # randomly pick K(2) cluser centroids
    # (dataset.sample selects K(2) number of points from the data)
    centroids = (dataset.sample(n=K))

    plot.scatter(dataset["f1"], dataset["f2"], c="green")
    plot.scatter(centroids["f1"], centroids["f2"], c="red")
    plot.xlabel("F1")
    plot.ylabel("F2")
    plot.title("Observations with Centroids")
    plot.show() # original dataset with centroids

    j=0
    # variable for if centroids changed - when diff = 0, centroids have not changed
    diff = 1

    while(diff != 0):
        dataset_diff = dataset
        dist_to = 1 # to track which centroid the distance is to
        # calculate euclidean distances between every record and centroids
        for _, row_centroid in centroids.iterrows():
            distance = [] # Euclidean Distances
            for _, row in dataset_diff.iterrows():
                d1 = (row_centroid["f1"] - row["f1"]) **2
                d2 = (row_centroid["f2"] - row["f2"]) **2
                d = sqrt(d1 + d2)
                distance.append(d)
            dataset[dist_to] = distance
            dist_to += 1

        cluster = []
        for _, row in dataset.iterrows():
            dist_min = row[1]
            group = 1
            for i in range(K):
                if dist_min > row[i+1]:
                    dist_min = row[i+1]
                    group = i+1
            cluster.append(group)
        dataset["Cluster"] = cluster

        # recalculate centroids by taking mean of all points 
        centroids_new = dataset.groupby(["Cluster"]).mean()[["f2", "f1"]]

        if j == 0:
            diff = 1
            j = j+1
        else:
            # determine if there are changes in the centroids positions
            diff = (centroids_new['f2'] - centroids['f2']).sum() + (centroids_new['f1'] - centroids['f1']).sum()
        centroids = centroids_new
    # print('-'*6)
    # print(dataset)
    # print('-'*6)
    return centroids, cluster

# c) Plot final clusters
def plot_final_clusters(K, centroids):
    color=['pink','blue']
    for k in range(K):
        data=csv[csv["Cluster"]==k+1]
        plot.scatter(data["f1"],data["f2"],c=color[k])
    plot.scatter(centroids["f1"],centroids["f2"],c='red')
    plot.xlabel('F1')
    plot.ylabel('F2')
    plot.title("Final Clusters")
    plot.show()

def final_report(K, cluster, centroids):
    # d) Report final cluster sizes
    print("Final Cluster Sizes")
    for k in range(K):
        print("Cluster size of cluster {}: {}".format(k+1, cluster.count(k+1)))
    print()
    # e) Report final centroids
    print("Final Centroids [f1, f2]")
    for i, row in centroids.iterrows():
        print("Centroid {}: [{}, {}]".format(i, row["f1"], row["f2"]))

# Main 

# a) Plot examples/observations
# read and process data from csv and save as dataset using pandas
csv = pandas.read_csv(r'A3/kmeans.csv')
original = seaborn.scatterplot(x="f1", y="f2", data=csv, c="green")
plot.xlabel("F1")
plot.ylabel("F2")
plot.title("Original Data / Observations")
plot.show()

# number of clusters
K=2

centroids, cluster = kmeans(K, csv)
plot_final_clusters(K, centroids)
final_report(K, cluster, centroids)