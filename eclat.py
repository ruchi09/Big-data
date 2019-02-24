#ECLAT

from namedlist import namedlist

freq = namedlist('freq','itemset support')
items = namedlist('items','itset trans_set length')
rules = namedlist('rules','ant cons conf')

#To find all unique items in the database
def find_unique_items(records):
	l = []
	for each in records:
		for each1 in each:
			if each1 not in l:
				l.append(each1)
	return l

def find_transaction_set(records,item):
	l = []
	for i in range(len(records)):
		if item in records[i]:
			l.append(i)
	return set(l)


def check_prefix(a,b):
	a1 = list(a)
	b1 = list(b)

	for i in range(len(a1)-1):
		if a1[i] != b1[i]:
			return 0
	return 1


#recursive ECLAT function
def ECLAT(item,min_sup,fi):
	if item == []:
		return fi
	new = []
	#print "start fi:",fi
	for each in item:
		if each.length >= min_sup:
			#print "frequent:",each
			fi.append(freq(each.itset,each.length))
			new.append(each)
	#print "new", new
	#print "fi:",fi
	#k=0
	new_items = []
	for i in range(len(new)):
		for j in range(i+1,len(new)):
			if(check_prefix(new[i].itset,new[j].itset)):					
				#print "CHECK:",sorted(set(new[i].itset).union(set(new[j].itset)))
				key = sorted(set(new[i].itset).union(set(new[j].itset)))
				common_trans = (new[i].trans_set.intersection(new[j].trans_set))
				new_items.append(items(list(key),common_trans,len(common_trans)))
				#print new_items[k]
				#k+=1

	return ECLAT(new_items,min_sup,fi)
	

#To read the data file
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


def is_bit_set(num, bit):
	return num & (1 << bit) > 0


#To find all subsets of given itemset
def find_subsets(itemset):
	sets = []
	for i in range(1 << len(itemset)):
		subset = [itemset[bit] for bit in range(len(itemset)) if is_bit_set(i, bit)]
		if subset!=[] and subset!=itemset:
			sets.append(subset)
	#print "subsets of",itemset,':',sets
	return sets

def find_confidence(set_a,lhs,fi):
	#print set_a
	sxy = 0
	sx = 0
	for each in fi:
		if set_a==each.itemset:
			sxy = each.support
		if lhs == each.itemset:
			sx = each.support
	support = (float(sxy)/sx)
	#print support
	return support


#To find association rules
def find_rules(fi,min_conf):
	ar = []
	for each in fi:
		if len(each.itemset)>1:
			x = find_subsets(each.itemset)
			for each1 in x:
				conf = find_confidence(each.itemset,each1,fi)
				if conf >= min_conf:
					lhs = list(each1)
					rhs = list(set(each.itemset).difference(set(lhs)))
					ar.append(rules(lhs,rhs,conf))

	return ar



def main():
	#minimum support
	min_sup = 3
	#min confidence
	min_conf = 0.7

	records = read_file("friend_data.txt")

	unique_set = find_unique_items(records)
	unique_set = sorted(unique_set)
	#print "unique_set: ",unique_set

	#all items
	it = []
	#i = 0
	for each in unique_set:
		x = find_transaction_set(records,each)
		it.append(items(list(each),x,len(x)))
		#print it[i]
		#i+=1

	fi = []
	fi = ECLAT(it,min_sup,fi)

	print "frequent itemsets:"
	for each in fi:
		print each


	print " "
	print " "

	print "association rules:"
	ar = find_rules(fi,min_conf)
	for each in ar:
		print each

if __name__ == '__main__':
	main()
