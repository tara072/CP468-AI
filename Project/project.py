import pandas
import matplotlib.pyplot as plot
from math import sqrt
import seaborn

# K-means clustering algorithm
def kmeans(K, dataset, xAxis, yAxis):

    # randomly pick K(2) cluser centroids
    # (dataset.sample selects K(2) number of points from the data)
    centroids = (dataset.sample(n=K))

    plot.scatter(dataset[xAxis], dataset[yAxis], c="green")
    plot.scatter(centroids[xAxis], centroids[yAxis], c="red")
    plot.xlabel(xAxis)
    plot.ylabel(yAxis)
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
                d1 = (row_centroid[xAxis] - row[xAxis]) **2
                d2 = (row_centroid[yAxis] - row[yAxis]) **2
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
        centroids_new = dataset.groupby(["Cluster"]).mean(numeric_only = True)[[yAxis, xAxis]]
        if j == 0:
            diff = 1
            j = j+1
        else:
            # determine if there are changes in the centroids positions
            diff = (centroids_new[yAxis] - centroids[yAxis]).sum() + (centroids_new[xAxis] - centroids[xAxis]).sum()
        centroids = centroids_new
    return centroids, cluster

# Plot final clusters
def plot_final_clusters(K, centroids, xAxis, yAxis):
    color=['pink','blue','green','purple', 'grey']
    for k in range(K):
        data=csv[csv["Cluster"]==k+1]
        plot.scatter(data[xAxis],data[yAxis],c=color[k])
    plot.scatter(centroids[xAxis],centroids[yAxis],c='red')
    plot.xlabel(xAxis)
    plot.ylabel(yAxis)
    plot.title("Final Clusters")
    plot.show()

def final_report(K, cluster, centroids, xAxis, yAxis):
    # Report final cluster sizes
    print("Final Cluster Sizes")
    for k in range(K):
        print("Cluster size of cluster {}: {}".format(k+1, cluster.count(k+1)))
    print()
    # Report final centroids
    print("Final Centroids [{}, {}]".format(xAxis, yAxis))
    for i, row in centroids.iterrows():
        print("Centroid {}: [{}, {}]".format(i, row[xAxis], row[yAxis]))

# Main 

try:
    # column to use for x-axis
    xAxis = input("Enter X-Axis: ").strip()
    # column to use for y-axis
    yAxis = input("Enter Y-Axis: ").strip()
    # number of clusters
    K = int(input("Enter Number of Clusters (Maximum of 5): ").strip())

    # Plot examples/observations
    # read and process data from csv and save as dataset using pandas
    csv = pandas.read_csv(r'Project/Mall_Customers.csv')
    original = seaborn.scatterplot(x=xAxis, y=yAxis, data=csv, c="green")
    plot.xlabel(xAxis)
    plot.ylabel(yAxis)
    plot.title("Original Data / Observations")
    plot.show()

    centroids, cluster = kmeans(K, csv, xAxis, yAxis)
    plot_final_clusters(K, centroids, xAxis, yAxis)
    final_report(K, cluster, centroids, xAxis, yAxis)

except ValueError as e:
    print("ValueError:", e)
except Exception as e:
    print("Error: ", e)