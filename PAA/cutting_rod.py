from decimal import Decimal

def cutting_rod(P):
	n = len(P)
	r = [None]*(n + 1)
	s = [None]*n
	r[0] = 0

	for j in range(1, n + 1):
		q = -Decimal('Infinity')
		for i in range(j):
			c = P[i] + r[j - i - 1]
			if c > q:
				q = c
				s[j - 1] = i + 1
		r[j] = q
	
	print(r)
	print(s)

	res = []
	while(n > 0):
		res.append(s[n - 1])
		n = n - s[n - 1]
	return res


print('Cutting: ', cutting_rod([3, 7, 10, 11, 12, 15, 17]))