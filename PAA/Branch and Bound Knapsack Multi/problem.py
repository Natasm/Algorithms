class Problem(object):
    
	def __init__(self, c=None, A=None, b=None, bounds=None):
		self.c = c #Vector values (objective function)
		self.A = A #Constrains (weights)
		self.b = b #Limits constraints (capacity of knapsacks)
		self.bounds = bounds #limits variables
		self.value_solution = None #Solution value
		self.variables = [] #Solution variables