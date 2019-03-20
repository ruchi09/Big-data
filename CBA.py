# ----------------------------------------------------------------------------------------------------------
# WRITTEN BY: Ruchi Saha     ( https://github.com/ruchi09 )
#
# PROBLEM STATEMENT: This program implements the CBA (Classification Based
#                     on Associations) Algorithm
#
# REFERENCE: Liu, B., Hsu, W. & Ma, Y. 1998. Integrating classification
#            and association rule mining. # KDD-98.
#
# ------------------------------------------------------------------------------------------------------------------



# -------------------------------------------------------------------------------------------------------------------
#                           PROGRAM BEGINS
# -------------------------------------------------------------------------------------------------------------------


from __future__ import division
from collections import namedtuple
from collections import Counter
maxItems = 0
numRules = 0
minSupport =15  # in percentage
minConfidence = 15 # in percentage
datasetSize = 0
ruleitems = namedtuple("ruleitems", "id condset condsupCount y rulesupCount")
rawrules = namedtuple("rawrules", "id condset y ")




#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: Formats and displays the argument
#
# PARAMETERS: A -> the set to be displayed
#             field_spaces -> the space to be used to display each field
#
# RETURN VALUE: void
#----------------------------------------------------------------------------------------------------------


def display(A,field_spaces):
    for namedtuple in A:

        assert len(field_spaces) == len(namedtuple._fields)
        string = "{0.__name__}( ".format(type(namedtuple))
        for f_n,f_v,f_s in zip(namedtuple._fields,namedtuple,field_spaces):
            string+= "{f_n}={f_v!r:<{f_s}}".format(f_n=f_n,f_v=f_v,f_s=f_s)
        print string+")"






# -------------------------------------------------------------------------------------------------------------------
#                                   ----- CBA RULE GENERATION  -----
# -------------------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: The readData function takes filename (a .csv file) as argument to read
#               data from and stores the data as set of rules of type 'rawrules'.
#
# PARAMETERS: file -> filename with path in string
#
# RETURN VALUE: x ->   set of rules of type 'rawrules'
#----------------------------------------------------------------------------------------------------------

def readData(file):
    global datasetSize
    global maxItems
    items = set()
    fd = open(file, 'r')
    x = set()
    # y = list()
    for itemset in fd:
        a=list(itemset.strip().split(","))
        # print a
        con  = frozenset(a[1:])
        items = items | con

        datasetSize +=1
        # print datasetSize
        qw= rawrules(id=datasetSize,condset = con, y = a[0])
        # print qw
        x.add(qw)
    # print "\n\n" ,  x
    maxItems = len(items)

    return x








#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: The genInitialRules function generates the 1-length rules from the dataset
#
# PARAMETERS: dataset -> set of rules of type 'rawrules'
#
# RETURN VALUE: x ->   set of initial rules of type 'ruleitems'
#----------------------------------------------------------------------------------------------------------

def genInitialRules(dataset):
    global numRules
    rulesupitems = list()
    condsupitems =list()

    F=set()
    for d in dataset:
        for i in d.condset:
            rulesupitems.append((i,d.y))
            condsupitems.append(i)


    count1 = Counter(rulesupitems)
    count2 = Counter(condsupitems)
    # maxItems = length(count2.keys())
    # print count1, "\n\n", count2,"\n\n\n\n\n\n"

    for i in count1:
        numRules+=1
        temp = ruleitems(id = numRules,condset = frozenset(i[0]), y=i[1],rulesupCount=count1[i],condsupCount=count2[i[0]] )
        # print i,count1[i] #,i[0], i.value(), count2(i.key[0])
        # print temp
        F.add(temp)
    # print "\n\n\n\n\n",F

    # print count.keys()
    return F







#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: The ruleSubset function takes a set of candidate ruleitems C
#                and a data case d to find all the ruleitems in C whose condsets
#                are supported by d.
#
# PARAMETERS: C -> set of candidate rules of type 'ruleitems'
#             d -> data case  of type 'rawrules'
#
# RETURN VALUE: x ->   set of supported rules of type 'ruleitems'
#----------------------------------------------------------------------------------------------------------

def ruleSubset(C, d):
    temp =set()
    for i in C:
        if i.condset.issubset(d.condset):
            temp.add(i)
    return temp









#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: Below function filter outs the rules which are frequent (support >minSupport)
#               and accurate (confidence > minConfidence) from the provided candidate rules
#
# PARAMETERS: F -> set of candidate rules of type 'ruleitems'
#
# RETURN VALUE: x ->   set of accurate and frequent rules of type 'ruleitems'
#----------------------------------------------------------------------------------------------------------

