def subset_max(A):
	size_list = len(A)

	if not A or size_list <= 0: return []

	c = [None] * size_list
	s = [None] * size_list

	for m in range(0, size_list):
		c[m] = 1

		for i in range(m, -1, -1):
			if A[i] < A[m] and (c[i] + 1) > c[m]:
				c[m] = c[i] + 1
				s[m] = i

	subseq_max = 0
	pos = -1
	for m in range(0, size_list):
		if(c[m] > subseq_max):
			subseq_max = c[m]
			pos = m

	res = []
	rewind = -1
	while(pos != None):
		rewind = pos;

		res.append(A[pos])
		pos = s[pos]

		if rewind == pos: break;
    
	res_size = len(res)
	res_reverse = [None] * res_size

	for j in range(0, res_size):
		res_reverse[(res_size - 1) - j] = res[j]
	
	return res_reverse;

print(subset_max([0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15]))
			

	