import math
import numpy as np
from stack import Stack
from problem import Problem
from scipy.optimize import linprog
from utils import *
from file import *

#Configure input parameters for simplex method
#RETORNA = c(values), A(weights), b(capacitys), bounds(variables limites => (min, max))
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

#Append one restrict in problem
def appendRestrict(bounds, constraint):
	i, eq, val = constraint
	bounds_buff = list(bounds)

	if eq == '>=':
		bounds_buff[i] = (val, None)
	elif eq == '<=':
		bounds_buff[i] = (0, val)

	return bounds_buff

#Verify if exist some restrict for variable i
def existRestrict(bounds, i):
	min_ , max_ = bounds[i]
	if min_ != 0 or max_ != None: return True

#Getting lower bound of fractionary solution
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

	#Set variables simplex method
	c, A, b, bounds = setConfigVariables(W, k, v)
	tol = 1e-11
    
    #resolve simplex
	result = linprog(c, method='simplex', A_ub=A, b_ub=b, bounds=bounds, options={'tol': tol})

	if(result.success == False): return [solution, solution_variables]

	#First upper bound
	problem = Problem(c, A, b, bounds)
	problem.value_solution = result.fun * -1
	problem.variables = result.x

	#First lower bound integer
	relaxation, new_variables = getLowerBound(problem, v)
	solution = relaxation
	solution_variables = new_variables
	
	#Stack init
	stack = Stack()
	stack.add_stack(problem)

	while(not stack.isEmpty()):
		problem_stack = stack.pop_stack()

		#Rules for pruning
		if problem_stack.value_solution == None: continue
		if problem_stack.value_solution < solution: continue
		if isReadySolved(solutions_buffer, problem_stack.value_solution): continue

		if not existFractionary(problem_stack.variables): break

		solutions_buffer.append(problem_stack.value_solution)

		print(problem_stack.value_solution)
		print('Solution: ', solution)
		#print(problem_stack.variables)
		print(stack.get_size())

		#Variable choice to branch
		j = -1
		min_interval = None
		for var in range(len(problem_stack.variables)):
			f, i = math.modf(problem_stack.variables[var])
			if f != 0:
				dif_floor = problem_stack.variables[var] - math.floor(problem_stack.variables[var])
				dif_ceil = math.ceil(problem_stack.variables[var]) - problem_stack.variables[var]
				if min_interval == None: 
					min_interval = dif_ceil - dif_floor
					j = var
				else:
					if min_interval > (dif_ceil - dif_floor): 
						min_interval = dif_ceil - dif_floor
						j = var

		if j == -1: continue
		
		#Branching
		for f in range(1):

				# LEFT resolve - Upper bound fractionary
				problem_left = Problem(c, A, b)
				problem_left.bounds = appendRestrict(problem_stack.bounds, (j, '<=', math.floor(problem_stack.variables[j])))

				result = linprog(problem_left.c, method='simplex', A_ub=problem_left.A, b_ub=problem_left.b, bounds=problem_left.bounds, options={'tol': tol})

				if result.success == True:
					problem_left.value_solution = result.fun * -1
					problem_left.variables = result.x

				# RIGHT resolve - Upper bound fractionary
				problem_right = Problem(c, A, b)
				problem_right.bounds = appendRestrict(problem_stack.bounds, (j, '>=', math.ceil(problem_stack.variables[j])))

				result = linprog(problem_right.c, method='simplex', A_ub=problem_right.A, b_ub=problem_right.b, bounds=problem_right.bounds, options={'tol': tol})

				if result.success == True:
					problem_right.value_solution = result.fun * -1
					problem_right.variables = result.x

				# Lower bound LEFT integer
				NEW_RELAXATION, NEW_VARIABLES = getLowerBound(problem_left, v)
				if  NEW_RELAXATION != None and NEW_RELAXATION > solution:
					solution = NEW_RELAXATION
					solution_variables = NEW_VARIABLES

				# Lower bound RIGHT integer
				NEW_RELAXATION, NEW_VARIABLES = getLowerBound(problem_right, v)
				if NEW_RELAXATION != None and NEW_RELAXATION > solution:
					solution = NEW_RELAXATION
					solution_variables = NEW_VARIABLES

				if problem_right.value_solution != None and problem_right.value_solution > solution:
					stack.add_stack(problem_right) #Branching right

				if problem_left.value_solution != None and problem_left.value_solution > solution:
					stack.add_stack(problem_left) #Branching left

				#break

	return [solution, solution_variables]

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