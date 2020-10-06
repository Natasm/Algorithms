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

	def __init__(self):
		self.value_solution = None
		self.variables = []

	def resolve(self, var_index=None, inequality=None, value=None):
		p = MixedIntegerLinearProgram()
		x = p.new_variable(real=True, nonnegative=True)

		p.set_objective(17*x[0] + 12*x[1])

		p.add_constraint(10*x[0] + 7*x[1] <= 40)

		p.add_constraint(x[0] + x[1] <= 5)

		p.add_constraint(x[0] >= 0)

		p.add_constraint(x[1] >= 0)

		if inequality == '<=': p.add_constraint(x[var_index] <= value)
		elif inequality == '>=': p.add_constraint(x[var_index] >= value)
		
		try:
			value_solution = round(p.solve(), 2)
			solution = p.get_values(x)

			variables = []
			for i in solution: variables.append(round(solution[i], 2))

			self.value_solution = value_solution
			self.variables = variables
    
			return[value_solution, variables]
		
		except:
		 	print("Solver failed: :(")
		 	return None

def existFractionary(array):
	for element in array:
		f, i = math.modf(element)
		if f != 0: return True
	return False

def existValue(array, value):
	for element in array:
		if element == value: return True
	return False


def branch_and_bound():
	solution = -1
	solution_variables = []
	values_solutions = []

	stack = Stack()

	problem = Problem()
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
				problem_new_less_than = Problem()
				problem_new_less_than.resolve(var_index=j, inequality="<=", value=math.floor(problem_stack.variables[j]))

				problem_new_bigger_then = Problem()
				problem_new_bigger_then.resolve(var_index=j, inequality=">=",value=math.ceil(problem_stack.variables[j]))
 				
				stack.add_stack(problem_new_bigger_then)
				stack.add_stack(problem_new_less_than)
		

	return [solution, solution_variables]

print(branch_and_bound())





    

