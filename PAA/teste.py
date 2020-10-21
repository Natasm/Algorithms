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

		p.add_constraint(p.sum(x[i]*self.k[i] for i in range(len(self.v))) <= self.W)

		for i in range(len(self.v)):
			p.add_constraint(x[i] <= 1)

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

def knapsack_with_file(filepath):
	file = open(filepath, 'r')
    
	n = 0
	W = 0
	k = []
	v = []

	for line in file:
		line_first = line.replace("\n", "").split(' ')
		W = int(line_first[1])
		n = int(line_first[0])
		break
    
	i = 0
	for line in file:
		if i == n: break
		line_subseq = line.replace("\n", "").split(' ')
		v.append(int(line_subseq[0]))
		k.append(int(line_subseq[1]))
		i = i + 1

	return (W, k, v)

capacity, weights, profits = knapsack_with_file("C:/Users/natandemorais/Desktop/knapsack/data/knapPI_1_2000_1000_1")
problem = Problem(capacity, weights, profits)
print(problem.resolve())