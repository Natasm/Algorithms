import math
import numpy as np

class Stack(object):
	def __init__(self):
		self.date = []
	
	def isEmpty(self):
		return len(self.date) == 0

	def add_stack(self, element):
		self.date.append(element)

	def pop_stack(self):
		if not self.isEmpty():	return self.date.pop(-1)
		else: return None

	def get_size(self):
		return len(self.date)

	def get_values(self):
		return self.date

class Problem(object):

	def __init__(self, W=None, k=None, v=None, constraints=[]):
		self.value_solution = None
		self.variables = []
		self.constraints = []
		self.W = W
		self.k = k
		self.v = v

		for i in constraints:
			self.constraints.append(i)

	def resolve(self, var_index=None, inequality=None, value=None):
		p = MixedIntegerLinearProgram()
		x = p.new_variable(real=True, nonnegative=True)

		p.set_objective(p.sum(x[i]*self.v[i] for i in range(len(self.v))))

		p.add_constraint(p.sum(x[i]*self.k[0][i] for i in range(len(self.v))) <= self.W[0])
		p.add_constraint(p.sum(x[i]*self.k[1][i] for i in range(len(self.v))) <= self.W[1])
		p.add_constraint(p.sum(x[i]*self.k[2][i] for i in range(len(self.v))) <= self.W[2])

		for i in range(len(self.constraints)):
			variable_constraint, equality, value_constraint = self.constraints[i]
			if equality == '==': p.add_constraint(x[variable_constraint] == value_constraint)
			elif equality == '<=': p.add_constraint(x[variable_constraint] <= value_constraint)
			elif equality == '>=': p.add_constraint(x[variable_constraint] >= value_constraint)

		if inequality == '==':	
			p.add_constraint(x[var_index] == value)
			self.constraints.append((var_index, "==", value))
		elif inequality == '<=':
			p.add_constraint(x[var_index] <= value)
			self.constraints.append((var_index, "<=", value))
		elif inequality == '>=':	
			p.add_constraint(x[var_index] >= value)
			self.constraints.append((var_index, ">=", value))

		try:
			value_solution = round(p.solve(), 2)
			solution = p.get_values(x)

			variables = []
			for i in solution: variables.append(round(solution[i], 2))

			self.value_solution = value_solution
			self.variables = variables
    
			return [value_solution, variables]
		
		except:
			return None
			print("Solver failed: :(")

def existFractionary(array):
	for element in array:
		f, i = math.modf(element)
		if f != 0: return True
	return False

def existValue(array, value):
	for element in array:
		if element == value: return True
	return False

#Exist space? >= 0?
def exist_space(node_id, node_capacity, weights):
	if node_capacity[0] >= weights[node_id][0] and node_capacity[1] >= weights[node_id][1] and node_capacity[2] >= weights[node_id][2]:
			return True
	else: return False

#Capacity is > 0?
def valid_space(node_capacity):
	if node_capacity[0] > 0 and node_capacity[1] > 0 and node_capacity[2] > 0: return True
	else: return False

#Return weights and profits sorteds, with division of profits per weights and initial Node
def init_solution(capacity, weights, profits):
	profit_per_weight = []
	for i in range(len(profits)):
		profit_per_weight.append((i, profits[i] / (weights[0][i] + weights[1][i] + weights[2][i])))

	profit_per_weight.sort(key=lambda element:element[1], reverse=True)
    
	weights_buffer = np.zeros((len(profits), 3), dtype=float)
	for i in range(len(profit_per_weight)):
		weights_buffer[i][0] = weights[0][profit_per_weight[i][0]]
		weights_buffer[i][1] = weights[1][profit_per_weight[i][0]]
		weights_buffer[i][2] = weights[2][profit_per_weight[i][0]]
	weights = weights_buffer
	
	profits = [profits[element[0]] for element in profit_per_weight]

	capacity_buffer = []
	for element in capacity: capacity_buffer.append(element)

	relaxation = 0
	for i in range(len(profit_per_weight)):
		if not valid_space(capacity_buffer): break
		if exist_space(i, capacity_buffer, weights): 
			x = int(capacity_buffer[0] / weights[i][0])
			y = int(capacity_buffer[1] / weights[i][1])
			z = int(capacity_buffer[2] / weights[i][2])
			relaxation+= min(x,y,z) * profits[i]
			capacity_buffer[0]-= min(x,y,z) * weights[i][0]
			capacity_buffer[1]-= min(x,y,z) * weights[i][1]
			capacity_buffer[2]-= min(x,y,z) * weights[i][2]

	return (weights, profits, profit_per_weight, relaxation)

