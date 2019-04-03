
def read_data(filename) :
	f=open(filename, "r")
	t = []
	line = f.readline()
	while(line != "") :
		t.append(map(lambda x: str(x), line.strip().split(" ")))
		line = f.readline()
	return t

def order(it,t,s) :
	w = []
	for i in range(len(it)) :
		temp = [it[i],0]
		for j in range(len(it)) :
			if(i != j) :
				count = 0
				for k in range(len(t)) :
					if(it[i] in t[k] and it[j] in t[k]) :
						count+= 1
				if(count>=s) :
					temp[1] += count
		w.append(temp)
	w = sorted(w,key = lambda x: x[1])
	for i in range(len(it)) :
		it[i] = w[i][0]
	return it

def format_t(t,s) :
	items = []
	for i in range(len(t)) :
		for j in range(len(t[i])) :
			if(t[i][j] not in items) :
				items.append(t[i][j])
	return(order(items,t,s))

def create_root(it,t) :
	c = []
	for i in range(len(it)) :
		temp = [[it[i]],[]]
		for j in range(len(t)) :
			if(it[i] in t[j]) :
				temp[1].append(j+1)
		c.append(temp)
	return c

def support(x,t) :
	s = 0
	for i in range(len(t)) :
		flag = 1
		for j in range (len(x)) :
			if(x[j] not in t[i]) :
				flag = 0
				break
		if(flag) :
			s += 1
	return s

def order_satisfy(xj,xi,w,t) :
	if(len(xj) == 1) :
		if(w.index(xj[0]) >= w.index(xi[0])) :
			return 1
	else :
		if(support(xj,t) >= support(xi,t)) :
			return 1
	return 0

def charm_property(pi,pj,t,s) :
	if(support(list(set(pi[0]).union(pj[0])),t) >= s) :
		if(pi[1] == pj[1]) :
			return 1
		elif(set(pi[1]).issubset(set(pj[1]))) :
			return 2
		elif(set(pj[1]).issubset(set(pi[1]))) :
			return 3
		else :
			return 4
	return 0

def charm_extend(p,t,s,o,c) :
	l = len(p)
	i = 0	
	while i<l :
		if(support(p[i][0],t) >= s) :
			z = [] 
			X = p[i][0]
			l = len(p)
			j = i
			while j < l :
				l = len(p)
				if(order_satisfy(p[j][0],p[i][0],o,t) and j!= i) :
					x = list(set(p[i][0]).union(set(p[j][0])))
					y = list(set(p[i][1]).intersection(set(p[j][1])))
					case = charm_property(p[i],p[j],t,s)
					if(case == 1) :
						del p[j]
						j -= 1
						l = len(p)
						k = 0
						while k < l :
							if(set(X).issubset(set(p[k][0]))) :
								p[k][0] = x
							k += 1
						k = 0
						while k < len(z) :
							if(set(X).issubset(set(z[k][0]))) :
								z[k][0] = list(set(p[j][0]).union(set(z[k][0])))
							k += 1
						x = list(set(X).union(set(p[j][0])))
					elif(case == 2) :
						k = 0
						while k < l :
							if(set(X).issubset(set(p[k][0]))) :
								p[k][0] = list(set(p[j][0]).union(set(p[k][0])))
							k += 1
						k = 0
						while k < len(z) :
							if(set(X).issubset(set(z[k][0]))) :
								z[k][0] = list(set(p[j][0]).union(set(z[k][0])))
							k += 1
						x = list(set(X).union(set(p[j][0])))
					elif(case == 3) :
						del p[j]
						j -= 1
						z.append([x,y])
					elif(case == 4) :
						z.append([x,y])
				l = len(p)
				j += 1
			if (z != []) :
				charm_extend(z,t,s,o,c)
			flag1 = 1
			for k in range(len(c)) :			
				if (p[i][0] in c[k]) :
					flag1 = 0
			if(flag1) :
				c.append(p[i][0])
		i += 1

def charm(t,s) :
	uio = format_t(t,s)
	root = create_root(uio,t)
	c = []
	charm_extend(root,t,s,uio,c)
	return(c)

def main() :
	min_support = input("give minimum support : ")
	transactions = read_data(raw_input("give input dataset file : "))
	print transactions
	#c = charm(transactions,min_support)
	#print "cfi : ",c	

if __name__ == '__main__':
	main()