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
	

graph_base = Graph()

vertices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

tuples = { (0, 4), (0, 5), (0, 8), (0, 9), (0, 10), (0, 11), (0, 13), (0, 14), (1, 0), (1, 2), (1, 3), (1, 6), (1, 7), (1, 9), (1, 10), (1, 14), (2, 1), (2, 3), (2, 4), (2, 9), (2, 11), (2, 12), (3, 9), (3, 12), (4, 2), (4, 8), (4, 9), (4, 10), (4, 12), (4, 14), (5, 0), (5, 1), (5, 6), (5, 7), (5, 10), (5, 11), (5, 12), (6, 0), (6, 2), (6, 4), (6, 5), (6, 7), (6, 11), (6, 12), (6, 13), (6, 14), (7, 0), (7, 4), (7, 8), (7, 11), (7, 12), (8, 1), (8, 6), (8, 7), (8, 9), (8, 10), (8, 12), (8, 13), (9, 2), (9, 3), (9, 6), (9, 7), (9, 8), (9, 10), (9, 12), (10, 1), (10, 2), (10, 5), (10, 6), (10, 14), (11, 0), (11, 2), (11, 3), (11, 5), (11, 6), (11, 7), (11, 10), (11, 12), (11, 14), (12, 0), (12, 1), (12, 3), (12, 5), (12, 6), (12, 9), (12, 10), (12, 11), (12, 13), (12, 14), (13, 0), (13, 2), (13, 4), (13, 6), (13, 8), (13, 9), (14, 1), (14, 4), (14, 5), (14, 6)}

graph_base.build_graph(vertices, tuples)

print(topologic_sort(graph_base))