def genRules(F):

    freq = list()
    temp = list()
    # print "[Gen Rules  ]     ", F
    for i in F:
        sup = (i.rulesupCount/datasetSize)*100
        conf =  (i.rulesupCount/i.condsupCount)*100
        if sup >= minSupport:
            if conf >= minConfidence:
                try:            # if rule is already there, then choose the rule with max confidance
                    ind = temp.index(i.condset)
                    if (freq[ind].rulesupCount/freq[ind].condsupCount)*100 <conf:
                        freq.remove(freq[ind])
                        freq.append(i)
                except ValueError:
                    freq.append(i)
                    temp.append(i.condset)

    return set(freq)




#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: candidateGen function uses given seed set to generate new possibly
#               frequent ruleitems, called candidate ruleitems
#
# PARAMETERS: F -> seed set of type 'ruleitems'
#
# RETURN VALUE: candidate -> set of candidate rules of type 'ruleitems'
#----------------------------------------------------------------------------------------------------------

def candidateGen(F):
    #cross product and stuff will happen here
    # print "-----------?---------------- in candidate gen"
    global numRules
    candidate = set()
    F = list(F)
    n = len(F)
    r = list()
    # print "[candidateGen :]", F[0].condset

    for i in range(0,n-1):
        for j in range(i+1,n):
            # print "\n\nr=",r
            # print "\n\n f[i] = ",i,F[i]
            # print "\n\n f[j] = ",j,F[j]
            if (F[i].condset != F[j].condset) :
                # print "hello", n
                if len(F[i].condset & F[j].condset)+1 == len(F[i].condset) or len(F[i].condset)<=1:
                    # print "hi"
                    conset = F[i].condset | F[j].condset

                    try:            # if rule is already there, then choose the rule with max confidance
                        t = [conset, F[i].y]
                        ind = r.index(t)
                    except ValueError:
                        numRules+=1
                        temp = ruleitems(id = numRules,condset = frozenset(conset), y=F[i].y,rulesupCount=0,condsupCount=0 )
                        candidate.add(temp)
                        r.append([conset, F[i].y])



                    try:            # if rule is already there, then choose the rule with max confidance

                        t = [conset, F[j].y]
                        ind = r.index(t)

                    except ValueError:
                        numRules+=1
                        temp = ruleitems(id = numRules,condset = frozenset(conset), y=F[j].y,rulesupCount=0,condsupCount=0 )
                        candidate.add(temp)
                        r.append([conset, F[j].y])


    return  candidate







#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: Below function filters the rules based on min minSupport on rules support count
#
# PARAMETERS: C -> set of rules of type 'ruleitems'
#
# RETURN VALUE: x ->   set of frequent rules of type 'ruleitems'
#----------------------------------------------------------------------------------------------------------

def frequentRules(C):
    global datasetSize
    temp = set()
    for i in C:
        if i.rulesupCount>= datasetSize*minSupport/100:
            temp.add(i)
    return temp









#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: Below function is called CBA rule generation. It generates and
#               returns Class Association Rules (CARs)
#
# PARAMETERS: dataset -> set of rules of type 'rawrules'
#
# RETURN VALUE: x ->   set of CARs, each of type 'ruleitems'
#----------------------------------------------------------------------------------------------------------

def CBA_RG(dataset):

    F= genInitialRules(dataset) # 1 len rules

    CAR = genRules(F)

    while(len(F) !=0):

        # print "[CBA_RG (F):]"
        # display(F)
        C = candidateGen(F)
        # print "[CBA_RG (C):]"
        # display(C)
        # print "\n---------------------"
        for d in dataset:
            Cd = ruleSubset(C, d)   # Cd is a set of named tuples
            C = C-Cd
            for c1 in Cd:
                con = c1.condsupCount+1
                rul = c1.rulesupCount
                if d.y == c1.y:
                     rul+=1
                temp = ruleitems(id = c1.id,condset = c1.condset, y=c1.y,rulesupCount=rul,condsupCount=con )
                C.add(temp)

        F = frequentRules(C)
        CAR = CAR | genRules(F)   # set1.union(set2)

    return CAR




# -------------------------------------------------------------------------------------------------------------------
#                                   ----- CBA CLASSIFIER BUILDING  -----
# -------------------------------------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: Below function compares the rules for precendence
#
# PARAMETERS: r1,r2 ->  rules of type 'ruleitems'
#
# RETURN VALUE: result ->   0 if r2>r1, 1 if r1>r2
#----------------------------------------------------------------------------------------------------------

def compareRules(r1,r2):
    r1_conf = r1.rulesupCount*1000/r1.condsupCount
    r2_conf = r2.rulesupCount*1000/r2.condsupCount
    result =0
    if r1_conf > r2_conf:
        result =1
    elif r1_conf == r2_conf:
        if r1.rulesupCount > r2.rulesupCount:
            result = 1
        elif r1.rulesupCount == r2.rulesupCount:
            if r1.id<r2.id:
                result = 1

    return result



#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: sortRules function sorts the rules acccording to prefernece
#
# PARAMETERS: R ->  set of rules of type 'ruleitems'
#
# RETURN VALUE: R ->  list of rules of type 'ruleitems'
#----------------------------------------------------------------------------------------------------------

