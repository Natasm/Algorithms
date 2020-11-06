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
		else: 
			return None

	def get_size(self):
		return len(self.date)

	def get_values(self):
		return self.date