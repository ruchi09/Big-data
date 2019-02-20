# ----------------------------------------------------------------------------------------------------------
# WRITTEN BY: Ruchi Saha  ( https://github.com/ruchi09 )
#
# PROBLEM STATEMENT: This program implements the improved apriori using hashing
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

        # print qw
        x.append(a)
    # print "\n\n" ,  x
    maxItems = len(items)

    return x







def nextFrequent(itemsets,dataset):
    global minSupport
    it = set()

    for i in range(0,len(itemsets)-1):
        ilen = len(itemsets[i])
        for j in range(i+1,len(itemsets)):
            jlen=len(itemsets[j])
            if (set(itemsets[i][:ilen-1]) == set(itemsets[j][:jlen-1])):
                new_itemset = list(itemsets[i])
                new_itemset.append(itemsets[j][jlen-1])
                it.add(tuple(new_itemset))

    final_it = list()
    for i in it:
        count =0
        for d in dataset:
            if set(i).issubset(set(d)):
                count+=1
        if count >= minSupport:
            final_it.append(i)

    return final_it





def nextFrequent_hash(itemsets,i1):
    global minSupport
    bucket_size = 17
    hashtable = [ [] for _ in range(0,bucket_size) ]
    frequent = list()
    for i in itemsets:

        for j in range(0, len(i)-1):
            for k in range(j+1,len(i)):

                hash = (i[j]*10 + i[k])%bucket_size
                hashtable[hash].append((i[j],i[k]))



    for i in range(0,bucket_size):
        x = Counter(hashtable[i])
        print "\n\n\n",x
        for a in x.keys():
            print a,"\n\n\n"
            if x[a]>=minSupport:
                frequent.append(a)
    return frequent


    #dhfiuerg


def apriori(dataset):

    items = list()
    freq =list()
    for i in range(2,maxItems):
        if i<3:
            freq = nextFrequent_hash(dataset,i)
            print "\n\n\n\nfreq = ", freq
        else:
            freq = nextFrequent(freq,dataset)
            print "\n\n\n\nfreq = ", freq

        items = items + freq
        if len(freq)<=1:
            break
    return items


if __name__ == "__main__":
    global minSupport
    global datasetSize
    dataset = readData("dataset.csv")
    minSupport = minSupport*datasetSize/100
    items = apriori(dataset)
    print "\n\n\n\n",items