def branch_and_bound(W=None, k=None, v=None):
	solution = -1
	solution_variables = []

	values_solutions = []

	problem = Problem(W, k, v)
	problem.resolve()

	capacity, weights, profits, relaxation = init_solution(W, k, v)
	
	stack = Stack()
	stack.add_stack(problem)
    
	while(not stack.isEmpty()):
		problem_stack = stack.pop_stack()

		if problem_stack.value_solution == None: continue
		if problem_stack.value_solution < solution: continue
		if problem_stack.value_solution < relaxation: continue

		if not existFractionary(problem_stack.variables): 
			if problem_stack.value_solution > solution:
				solution = problem_stack.value_solution
				solution_variables = problem_stack.variables
			continue
		
		for j in range(len(problem_stack.variables)):
			f, i = math.modf(problem_stack.variables[j])
			if f != 0: 
				problem_new_less_than = Problem(W, k, v, problem_stack.constraints)
				problem_new_less_than.resolve(var_index=j, inequality="<=", value=math.floor(problem_stack.variables[j]))

				problem_new_bigger_then = Problem(W, k, v, problem_stack.constraints)
				problem_new_bigger_then.resolve(var_index=j, inequality=">=", value=math.ceil(problem_stack.variables[j]))

				stack.add_stack(problem_new_bigger_then)
				stack.add_stack(problem_new_less_than)

				break
		

	return [solution, solution_variables]

def knapsack_with_file(filepath, dimension):
	file = open(filepath, 'r')
    
	n = 0
	W = [0] * dimension

	for line in file:
		line_first = line.replace("\n", "").split(' ')
		n = int(line_first[0])
		W[0] = int(line_first[1])
		W[1] = int(line_first[2])
		W[2] = int(line_first[3])
		break

	k = np.zeros((n, dimension), dtype=float)
	v = []
    
	i = 0
	for line in file:
		if i == n: break
		line_subseq = line.replace("\n", "").split(' ')
		k[i][0] = (int(line_subseq[0]))
		k[i][1] = (int(line_subseq[1]))
		k[i][2] = (int(line_subseq[2]))
		v.append(int(line_subseq[3]))
		i = i + 1

	return (W, k, v)

	#print(W)
	#print(k)
	#print(v)

#a = Problem(50, [10,20,30], [60,100,120])
#print(a.resolve())
#print(branch_and_bound(50, [10,20,30], [60,100,120]))

#a = Problem(10, [2,3.14,1.98,5,3], [40,50,100,95,30])
#print(a.resolve())
#print(branch_and_bound(10, [2,3.14,1.98,5,3], [40,50,100,95,30]))

#a = Problem(15, [10,8,6,5], [24,17,12,6])
#print(a.resolve(), '\n\n')
#print(branch_and_bound(15, [10,8,6,5], [24,17,12,6]))

#print(branch_and_bound(7, [2,1,6,5],[10,7,25,24]))

#W, k, v = knapsack_with_file('C:/Users/natandemorais/Downloads/instances KP/large_scale/natan.txt', 3)

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
a = Problem(capacity,weights,profits)
#print(W)
#print(k)
#print(v)
print(a.resolve())
print(branch_and_bound(capacity,weights,profits))






    

