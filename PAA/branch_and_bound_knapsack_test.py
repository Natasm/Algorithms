import math

class Stack(object):
	def __init__(self):
		self.date = []
	
	def isEmpty(self):
		return len(self.date) == 0

	def add_stack(self, element):
		self.date.append(element)

	def pop_stack(self):
		if not self.isEmpty():
			return self.date.pop(-1)
		else: return None

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

		p.add_constraint(p.sum(x[i]*self.k[i] for i in range(len(self.v))) <= self.W)

		for i in range(len(self.v)):
			p.add_constraint(x[i] <= 1)

		for i in range(len(self.v)):
			p.add_constraint(x[i] >= 0)

		for i in range(len(self.constraints)):
			variable_constraint, equality, value_constraint = self.constraints[i]
			p.add_constraint(x[variable_constraint] == value_constraint)

		if inequality == '==':	
			p.add_constraint(x[var_index] == value)
			self.constraints.append((var_index, "==", value))
		
		try:
			value_solution = round(p.solve(), 2)
			solution = p.get_values(x)

			variables = []
			for i in solution: variables.append(round(solution[i], 2))

			self.value_solution = value_solution
			self.variables = variables
    
			return[value_solution, variables]
		
		except:
			return None
		 	#print("Solver failed: :(")

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

	stack = Stack()

	problem = Problem(W, k, v)
	problem.resolve()
	stack.add_stack(problem)

	while(not stack.isEmpty()):

		problem_stack = stack.pop_stack()

		if problem_stack.value_solution == None: continue
		if not existFractionary(problem_stack.variables): 
			if problem_stack.value_solution > solution:
				solution = problem_stack.value_solution
				solution_variables = problem_stack.variables
			continue
		if existValue(values_solutions, problem_stack.value_solution): continue
		
		values_solutions.append(problem_stack.value_solution)
		
		for j in range(len(problem_stack.variables)):
			f, i = math.modf(problem_stack.variables[j])
			if f != 0: 
				problem_new_less_than = Problem(W, k, v, problem_stack.constraints)
				problem_new_less_than.resolve(var_index=j, inequality="==", value=0)

				problem_new_bigger_then = Problem(W, k, v, problem_stack.constraints)
				problem_new_bigger_then.resolve(var_index=j, inequality="==", value=1)

				stack.add_stack(problem_new_bigger_then)
				stack.add_stack(problem_new_less_than)
		

	return [solution, solution_variables]

#a = Problem(50, [10,20,30], [60,100,120])
#print(a.resolve())
#print(branch_and_bound(50, [10,20,30], [60,100,120]))

#a = Problem(10, [2,3.14,1.98,5,3], [40,50,100,95,30])
#print(a.resolve())
#print(branch_and_bound(10, [2,3.14,1.98,5,3], [40,50,100,95,30]))

#a = Problem(15, [10,8,6,5], [24,17,12,6])
#print(a.resolve(), '\n\n')
#print(branch_and_bound(15, [10,8,6,5], [24,17,12,6]))





    

