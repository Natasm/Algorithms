class Node(object):
	def __init__(self, level=-1, profit=0, weight=1, bound=0 ):
		self.level = level
		self.profit = profit
		self.weight = weight
		self.bound = bound
		self.ratio = self.profit / self.weight