def sortRules(R):

    R = list(R)
    flag=1
    while flag:
        flag=0
        for i in range(0,len(R)):
            for j in range(0,len(R)-1):
                if compareRules(R[j],R[j+1])==0:
                    temp = R[j]
                    R[j] = R[j+1]
                    R[j+1] = temp
                    flag=1
    print "\n index  0  in sorted rules   ",R[0],"\n\n"
    print "\n\n Sorted rules:\n"
    display(R,(10,30,10,10,5))
    return R




#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: selectDefault function selects the default class for the given classifier
#               by selecting the most common class from th remaining daatabase
#
# PARAMETERS: dataset ->  set of rules of type 'rawrules'
#
# RETURN VALUE: most common class
#----------------------------------------------------------------------------------------------------------


def selectDefault(dataset):
    classes = list()
    for i in dataset:
        classes.append(i.y)

    count =  Counter(classes)
    # print "\n\n @@@@@@@@@@@@@@@ [in selectDefault]  ", count
    # print count.most_common(1)
    return count.most_common(1)




#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: satisfies function checks whether data 'd'  satisfies the conditions of rule 'r'
#
# PARAMETERS: d -> named tuple of type 'rawrules'
#             r ->  named tuple of type 'rawrules'
#
# RETURN VALUE: result ->  True if the condition is satisfied, False otherwise
#----------------------------------------------------------------------------------------------------------


def satisfies(d,r):
    result = False
    if d.condset.issubset(r.condset):
            result = True
    # print "\n [In satisfies]", d,r,result
    return result



#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: computeErrors function computes the total error of C. This
#               is the sum of the number of errors that have been made
#               by all the selected rules in C and the number of errors to
#               be made by the default class in the training data.
#
# PARAMETERS: dataset -> set of named tuple of type 'rawrules'
#             C -> list of named tuple of type 'rawrules'
#             default_class -> an integer representing a class label
#
# RETURN VALUE: error -> list representing no of errors of each rule
#----------------------------------------------------------------------------------------------------------


def computeErrors(dataset,C, default_class):
    # print "\n !!!!!!!!!!!!!!!!!!!!!!!!!!! computeErrors C =",C
    n = len(C)
    error = [0 for i in range (0,n+1)]

    for d in dataset:
        classified = False
        for i in range(0,n):
            if(satisfies(d,C[i])):
                classified = True
                if d.y != C[i].y:
                    error[i] +=1
                break

        if classified ==False:
            if default_class != d.y:
                error[n]+=1
    return error






#----------------------------------------------------------------------------------------------------------
# DESCRIPTION: CBA_CB function implements naive classifier builder in CBA algorithm
#
# PARAMETERS: CAR ->  set of class association rules of type 'ruleitems'
#             dataset -> set of rules of type 'rawrules'
#
# RETURN VALUE: C ->  list of rules of type 'ruleitems' representing classifier
#----------------------------------------------------------------------------------------------------------

def CBA_CB(CAR, dataset):

    global numRules
    R= sortRules(CAR)
    # print "\n\n [cmjgdsiu]  Sorted rules:\n"
    # display(R,(10,30,10,10,5))
    C = list()
    error = list()
    original_dataset = dataset
    default_class = 0
    for r in R:
        temp=set()
        marked =0
        for d in dataset:
            # print d
            if satisfies(d,r):
                if r.y == d.y:
                    temp.add(d)
                    marked =1
                    # print "\n--------- d satisfies r"
                    # print d.id,r.id, d.y,r.y

        if marked ==1:
            C.append(r)
            dataset = dataset - temp
            default_class = selectDefault(dataset)
            # print "\n\n------------------------------- in CB, \n "
            # display(C,(10,30,10,10,5))
            error = computeErrors(original_dataset,C,default_class)

    print "\n\nInitial Classifier: "
    display(C,(10,30,10,10,5))
    print "\ninitial error :", error
    p = error.index(min(error))
    C = C[0:p+1]
    default_class = selectDefault(original_dataset)
    default_class = default_class[0][0]
    error = computeErrors(original_dataset,C,default_class)
    numRules+=1
    con = [str(i) for i in range(1,maxItems+1)]
    temp = ruleitems(id = numRules,condset = frozenset( con  ), y=default_class,rulesupCount=0,condsupCount=0 )
    C.append(temp)



    return C, error







if __name__ == "__main__":
    # print "inside main"
    # numRules = 0
    dataset=readData("itemsets.csv")
    # print "\n\n\n Dataset:"
    # display(dataset,(10,30,10))
    # print "reio", datasetSize
    x=CBA_RG(dataset)
    print "\n\n\n Class Association Rules:"
    display(x,(10,30,10,10,5))

    C, error = CBA_CB(x,dataset)
    print "\n\n\n Classifier: "
    display(C,(10,30,10,10,5))
    print "\n\n Training Error: ",error

    # sortRules(x)
