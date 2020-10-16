class NodeTree(object):
	def __init__(self, id_=0,capacity=0,objective=0,variables=[],relaxation=0):
		self.id = id_
		self.capacity = capacity
		self.objective = objective
		self.variables = variables
		self.relaxation = relaxation
