from topologic_sort import topologic_sort
from graph import Graph
from decimal import Decimal

def minimum_path(G, s):
	dist = {}
	d = {}

	for v in G.get_nodes(): 
		dist.update({ G.get_nodes()[v].get_content() : Decimal('Infinity') })
		d.update({ G.get_nodes()[v].get_content() : None })

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
				d[G.get_nodes()[vertice].get_content()] = topologic_sorted[i] 

	for solution in d:
		if d[solution] != None : print('Vértice ', d[solution], ' tem aresta para ', solution)


	return dist

graph_base = Graph()

vertices = [0, 1 , 2, 3, 4, 5, 6]

tuples = { (0,2,0.3), (0,5,0.6), (0,1,0.1),
           (3,2,3.3), (3,5, 3.7), (3,4,3.2),
           (3,6,3.5), (5,2,4.2), (1,4,1.4),
           (6,0,0.6), (6,4,4.6)}

#vertices = ['r', 's', 't', 'x', 'y', 'z']

#tuples = { ('r','s', 5), ('r','t',3),
#           ('s','x',6), ('s','t',2),
#           ('t','x',7), ('t','y',4), ('t','z', 2),
#           ('x','y',-1), ('x','z',1),
#           ('y','z',-2),}

#vertices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

#tuples = {(0, 1, 10), (0, 2, 14), (0, 3, 6), (0, 5, 28), (0, 6, 30), (0, 7, 9), (0, 8, 29), (0, 9, 9), (0, 10, 26), (0, 14, 24), (1, 2, 27), (1, 3, 8), (1, 4, 27), (1, 6, 26), (1, 7, 13), (1, 8, 3), (1, 12, 9), (1, 13, 29), (2, 3, 20), (2, 4, 23), (2, 5, 15), (2, 7, 29), (2, 8, 14), (2, 9, 8), (2, 10, 10), (2, 11, 15), (2, 13, 21), (2, 14, 18), (3, 5, 15), (3, 6, 4), (3, 8, 5), (3, 9, 15), (3, 10, 20), (3, 11, 18), (3, 13, 13), (3, 14, 12), (4, 5, 6), (4, 6, 25), (4, 8, 9), (4, 9, 28), (4, 10, 28), (4, 11, 1), (4, 12, 18), (4, 13, 15), (4, 14, 16), (5, 6, 11), (5, 8, 24), (5, 9, 8), (5, 10, 5), (5, 11, 11), (5, 12, 30), (5, 13, 8), (6, 7, 25), (6, 10, 19), (6, 11, 18), (6, 12, 20), (6, 13, 19), (7, 8, 23), (7, 10, 17), (7, 11, 30), (7, 12, 13), (7, 14, 25), (8, 9, 28), (8, 10, 1), (9, 10, 28), (9, 11, 11), (9, 12, 10), (9, 13, 15), (9, 14, 20), (10, 12, 10), (10, 14, 16), (11, 14, 6), (12, 13, 10), (12, 14, 1), (13, 14, 12)}

graph_base.build_graph(vertices, tuples)

print(minimum_path(graph_base, 6))



