from node import Node

class Graph(object):
	def __init__(self):
		self.nodes = {}
		self.count = 0

	def build_graph(self, vertices, tuples):
		for v in vertices:
			self.nodes.update({ self.count : Node(v) })
			self.count = self.count + 1

		for t in tuples:
			if len(t) == 2 : self.add_node(t[0], [t[1]], [0])
			elif len(t) == 3: self.add_node(t[0], [t[1]], [t[2]])

	def add_node(self, content, neighbors, costs):
		node_id_ref = self.exist_node(content)
		
		new_node = None
		new_id = self.count
		self.count = self.count + 1

		if node_id_ref != None: new_node = self.nodes[node_id_ref]
		else: new_node = Node(content)

		for x in range(0, len(neighbors)):
			node_id = self.exist_node(neighbors[x])
			
			if node_id != None: 
				new_node.add_neighbor(node_id, costs[x])
				self.nodes[node_id].add_incident(new_id)
		
		if node_id_ref == None: 
			self.nodes.update({ new_id : new_node })

	def delete_node(self, key):
		del self.nodes[key]

	def exist_node(self, content):
		for node_id in self.nodes:
			ref_node = self.nodes[node_id] 
			if ref_node.get_content() == content: return node_id
		
		return None

	def get_nodes(self):
		return self.nodes

