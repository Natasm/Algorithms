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
		x = p.new_variable(integer=True, nonnegative=True)

		p.set_objective(p.sum(x[i]*self.v[i] for i in range(len(self.v))))

		p.add_constraint(p.sum(x[i]*self.k[i][0] for i in range(len(self.v))) <= self.W[0])
		p.add_constraint(p.sum(x[i]*self.k[i][1] for i in range(len(self.v))) <= self.W[1])
		p.add_constraint(p.sum(x[i]*self.k[i][2] for i in range(len(self.v))) <= self.W[2])

		for i in range(len(self.v)):
			p.add_constraint(x[i] <= 1)

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

def branch_and_bound(W=None, k=None, v=None):
	solution = -1
	solution_variables = []

	values_solutions = []

	problem = Problem(W, k, v)
	problem.resolve()
	
	stack = Stack()
	stack.add_stack(problem)
    
	while(not stack.isEmpty()):

		print('Begin')
		for natan in stack.get_values():
			print(natan.value_solution)
		print('End\n')

		problem_stack = stack.pop_stack()

		if problem_stack.value_solution == None: continue
		if problem_stack.value_solution < solution: continue
		if existValue(values_solutions, problem_stack.value_solution): continue
		
		if not existFractionary(problem_stack.variables): 
			if problem_stack.value_solution > solution:
				solution = problem_stack.value_solution
				solution_variables = problem_stack.variables
			continue

		values_solutions.append(problem_stack.value_solution)
		
		for j in range(len(problem_stack.variables)):
			f, i = math.modf(problem_stack.variables[j])
			if f != 0: 
				problem_new_less_than = Problem(W, k, v, problem_stack.constraints)
				problem_new_less_than.resolve(var_index=j, inequality="==", value=math.floor(problem_stack.variables[j]))

				problem_new_bigger_then = Problem(W, k, v, problem_stack.constraints)
				problem_new_bigger_then.resolve(var_index=j, inequality="==", value=math.ceil(problem_stack.variables[j]))

				stack.add_stack(problem_new_bigger_then)
				stack.add_stack(problem_new_less_than)
		

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

W, k, v = knapsack_with_file('C:/Users/natandemorais/Downloads/instances KP/large_scale/natan.txt', 3)
a = Problem(W,k,v)
#print(W)
#print(k)
#print(v)
print(a.resolve())
#print(branch_and_bound(W,k,v))






    

