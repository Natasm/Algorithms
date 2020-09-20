def solution(S, v):
	solution = []
	max_value = 0
	for j in range(0, len(S)):
				if S[j] != None: 
					solution.append(str(j) + ' - ' + str(S[j]))
					max_value = max_value + (v[j] * S[j])
	return max_value, solution


def knapsack_fractionary(W, p, v):
	S = [None] * len(p)
	c = W

	for i in range(0, len(p)):
		if p[i] <= c:
			S[i] = 1
			c = c - p[i]
		else:
			S[i] = c / p[i]
			return solution(S, v)
	return solution(S, v)

print(knapsack_fractionary(50, [40,30,20,10,20], [840,600,400,100,300]))

		    