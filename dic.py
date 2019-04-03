import random
from collections import namedtuple
import numpy as np

n=5
t=5
m=2
s=2
support = 2
confidence = 0.5
suspect=n
start=0
c = n
base = [0 for j in range(0,n)]
a=[[0 for i in range(t)] for j in range(n)]
it = list()
rules = list()
iteminfo = namedtuple("iteminfo","item count stage dones length")
allrules = namedtuple("allrules","lhs rhs confidence")

def gen_one_size_itemset() :

	for i in range(0,n) :
		temp = iteminfo(item = [0 for j in range(0,n)] ,count = 0 ,stage = 1 ,dones = 0 ,length = 1 )
		it.append(temp) 
		it[i].item[i] = 1

def read_m_trans() :

	global start
	for i in range (start*m,start*m+m):
		for j in range (0,c):
			if (list(np.array(a[i]) & np.array(it[j].item)) == it[j].item and it[j].dones<t) :
				it[j] = it[j]._replace(count=int(it[j].count)+1)
			it[j] = it[j]._replace(dones=int(it[j].dones)+1) 
	start += 1
	if (start == (t/m)) :
		for i in range (start*m,start*m+t%m) :
			for j in range (0,c):
				if (list(np.array(a[i]) & np.array(it[j].item)) == it[j].item and it[j].dones<t) :
					it[j] = it[j]._replace(count = int(it[j].count)+1)
				it[j] = it[j]._replace(dones = int(it[j].dones)+1)
		start = 0

def update_itemset_info() :

	global suspect
	for j in range (0,c):
		if it[j].dones == t :
			suspect -= 1
			if it[j].count >= support :
				it[j] = it[j]._replace(stage=3)
			else :
				it[j] = it[j]._replace(stage=0)

def dic() :

	global start,c,suspect	
	while (start < t/m and suspect != 0) :

		read_m_trans()
		update_itemset_info()
		for i in range (2,n) :
			counter = 0
			checklist = list()
			for j in range (0,c) :
				if(it[j].length == i-1 and (it[j].stage == 2 or it[j].stage == 3)) :
					counter += 1
			if(counter >= i) :
				for j in range (0,c) :
					if(it[j].length == i-1) :
						for k in range (0,n) :
							if(list(np.array(it[j].item) & np.array(it[k].item)) == base and (it[j].stage == 2 or it[j].stage == 3)) :
								checklist.append(list(np.array(it[j].item) | np.array(it[k].item)))
			temp = 0
			for j in range (0,len(checklist)) :
				if(checklist[j] != base) :
					temp = 1
					for k in range (0, len(checklist)) :
						if( j!= k and checklist[j] == checklist[k]) :
							temp += 1
							checklist[k] = base
				if(temp == i) :
					possible = 1	
					for k in range (0,c) :
						if(it[k].item == checklist[j]) :
							possible = 0
							break
					if (possible == 1 and checklist[j] != base) :
						c += 1
						suspect += 1
						temporary = iteminfo(item = checklist[j] ,count = 0,stage = 1,dones = 0,length = i)
						it.append(temporary)
						checklist[j] = base

if __name__ == "__main__":
	
	a = [[1, 0, 0, 1, 0],[1, 0, 0, 0, 1],[0, 1, 1, 0, 1],[1, 1, 1, 1, 1],[0, 1, 1, 1, 0]]
	
	# generate one size subsets
	gen_one_size_itemset()

	#start dic
	dic()

	#print the item sets and generated rules		
	print "frequent item sets : "
	for i in range (0,c) :
		if(it[i].stage == 3) : 
			print it[i]
	for r in range (2,n) :
		lor = r
		for i in range (0,c) :
			for j in range (0,c) :
				if(it[j].length < r and it[i].length == r) :
					if(list(np.array(it[j].item) & np.array(it[i].item)) == it[j].item) :
						for k in range (0,c) : 
							if((it[k].length == r-it[j].length)and(list(np.array(it[k].item) | np.array(it[j].item)) == it[i].item)) :
								if ((it[i].count/float(it[j].count)) >= confidence) :
									temp = allrules(lhs = it[j].item ,rhs = it[k].item, confidence = it[i].count/float(it[j].count))
									rules.append(temp)
	print "rules : "
	for i in range (0,len(rules)) :
		print rules[i]
	