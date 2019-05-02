import sys
import copy

from string import atoi
from pyspark import SparkContext, SparkConf

import aprioriWorker as apriori


def findFrequentItemsets(input, output, numPartitions, s, sc):
    """
    Find frequent item sets using the apriori transaction reduction
    algorithm in two stages.
    First stage: divide document and find frequent itemsets in each partition.
    Second stage: join local itemset candidates, distribute to workers and
    count actual frequency.
    Args:
        arg1 (string): Location of the data file
        arg2 (string): Where to save itemsets
        arg3 (int): Number of partitions to make. Leave empty for default
        arg4 (float): Threshold
        arg5 (SparkContext): Spark Context
    Returns:
        list: List of all the encountered frequent itemsets. There is no
        guarantee that all frequent itemsets were found. But if something is
        in the list, it must be a frequent itemset.
    """

    data = sc.textFile(input, numPartitions)

    numPartitions = data.getNumPartitions()

    count = data.count()

    threshold = s*count

    #split string baskets into lists of items
    baskets = data.map(lambda line: sorted([int(y) for y in line.strip().split(',')]))
    # print "\n\n baskets",baskets.collect()

    #treat a basket as a set for fast check if candidate belongs
    basketSets = baskets.map(set).persist()

    #each worker calculates the itemsets of his partition
    localItemSets = baskets.mapPartitions(lambda data: [x for y in apriori.get_frequent_items_sets(data, threshold/numPartitions).values() for x in y], True)
    # print "\n\n localItemSets", localItemSets.collect()

    #for reducing by key later
    allItemSets = localItemSets.map(lambda n_itemset: (n_itemset,1))

    #merge candidates that are equal, but generated by different workers
    mergedCandidates = allItemSets.reduceByKey(lambda x,y: x).map(lambda (x,y): x)

    #distribute global candidates to all workers
    mergedCandidates = mergedCandidates.collect()
    # print "\n\n mergedCandidates",mergedCandidates

    candidates = sc.broadcast(mergedCandidates)

    #count actual occurrence of candidates in document
    counts = basketSets.flatMap(lambda line: [(candidate,1) for candidate in candidates.value if line.issuperset(candidate)])
    # print "\n\n counts",counts.collect()

    #filter finalists
    finalItemSets = counts.reduceByKey(lambda v1, v2: v1+v2).filter(lambda (i,v): v>=threshold)

    #put into nice format
    finalItemSets = finalItemSets.map(lambda (itemset, count): ",".join([str(x) for x in itemset])+" ("+str(count)+")")

    # finalItemSets.saveAsTextFile(output)

    return finalItemSets


if __name__ == "__main__":

    APP_NAME = "transaction-reduction-apriori"

    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")

    sc  = SparkContext(conf=conf)

    # f_input = sys.argv[1]
    # f_output = sys.argv[2]
    # threshold = float(sys.argv[3])
    #
    #
    #
    # if len(sys.argv) > 4:
    #     numPartitions = int(sys.argv[4])
    # else:
    #     numPartitions = None

    f_input = "../dataset.csv"
    f_output = "./output"
    threshold = 0.4



    numPartitions = 4
    final_it = findFrequentItemsets(f_input, f_output, numPartitions, threshold, sc)

    print "\n\n   final :",final_it.collect()