from stack import Stack 
from graph import Graph

def topologic_sort(G):
	if G is None: return []

	S = Stack()
	for vertice in G.get_nodes():
		if G.get_nodes()[vertice].get_in_degree() == 0: S.add_stack(vertice)
	
	t = 0
	s = []
	while(S.isEmpty() != True):
		v = S.pop_stack()
		
		G.get_nodes()[v].insert_sort(t)
		t = t + 1
		
		s.append(G.get_nodes()[v].get_content())
		for neighbor in G.get_nodes()[v].get_neighbors():
			G.get_nodes()[neighbor].pop_in_degree(1)
			if G.get_nodes()[neighbor].get_in_degree() == 0: S.add_stack(neighbor)

	return s
	

#graph_base = Graph()

#vertices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

#tuples = {(0, 1), (0, 2), (0, 4), (0, 5), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 14), (1, 2), (1, 3), (1, 5), (1, 7), (1, 8), (1, 9), (1, 10), (1, 13), (1, 14), (2, 3), (2, 4), (2, 5), (2, 7), (2, 11), (2, 13), (3, 4), (3, 5), (3, 6), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 14), (4, 5), (4, 7), (4, 8), (4, 10), (4, 11), (4, 12), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (6, 7), (6, 8), (6, 9), (6, 12), (6, 14), (7, 8), (7, 10), (8, 9), (8, 11), (8, 12), (8, 13), (9, 10), (10, 11), (10, 13), (11, 13), (11, 14), (13, 14) }

#graph_base.build_graph(vertices, tuples)

#print(topologic_sort(graph_base))
