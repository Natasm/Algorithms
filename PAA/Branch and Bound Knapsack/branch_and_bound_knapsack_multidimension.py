import math
import numpy as np
from scipy.optimize import linprog

class Stack(object):
	def __init__(self):
		self.date = []
	
	def isEmpty(self):
		return len(self.date) == 0

	def add_stack(self, element):
		self.date.append(element)

	def pop_stack(self, level):
		if not self.isEmpty():
			#self.date.sort(key=lambda element:element.value_solution, reverse=True)
			#element = self.date.pop(0)
			#self.date = []
			#return element
			return self.date.pop(-1)
		else: return None

	def get_size(self):
		return len(self.date)

	def get_values(self):
		return self.date

class Problem(object):

	def __init__(self, c=None, A=None, b=None, bounds=None):
		self.c = c
		self.A = A
		self.b = b
		self.bounds = bounds
		self.value_solution = None
		self.variables = []

def existFractionary(array):
	for element in array:
		f, i = math.modf(element)
		if f != 0: return True
	return False

def existValue(array, value):
	for element in array:
		if element == value: return True
	return False

def setConfigVariables(W, k, v):
	c = []
	
	A = []
	k1 = []
	k2 = []
	k3 = []
	
	b = []

	bounds = []

	for profit in v:
		c.append(-profit)
		bounds.append((0, None))

	for i in range(len(v)):
		k1.append(k[0][i])
		k2.append(k[1][i])
		k3.append(k[2][i])

	A.append(k1)
	A.append(k2)
	A.append(k3)

	for capacity in W:
		b.append(capacity)

	return (c, A, b, bounds)

def appendRestrict(bounds, constraint):
	i, eq, val = constraint
	bounds_buff = list(bounds)

	if eq == '>=':
		bounds_buff[i] = (val, None)
	elif eq == '<=':
		bounds_buff[i] = (0, val)

	return bounds_buff

def existRestrict(bounds, i):
	min_ , max_ = bounds[i]
	if min_ != 0 or max_ != None: return True

def isEqual(arrX, arrY):
	if len(arrX) != len(arrY): return False
	for i in range(len(arrX)):
		if arrX[i] != arrY[i]: return False
	return True

def isReadySolved(array, search):
	for element in array:
		sol, var = element
		sol_, var_ = search
		if (sol == sol_) and isEqual(var, var_): return True
	return False

def getLowerBound(problem, v):
	result = 0
	variables = [0] * len(v)

	for i in range(len(problem.variables)):
		result += math.floor(problem.variables[i]) * v[i]
		variables[i] = math.floor(problem.variables[i])
	return (result, variables)

