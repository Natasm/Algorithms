class Node(object):
	def __init__(self, content):
		self.content = content
		self.incidents = []
		self.neighbors = []
		self.in_degree = 0
		self.out_degree = 0
		self.sort = 0

	def add_neighbor(self, neighbor):
		self.neighbors.append(neighbor)
		self.out_degree = self.out_degree + 1

	def add_incident(self, incident):
		self.incidents.append(incident)
		self.in_degree = self.in_degree + 1

	def insert_sort(self, sort):
		self.sort = sort

	def get_content(self):
		return self.content

	def get_in_degree(self):
		return self.in_degree

	def get_out_degree(self):
		return self.out_degree

	def get_neighbors(self):
		return self.neighbors

	def get_incidents(self):
		return self.incidents

	def pop_in_degree(self, size):
		self.in_degree = self.in_degree - size

	def pop_out_degree(self, size):
		self.out_degree = self.out_degree - size