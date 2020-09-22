import numpy as np

def cutting_cloth(X, Y, a, b, p):
	C = np.zeros((X + 1,Y + 1))
	S = np.zeros((X + 1,Y + 1), dtype=np.dtype('O')) #WARNING - O (Object Python)

	for i in range(1, X + 1):
		for j in range(1, Y + 1):
			S[i][j] = []
			for k in range(0, len(p)):
				if ((a[k] <= i and b[k] <= j) or (b[k] <= i and a[k] <= j)) and (p[k] > C[i][j]): 
						C[i][j] = p[k]
						S[i][j] = [k]
			for k in range(1, i):
				if (C[k][j] + C[i - k][j]) > C[i][j]:
					C[i][j] = C[k][j] + C[i - k][j]
					S[i][j] = S[k][j] + S[i - k][j]
			for k in range(1, j):
				if (C[i][k] + C[i][j - k]) > C[i][j]:
					C[i][j] = C[i][k] + C[i][j - k]
					S[i][j] = S[i][k] + S[i][j - k]

	solution = []
	for i in S[X][Y]:
		solution.append(i)

	return C[X][Y], solution

print(cutting_cloth(20,20, [2,15,15], [2,15,5],[5,400,90]))

print(cutting_cloth(5,6,[3,2], [2,1], [5,1]))

print(cutting_cloth(9,10, [2,3,3,5], [3,2,5,3], [50,50,100,100]))
print(cutting_cloth(5,6,[1,1,2,2],[1,2,1,2], [1,3,2,3]))
print(cutting_cloth(5,6,[1,1,2,2],[1,2,1,2], [3,4,3,6]))

print(cutting_cloth(15,10,[8,3,8,3,3,3,2],[4,7,2,4,3,2,1], [66,35,24,17,11,8,2]))

print(cutting_cloth(40,70, [21,31,9,9,30,11,10,14,12,13,21],
	                       [22,13,35,24,7,13,14,8,8,7,4], 
                           [582,403,315,216,210,143,140,110,94,90,4]))

print(cutting_cloth(40,70, [31,30,29,28,27,26,25,24,33,22,31,29,17,15,16,15,23,21,19,9],
	                       [43,41,39,38,37,36,35,34,23,32,21,18,27,24,25,24,14,12,11,17],
	                       [500, 480, 460, 440, 420, 410, 400, 380, 360, 340, 320, 300, 280, 240,260, 240, 220, 180, 160, 140]))
