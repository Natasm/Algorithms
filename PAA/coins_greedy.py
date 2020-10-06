def coins_greedy(coins, n):
	coins.sort(reverse=True)

	s = []
	i = 0
	while(n > 0):
		if i > len(coins): return 'No solution'
		if coins[i] <= n:
			n = n - coins[i]
			s.append(coins[i])
		else:
			i = i + 1
	return s

#print(coins_greedy([1,5,10,25,100], 30)) 
print(coins_greedy([1,4,6], 8))
