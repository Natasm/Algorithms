import numpy as np

def knapsack_no_repeat(W, p, v):
	K = np.zeros((W + 1, len(p) + 1), dtype=np.float64)

	for i in range(1, len(p) + 1):
		for j in range(1, W + 1):
			K[j][i] = K[j][i - 1]
			
			if j >= p[i - 1]:
				if (K[j - p[i - 1]][i - 1] + v[i - 1]) > K[j][i - 1]:
					K[j][i] = K[j - p[i - 1]][i - 1] + v[i - 1]
				else:
					K[j][i] = K[j][i - 1]

	solution = []
	n = len(p)
	M = W
	while(n > 0):
		if K[M][n] != K[M][n - 1]:
			solution.insert(0, n - 1)
			M = M - p[n - 1]
		n = n - 1
	
	return K[W, len(p)], solution

print(knapsack_no_repeat(11, [3,4,5,9,4], [3,4,4,10,4]))