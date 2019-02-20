# ----------------------------------------------------------------------------------------------------------
# WRITTEN BY: Ruchi Saha ( https://github.com/ruchi09 )
#
# PROBLEM STATEMENT: This program implements the improved apriori using partitioning
#
# ------------------------------------------------------------------------------------------------------------------


from __future__ import division
from collections import namedtuple
from collections import Counter
from itertools import combinations
maxItems = 0
numRules = 0
minSupport =30  # in percentage
minConfidence = 15 # in percentage
datasetSize = 0
no_of_partition = 2





#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: The readData function takes filename (a .csv file) as argument to read
#               data from and stores the data as set of transactions/itemsets .
#
# PARAMETERS: file -> filename with path in string
#
# RETURN VALUE: x ->   set of itemsets
#----------------------------------------------------------------------------------------------------------

def readData(file):
    global datasetSize
    global maxItems
    items = set()
    fd = open(file, 'r')
    x = list()
    # y = list()
    for itemset in fd:
        a=list(map(int, itemset.strip().split(",")))
        # print a
        con  = frozenset(a)
        items = items | con
        datasetSize +=1
        # print datasetSize
        x.append(a)
    # print "\n\n" ,  x
    maxItems = len(items)
    return x





#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: The function nextFrequent performs cross on the provided itemsets and attempts to create
#               and find frequent itemsets for next level.
#
# PARAMETERS: itemsets -> list of frequent items in prev level (list of tuples)
#             dataset  -> database (list of tuples)
#
# RETURN VALUE: final_it ->  frequent itemsets for next level level (list of tuples)
#----------------------------------------------------------------------------------------------------------


def nextFrequent(itemsets,dataset):
    global minSupport
    it = set()

    # generating itemsets
    for i in range(0,len(itemsets)-1):
        ilen = len(itemsets[i])
        for j in range(i+1,len(itemsets)):
            jlen=len(itemsets[j])
            if (set(itemsets[i][:ilen-1]) == set(itemsets[j][:jlen-1])):
                new_itemset = list(itemsets[i])
                new_itemset.append(itemsets[j][jlen-1])
                it.add(tuple(new_itemset))

    # finding frequent ones
    final_it = list()
    for i in it:
        count =0
        for d in dataset:
            if set(i).issubset(set(d)):
                count+=1
        if count >= minSupport:
            final_it.append(i)
    return final_it







#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: Updates the support count of given itemsets over the given database
#
# PARAMETERS: items ->  (list of tuples)
#             dataset  -> database (list of tuples)
#
# RETURN VALUE: freq ->  frequent itemsets (list of tuples)
#----------------------------------------------------------------------------------------------------------

def updateSupport(items,dataset):
    freq = list()
    for i in items:
        count =0
        for d in dataset:
            if set(i).issubset(set(d)):
                count+=1
        if count > minSupport:
            freq.append(i)
    return freq






#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: Implements normal apriori algorithm
#
# PARAMETERS: dataset  -> database (list of tuples)
#
# RETURN VALUE: items ->  frequent itemsets (list of tuples)
#----------------------------------------------------------------------------------------------------------

def apriori(dataset):
    global maxItems
    items = list()
    freq = list()
    for i in range(1, maxItems):
        for j in range(i+1, maxItems+1):
            freq.append((i,j))

    # print "\n\n\n initial: ",freq

    freq = updateSupport(freq,dataset)
    print "\ninitial freq: ",freq
    for i in range(2,maxItems):
        items = items + freq
        freq = nextFrequent(freq,dataset)
        print "\n\nfreq = ", freq

        if len(freq)<=1:
            break

    return items





if __name__ == "__main__":

    global minSupport
    global datasetSize
    global no_of_partition

    dataset = readData("dataset.csv")
    minSupport = minSupport*datasetSize/(100 * no_of_partition) #assuming minSupport to be constant for each partition

    local_freq_items = set()

    for i in range(0,no_of_partition):
        print "\n\n\n[Partition ",i+1,"]-------------------------------------------------------------------------\n\n\n"
        data = dataset[i*datasetSize//no_of_partition : (i+1) * datasetSize//no_of_partition]
        item = apriori(data)
        local_freq_items = local_freq_items | set(item)

    minSupport = minSupport*no_of_partition
    final_it=updateSupport(list(local_freq_items),dataset)

    print "\n\n\n------------------------------------------------------------------------------\n\n final = ",final_it,"\n\n"
