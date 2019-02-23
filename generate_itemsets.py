# ----------------------------------------------------------------------------------------------------------
#
# WRITTEN BY: Ruchi Saha   ( https://github.com/ruchi09 )
#
# PROBLEM STATEMENT: This program generates the dataset to be used by programs in this repository.
#                    It can generate the dataset for both classifier and ARM (by commenting the appropriate
#                     statements ).
#
# ------------------------------------------------------------------------------------------------------------------


import random as r



if __name__ =='__main__':
    f=open("dataset.csv","w")

    max_items = 5
    max_sequence = 5
    min_sequence = 2
    no_of_entries = 200
    no_of_classes = 2
    for _ in range(no_of_entries):
        items = r.randint(min_sequence,max_sequence)
        itemset = set()",
        while len(itemset)<items:
            ran = r.randint(1,max_items)
            itemset.add(str(ran))

        # itemset for classifier (first item is class label)
        # itemset = str(r.randint(1,no_of_classes))+","+ ",".join(itemset)

        #itemset for ARM
        itemset = ",".join(itemset)

        f.write(itemset+"\n")
    f.close()
