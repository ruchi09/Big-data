from namedlist import namedlist
import numpy as np

vert_bit_map = namedlist('vert_bit_map','itset bitmap')
tree_node = namedlist('tree_node','head tail support')

def read_file(filename):
    count = 0
    f = open(filename,"r")
    line = f.readline()

    records = list()
    while(line != ""):
        count=count+1
        records.append(list(map(lambda x: str(x), line.strip().split(" "))))
        line = f.readline()
    f.close()
    return records


def compute_trans_vert_bitmap(records):
	l = []
	items = set()
	for transaction in records:
		items.update(transaction)
	items = sorted(list(items))

	for each in items:
		l.append(vert_bit_map(each,[False for i in range(len(records))]))

	for i in range(len(records)):
		for item in records[i]:
			for j in range(len(l)):
				if l[j].itset == item:
					l[j].bitmap[i] = True
					break
	return l

def compute_bit_map(bit_map,item):
	if len(item) == 1:
		for i in range(len(bit_map)):
			if list(bit_map[i].itset) == item:
				return(bit_map[i].bitmap)
				
	else:
		last_it = item[-1]
		for i in range(len(bit_map)):
			if bit_map[i].itset == last_it:
				last_bit_map = bit_map[i].bitmap
				break
		return list(np.array((compute_bit_map(bit_map,item[:-1]))) &  np.array(last_bit_map))


def find_support(bit_map,item):
	itemset_vertical_bitmap=compute_bit_map(bit_map,item)
	support_count = sum(itemset_vertical_bitmap)
	return support_count


def mafia_alg(current_node,mfi,bit_map,min_sup):

	leaf = True
	for i in range(len(current_node.tail)):
		new_node_head = list(current_node.head) + list(current_node.tail[i])
		new_node_support = find_support(bit_map,new_node_head)
		if new_node_support == current_node.support:				#PEP pruning
			current_node.head = sorted(list(set(current_node.head).union(set(new_node_head))))
		elif new_node_support>=min_sup:
			leaf = False
			new_node_tail = current_node.tail[i+1:]
			new_node = tree_node(new_node_head,new_node_tail,new_node_support)
			mafia_alg(new_node,mfi,bit_map,min_sup)

	if leaf:
		flag = 1
		for each in mfi:
			if set(current_node.head).issubset(set(each)):
				flag = 0
				break
		if flag==1:
			mfi.append(current_node.head)


def MAFIA(records,min_sup):
	trans_vert_bit_map = compute_trans_vert_bitmap(records)
	mfi = []
	items = [trans_vert_bit_map[i].itset for i in range(len(trans_vert_bit_map))]
	root = tree_node([],items,len(records))
	mafia_alg(root,mfi,trans_vert_bit_map,min_sup)
	return mfi




def main():
    min_sup = 3
    records = read_file("friend_data.txt")
    mfi = MAFIA(records,min_sup)
    print("MFI::")
    for each in mfi:
    	print(each)

    
if __name__ == '__main__':
    main()
