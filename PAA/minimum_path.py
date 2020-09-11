from topologic_sort import topologic_sort
from graph import Graph
from decimal import Decimal

def minimum_path(G, s):
	dist = {}

	for v in G.get_nodes(): 
		dist.update({ G.get_nodes()[v].get_content() : Decimal('Infinity') })

	dist[s] = 0

	topologic_sorted = topologic_sort(G)
	topologic_sorted_size = len(topologic_sorted)
	print('Topologic sorted: ', topologic_sorted)

	begin = -1
	for x in range(0, topologic_sorted_size):
		if topologic_sorted[x] == s: begin = x

	if begin == -1: return 'Origin vertice not found'	

	for i in range(begin, topologic_sorted_size):
		exist_node = G.exist_node(topologic_sorted[i])
		if exist_node == None: continue

		vertices_adj = G.get_nodes()[exist_node].get_neighbors()

		for vertice in vertices_adj:
			if (dist[topologic_sorted[i]] + vertices_adj[vertice]) < dist[G.get_nodes()[vertice].get_content()]:
				dist[G.get_nodes()[vertice].get_content()] = dist[topologic_sorted[i]] + vertices_adj[vertice]

	return dist

graph_base = Graph()

vertices = ['r', 's', 't', 'x', 'y', 'z']

tuples = { ('r','s', 5), ('r','t',3),
           ('s','x',6), ('s','t',2),
           ('t','x',7), ('t','y',4), ('t','z', 2),
           ('x','y',-1), ('x','z',1),
           ('y','z',-2),}

graph_base.build_graph(vertices, tuples)

print(minimum_path(graph_base, 's'))



