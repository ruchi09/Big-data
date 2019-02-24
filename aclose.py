#A-close for closed frequent itemset mining

from namedlist import namedlist

freq = namedlist('freq','itset length support')
itemset = namedlist('itemset','itset length')


#Reading text file containing data set
def read_file(filename):
    count = 0
    f = open(filename,"r")
    line = f.readline()

    records = list()
    while(line != ""):
        count=count+1
        records.append(map(lambda x: str(x), line.strip().split(" ")))
        line = f.readline()
    f.close()
    return records


#To find all unique items in the database
def find_unique_items(records):
    l = []
    for each in records:
        for each1 in each:
            if each1 not in l:
                l.append(each1)
    return l

def find_support(records,item):
    count = 0
    for each in records:
        if set(item).issubset(set(each)):
            count+=1
    return count


def check_closure(item,sup,fi):
    for each in fi:
        if set(each.itset).issubset(set(item)) and each.length == len(item)-1:
            if each.support == sup:
                return 1
    return 0

def check_prefix(a,b):
    a1 = list(a)
    b1 = list(b)

    for i in range(len(a1)-1):
        if a1[i] != b1[i]:
            return 0
    return 1

def find_next_cand(records,items,fi):
    cand = []
    for i in range(len(items)):
        for j in range(i+1,len(items)):
            if check_prefix(items[i].itset,items[j].itset):
                key = sorted(set(items[i].itset).union(set(items[j].itset)))
                y = check_closure(key,find_support(records,key),fi)
                if y==0:
                    cand.append(itemset(key,len(key)))
    return cand


def Aclose(records,candidate,min_sup,fi):
    if candidate == []:
        return fi

    new = []
    new_cand = []
    for each in candidate:
        x = find_support(records,each.itset)
        if x >= min_sup:
            fi.append(freq(each.itset,each.length,x))
            new.append(each)
            #check if any immediate subsets of the set is already there in the fi with same support count
            #if not then add it to the fi set
            #y = check_closure(each.itset,x,fi)
            #if y == 0:
                #fi.append(freq(each.itset,each.length,x))
                #new.append(each)

    #find ci+1
    new_cand = find_next_cand(records,new,fi)
    #call Aclose with new candidate set
    return Aclose(records,new_cand,min_sup,fi)

def find_trans_set(records,item):
    trans = []
    for i in range(len(records)):
        if set(item.itset).issubset(set(records[i])):
            trans.append(i)
    return trans

def find_common_items(records,trans,unique):
    its = []
    
    for each in unique:
        ch = 1
        for i in trans:
            if each not in records[i]:
                ch = 0
                break
        if ch:
            its.append(each)
    return its


def generate(unique,records,generator):
    cfi = []
    for each in generator:
        trans = find_trans_set(records,each)
       
        it = find_common_items(records,trans,unique)
       # print "generator  Trans  it\n:",each.itset,"  ",trans,"  ",it
        if it not in cfi:
            cfi.append(it)
    return cfi



def main():

    min_sup = 3

    records = read_file("friend_data.txt")

    unique_set = find_unique_items(records)
    unique_set = sorted(unique_set)

    candidate = []

    for each in unique_set:
        candidate.append(itemset(list(each),1))

    generator = []

    generator = Aclose(records,candidate,min_sup,generator)
    #for each in generator:
        #print each.itset,"   ",each.support

    cfi = []
    cfi = generate(unique_set,records,generator)
    print "cfi:"
    for each in cfi:
        print each


if __name__ == '__main__':
    main()
