from numpy import array
from math import sqrt
from pyspark import SparkContext
from pyspark.mllib.clustering import KMeans, KMeansModel
from pyspark.mllib.clustering import BisectingKMeans, BisectingKMeansModel


def error(point,clusters):
    center = clusters.centers[clusters.predict(point)]
    return sqrt(sum([x**2 for x in (point - center)]))



def BisectingKMeans_clustering(parsedData):

    parsedData = data.map(lambda line: array([float(x) for x in line.split(' ')]))

    # Build the model (cluster the data)
    model = BisectingKMeans.train(parsedData, 2, maxIterations=5)


    print "\n-----------------------------------------------------------------------------"
    print "\n          Cluster Centers (BisectingKMeans)"
    print "\n-----------------------------------------------------------------------------"

    print model.clusterCenters


def Kmeans_clustering(parsedData):
    # Build the model (cluster the data)
    clusters = KMeans.train(parsedData, 2, maxIterations=10, initializationMode="random")
    print "\n-----------------------------------------------------------------------------"
    print "\n          Cluster Centers (kmeans)"
    print "\n-----------------------------------------------------------------------------"

    print clusters.clusterCenters
    # Evaluate clustering by computing Within Set Sum of Squared Errors

    WSSSE = parsedData.map(lambda point: error(point,clusters)).reduce(lambda x, y: x + y)
    print("Within Set Sum of Squared Error = " + str(WSSSE))



if __name__ =="__main__":
    sc = SparkContext("local", "first app")
    # Load and parse the data
    data = sc.textFile("./sample_kmeans_data.txt")
    parsedData = data.map(lambda line: array([float(x) for x in line.split(' ')]))
    Kmeans_clustering(parsedData)
    BisectingKMeans_clustering(parsedData)
