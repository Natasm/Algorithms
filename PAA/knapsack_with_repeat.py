def knapsack_with_repeat(W, p, v):
	K = [0] * (W + 1)
	S = [-1] * (W + 1) 

	K[0] = 0
	S[0] = -1

	for i in range(1, W + 1):
		for j in range(0, len(p)):
			if p[j] <= i and (K[i - p[j]] + v[j]) > K[i]:
				K[i] = K[i - p[j]] + v[j]
				S[i] = j
    
	solution = []
	N = W
	while(N > 0):
		solution.append(S[N])
		N = N - p[S[N]]

	return K[W], solution

print(knapsack_with_repeat(8, [1,3,4,5], [10,40,50,70])) 