def branch_and_bound(W=None, k=None, v=None):
	solution = -1
	solution_variables = []

	solutions_buffer = []

	c, A, b, bounds = setConfigVariables(W, k, v)
	tol = 1e-11

	result = linprog(c, method='simplex', A_ub=A, b_ub=b, bounds=bounds, options={'tol': tol})

	if(result.success == False): return [solution, solution_variables]

	problem = Problem(c, A, b, bounds)
	problem.value_solution = result.fun * -1
	problem.variables = result.x

	#print(problem.value_solution)

	#problem.resolve()
	#print(problem.variables)

	relaxation, new_variables = getLowerBound(problem, v)
	solution = relaxation
	solution_variables = new_variables

	#print('Main relaxation: ', [relaxation])
	
	stack = Stack()
	stack.add_stack(problem)

	level = 0
	p = 0

	while(not stack.isEmpty()):
		problem_stack = stack.pop_stack(level)

		if problem_stack.value_solution == None: continue
		if problem_stack.value_solution < solution: continue
		if problem_stack.value_solution < relaxation: continue
		if isReadySolved(solutions_buffer, (problem_stack.value_solution, problem_stack.variables)): continue

		solutions_buffer.append((problem_stack.value_solution, problem_stack.variables))

		print(problem_stack.value_solution)
		print('Solution: ', solution)
		#print(problem_stack.variables)
		print(stack.get_size())

		j = -1
		min_interval = None
		for var in range(len(problem_stack.variables)):
			f, i = math.modf(problem_stack.variables[var])
			if f != 0:
				dif_floor = problem_stack.variables[var] - math.floor(problem_stack.variables[var])
				dif_ceil = math.ceil(problem_stack.variables[var]) - problem_stack.variables[var]
				if min_interval == None: 
					min_interval = (dif_floor, dif_ceil)
					j = var
				else:
					lower, upper = min_interval
					if lower > dif_floor or upper > dif_ceil: 
						min_interval = (dif_floor, dif_ceil)
						j = var

		if j == -1: continue

		for t in range(1):

				# LEFT resolve - Upper bound
				problem_left = Problem(c, A, b)
				problem_left.bounds = appendRestrict(problem_stack.bounds, (j, '<=', math.floor(problem_stack.variables[j])))

				result = linprog(problem_left.c, method='simplex', A_ub=problem_left.A, b_ub=problem_left.b, bounds=problem_left.bounds, options={'tol': tol})

				if result.success == True:
					problem_left.value_solution = result.fun * -1
					problem_left.variables = result.x

				# RIGHT resolve - Upper bound
				problem_right = Problem(c, A, b)
				problem_right.bounds = appendRestrict(problem_stack.bounds, (j, '>=', math.ceil(problem_stack.variables[j])))

				result = linprog(problem_right.c, method='simplex', A_ub=problem_right.A, b_ub=problem_right.b, bounds=problem_right.bounds, options={'tol': tol})

				if result.success == True:
					problem_right.value_solution = result.fun * -1
					problem_right.variables = result.x

				# New lower bound left
				NEW_RELAXATION, NEW_VARIABLES = getLowerBound(problem_left, v)
				if  NEW_RELAXATION != None and NEW_RELAXATION > relaxation: 
					relaxation = NEW_RELAXATION
					#print('Nova relaxacao: ', NEW_RELAXATION)
					if relaxation > solution: 
						solution = relaxation
						solution_variables = NEW_VARIABLES

				# New lower bound right
				NEW_RELAXATION, NEW_VARIABLES = getLowerBound(problem_right, v)
				if NEW_RELAXATION != None and NEW_RELAXATION > relaxation: 
					relaxation = NEW_RELAXATION
					#print('Nova relaxacao: ', NEW_RELAXATION)
					if relaxation > solution: 
						solution = relaxation
						solution_variables = NEW_VARIABLES

				if problem_right.value_solution != None and problem_right.value_solution >= relaxation:
					stack.add_stack(problem_right)

				if problem_left.value_solution != None and problem_left.value_solution >= relaxation:
					stack.add_stack(problem_left)

				break

	return [solution, solution_variables]

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

	#print(W)
	#print(k)
	#print(v)

#capacity = [52,52,104]
#profits =  [60, 3456, 2880, 1950, 924, 143, 798, 456, 180, 247, 697, 1176, 2880, 3440, 1530, 2325, 1296, 3948, 324, 1000]
#weights =  [[30, 48, 36, 50, 22, 11, 38, 38, 3, 19, 41, 21, 20, 40, 34, 31, 24, 47, 27, 50],
#			  [1, 36, 40, 39, 14, 13, 21, 4, 30, 13, 17, 28, 48, 43, 15, 25, 27, 28, 12, 20],
#			  [19, 35, 41, 39, 50, 49, 46, 2, 21, 6, 31, 45, 43, 39, 14, 39, 25, 47, 40, 19]]

capacity = [52,52,104]
profits =  [60, 3456, 880, 1950, 924, 143, 4000, 5000, 1890, 247, 697, 1176, 2880, 3440, 1530, 2325, 1296, 3948, 324, 1000]
weights =  [[30, 48, 36, 50, 22, 11, 38, 38, 3, 19, 41, 21, 20, 40, 34, 31, 4, 47, 27, 50],
			  [1, 36, 40, 39, 14, 13, 21, 4, 3, 13, 17, 28, 48, 43, 15, 25, 27, 28, 12, 20],
			  [19, 35, 41, 39, 50, 49, 46, 2, 21, 6, 31, 45, 4, 39, 14, 39, 25, 47, 40, 19]]

capacity, weights, profits = knapsack_with_file('C:/Users/natandemorais/Desktop/key/facil4', 3)

#a = ProblemInteger(capacity, weights, profits)
#print(a.resolve())

#b = ProblemInteger(capacity, weights, profits)
#print(b.resolve())
#print(W)
#print(k)
#print(v)
print(branch_and_bound(capacity,weights,profits))






    

