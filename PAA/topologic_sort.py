from stack import Stack 
from graph import Graph

def topologic_sort(G):
	S = Stack()
	for vertice in G:
		if G[vertice].get_in_degree() == 0: S.add_stack(vertice)
	
	t = 0
	s = []
	while(S.isEmpty() != True):
		v = S.pop_stack()
		
		G[v].insert_sort(t)
		t = t + 1
		
		s.append(G[v].get_content())
		for neighbor in G[v].get_neighbors():
			G[neighbor].pop_in_degree(1)
			if G[neighbor].get_in_degree() == 0: S.add_stack(neighbor)

	return s
	

graph_base = Graph()

tuples = { ('b', 'c', 'd', 'a'), ('c', 'e'), ('d', 'e'), ('a', 'f'), ('f', 'g'), ('e', 'g') }

graph_base.build_graph(tuples)

print(topologic_sort(graph_base.get_nodes()))
