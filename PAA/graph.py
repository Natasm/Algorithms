from node import Node

class Graph(object):
	def __init__(self):
		self.nodes = {}
		self.count = 0

	def build_graph(self, tuples):
		for t in tuples:
			self.add_node(t[0], t[1:])

	def add_node(self, content, neighbors):
		node_id_ref = self.exist_node(content)
		
		new_node = None
		new_id = self.count
		self.count = self.count + 1

		if node_id_ref != None: new_node = self.nodes[node_id_ref]
		else: new_node = Node(content)

		for x in neighbors:
			node_id = self.exist_node(x)
			
			if node_id != None: 
				new_node.add_neighbor(node_id)
				self.nodes[node_id].add_incident(new_id)
			elif x != content:
				new = Node(x) 
				self.nodes.update({ self.count : new })
				new_node.add_neighbor(self.count)
				self.nodes[self.count].add_incident(new_id)
				self.count = self.count + 1
		
		if node_id_ref == None: 
			self.nodes.update({ new_id : new_node })

	def exist_node(self, content):
		for node_id in self.nodes:
			ref_node = self.nodes[node_id] 
			if ref_node.get_content() == content: return node_id
		
		return None

	def get_nodes(self):
		return self.nodes

