
def read_data(filename) :
	f=open(filename, "r")
	line = f.readline()
	data = list()
	count =0
	while(line != ""):
		count=count+1
		data.append(map(lambda x: x, line.strip().split(" ")))
		line = f.readline()
	return data

def data_to_num(t) :
	items = []
	k = 0
	r = [[0 for i in range(len(t[j]))]for j in range(len(t))]
	for i in range(len(t)) :
		for j in range(len(t[i])) :
			if(t[i][j] not in items) :
				r[i][j] = k
				items.append(t[i][j])
				k += 1
			else :
				r[i][j] = items.index(t[i][j]) 
	return r,items

def get_actual_output(o,m) :
	r = [[0 for i in range(len(o[j]))] for j in range(len(o))]
	for i in range(len(o)) :
		for j in range(len(o[i])) :
			r[i][j] = m[o[i][j]]
	return r

def generate_c1(t) :
	c1 = []
	items = []
	for i in range (len(t)) :
		for j in range (len(t[i])) :
			if(t[i][j] not in items) :
				items.append(t[i][j])
				l = [t[i][j]]
				c1.append(l)
	return c1

def generate_mfcs(t) :
	m = []
	l = []
	max = 0
	for i in range (len(t)) :
		for j in range (len(t[i])) :
			if(t[i][j] not in l) :
				l.append(t[i][j])
	m.append(l)
	return(m)

def cal_support(c,mfcs,t,k) :
	s = []
	cs = [0 for i in range(len(c[k]))]
	m = [0 for i in range(len(mfcs))]
	for i in range(len(c[k])) :
		for j in range(len(t)) :
			if(set(c[k][i]).issubset(set(t[j]))) :
				cs[i] += 1
	for i in range(len(mfcs)) :
		for j in range(len(t)) :
			if(set(mfcs[i]).issubset(set(t[j]))) :
				m[i] += 1
	s.append(cs)
	s.append(m)
	return s

def update_mfs(mfs,mfcs,x,s) :
	freq_mfcs = []
	flag = 0
	for i in range(len(mfcs)) :
		if(s[i] >=x and mfcs[i] not in mfs) :
			freq_mfcs.append(mfcs[i])
			flag = 1
	if(flag == 1) :
		mfs = mfs + freq_mfcs
	return mfs

def get_lk(ck,s,x,mfs) :
	freq_ck = []
	l = []
	flag = 1
	for i in range(len(ck)) :
		if(s[i] >= x) :
			freq_ck.append(ck[i])
	for i in range(len(freq_ck)) :
		flag = 1
		for j in range(len(mfs)) :
			if(set(freq_ck[i]).issubset(set(mfs[j]))) :
				flag = 0
				break
		if(flag == 1) :
			l.append(sorted(freq_ck[i]))
	return l,flag

def get_sk(ck,s,x) :
	infreq_ck = []
	for i in range(len(ck)) :
		if(s[i] < x) :
			infreq_ck.append(sorted(ck[i]))
	return infreq_ck

def mfcs_gen(mfcs,sk) :
	
	length = len(mfcs)
	for i in range(len(sk)) :
		j = 0 
		while j < length :
			if(set(sk[i]).issubset(set(mfcs[j]))) :
				temp = mfcs[j]
				del mfcs[j]
				for e in range(len(sk[i])) :
					flag = 0
					temp1 = temp[0:]
					temp1.remove(sk[i][e])
					for t in range(len(mfcs)) :
						if(set(temp1).issubset(set(mfcs[t]))) :
							flag = 1
							break
					if(flag == 0 and temp1 not in mfcs) :
						mfcs.append(list(temp1))
			length = len(mfcs)
			j += 1
	return mfcs

def same_prefix(a,b,k) :
	flag = 0
	for i in range(k):
		if(a[i] != b[i]) :
			flag = 1
			break
	if(flag == 1) :
		return False
	return True

def join_procedure(lk,k) :
	cnext = []
	for i in range(len(lk)-1) :
		for j in range(i+1,len(lk)) :
			if(same_prefix(lk[i],lk[j],k-1)) :
				cnext.append(list(set(lk[i]).union(set(lk[j]))))
			else :
				break
	return cnext

def recover(c,lk,mfs,x) :

	for k in range(len(lk)) :
		for j in range(len(mfs)) :
			if(same_prefix(lk[k],mfs[j],x-1)) :
				for i in range (j+1,len(mfs[j])) :
					temp = []
					temp = temp + lk[0:k]
					temp.append(mfs[j][i])
					c.append(temp)
	return c

def new_prune(ck,mfs,lk) :
	x = len(ck)
	i = 0
	while i < x :
		flag = 1
		for j in range(len(mfs)) :
			if(set(ck[i]).issubset(set(mfs[j]))) :
				flag = 0
				break
		if(flag == 0) :
			del ck[i]
			x = len(ck)
		else :
			for j in range(len(ck[i])) :
				temp = ck[i][0:]
				temp.remove(ck[i][j])
				if(temp not in lk) :
					del ck[i]
					x = len(ck)
					break
		i += 1
	return ck

def pincer_search(t,s) :
	lk = []
	sk = []
	k = 1
	mfs = []
	c = []
	lk.append([])
	sk.append([])
	c.append([0])
	c.append(generate_c1(t))
	mfcs = generate_mfcs(t)
	while (c[k] != []) :
		support = cal_support(c,mfcs,t,k)
		mfs = update_mfs(mfs,mfcs,s,support[1])
		print "mfs for ",k," -> ",mfs		
		temp,flag = get_lk(c[k],support[0],s,mfs)
		lk.append(temp)
		print "lk for ",k," -> ",lk[k]
		sk.append(get_sk(c[k],support[0],s))
		print "sk for ",k," -> ",sk[k]
		if(sk[k] != []) :
			mfcs = mfcs_gen(mfcs,sk[k])
		print "mfcs for ",k," -> ",mfcs
		temp1 = join_procedure(lk[k],k)
		print "possible candidate set for c",k+1," is : ",temp1
		if(flag == 0) :
			temp1 = recover(temp1,lk[k],mfs,k)
		print "after recovery : ",temp1
		temp1 = new_prune(temp1,mfs,lk[k])
		print "after pruning : ",temp1
		c.append(temp1)
		print "ck+1 for ",k," -> ",temp1
		k += 1
	support = cal_support(c,mfcs,t,k)
	mfs = update_mfs(mfs,mfcs,s,support[1])
	return mfs

def main() :
	minSupport = input("give minimum support value : ")
	file = raw_input("give filename for dataset : ")
	input_t = read_data(file)
	transactions,mapper = data_to_num(input_t)
	MFS = pincer_search(transactions,minSupport)
	print MFS,mapper
	mfs = get_actual_output(MFS,mapper)
	print "MFS obtained : ",mfs

if __name__ == '__main__':
	main()
