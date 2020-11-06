import numpy as np

#Read file and return capacity list (W), weights matrix(k) and values list(v)
def knapsack_with_file(filepath, dimension):
	file = open(filepath, 'r')
    
	n = 0
	W = [0] * dimension

	for line in file:
		line_first = line.replace("\n", "").split(' ')
		n = int(line_first[0])
		break

	for line in file:
		line_first = line.replace("\n", "").split(' ')
		W[0] = float(line_first[0])
		W[1] = float(line_first[1])
		W[2] = float(line_first[2])
		break

	k = np.zeros((dimension, n), dtype=float)
	v = []
    
	i = 0
	for line in file:
		if i == n: break
		line_subseq = line.replace("\n", "").split(' ')
		v.append(float(line_subseq[0]))
		k[0][i] = (float(line_subseq[1]))
		k[1][i] = (float(line_subseq[2]))
		k[2][i] = (float(line_subseq[3]))
		i = i + 1

	return (W, k, v)