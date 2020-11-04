from stack import Stack 
from node_tree import NodeTree
import numpy as np

#Return weights and profits sorteds, with division of profits per weights and initial Node
def init_solution(capacity, weights, profits):

	weights_buffer = [0] * len(profits)
	for i in range(0, len(profits)):
		weights_buffer[i] = (weights[0][i] + weights[1][i] + weights[2][i])

	profit_per_weight = [] 
	for j in range(len(profits)):
		profit_per_weight.append((j, profits[j] / weights_buffer[j]))		
	
	profit_per_weight.sort(key=lambda element:element[1], reverse=True)

	print(profit_per_weight)

	weights_buffer = np.zeros((3, len(profits)), dtype=float)
	for i in range(len(profit_per_weight)):
		weights_buffer[0][i] = weights[0][profit_per_weight[i][0]]
		weights_buffer[1][i] = weights[1][profit_per_weight[i][0]]
		weights_buffer[2][i] = weights[2][profit_per_weight[i][0]]
	
	profits_buffer = [profits[element[0]] for element in profit_per_weight]
	
	Node = NodeTree()
	Node.id = -1
	Node.capacity = capacity
	Node.objective = 0
	Node.variables = [0] * len(profits)
	Node.relaxation = bound(Node, weights_buffer, profits_buffer, profit_per_weight)

	return (weights_buffer, profits_buffer, profit_per_weight, Node)

#Exist space? >= 0?
def exist_space(node_id, node_capacity, weights):
	if node_capacity[0] >= weights[0][node_id] and node_capacity[1] >= weights[1][node_id] and node_capacity[2] >= weights[2][node_id]:
		return True
	else: 
		return False

#Capacity is > 0?
def valid_space(node_capacity):
	if node_capacity[0] > 0 and node_capacity[1] > 0 and node_capacity[2] > 0: 
		return True
	else: 
		return False

#Return best solution given configurations
def bound(node, weights, profits, profit_per_weight):
	node_id = node.id
	node_objective = node.objective

	node_capacity = []
	for element in node.capacity: node_capacity.append(element)

	current_node = node_id
	
	while node_id < (len(profits) - 1):
		if exist_space(node_id + 1, node_capacity, weights):
			node_objective += profits[node_id + 1]
			node_capacity[0] -= weights[0][node_id + 1]
			node_capacity[1] -= weights[1][node_id + 1]
			node_capacity[2] -= weights[2][node_id + 1]

			current_node = node_id + 1
		else:
			node_id += 1

	current_node += 1

	if current_node < (len(profits) - 1) and valid_space(node_capacity):
		print(current_node)
		node_objective+= max(node_capacity[0], node_capacity[1], node_capacity[2], weights[0][current_node], weights[1][current_node], weights[2][current_node]) * profit_per_weight[current_node][1]

	return node_objective

#Branch and bound
def branch_and_bound_knapsack(capacity, weights, profits):
	stack = Stack()

	weights, profits, profit_per_weight, root = init_solution(capacity, weights, profits)

	print(root.relaxation)

	stack.add_stack(root)

	solution = None

	while not stack.isEmpty():
		root = stack.pop_stack()

		if solution and root.relaxation < solution.relaxation: continue
		elif root.id == (len(profits) - 1): continue

		Node = NodeTree(root.id + 1, root.capacity, root.objective, root.variables)
		if valid_space(Node.capacity):
			Node.relaxation = bound(Node, weights, profits, profit_per_weight)
			stack.add_stack(Node)
			print('Tira ', Node.relaxation)

			if Node.objective == Node.relaxation:
				if solution and Node.objective > solution.objective: solution = Node
				elif solution is None: solution = Node

		Node = NodeTree(root.id + 1, root.capacity)
		node_id = Node.id
		node_capacity = list(Node.capacity)
		min_get_itens = 1
		Node.capacity[0] -= min_get_itens * weights[0][Node.id]
		Node.capacity[1] -= min_get_itens * weights[1][Node.id]
		Node.capacity[2] -= min_get_itens * weights[2][Node.id]

		if valid_space(Node.capacity) and min_get_itens > 0:
			print('min_get_itens: ', min_get_itens)
			print('capacits dentro: ', Node.capacity)
			Node.objective = root.objective + min_get_itens * profits[Node.id]
			Node.variables = list(root.variables)
			Node.variables[Node.id] = min_get_itens
			Node.relaxation = bound(Node, weights, profits, profit_per_weight)
			stack.add_stack(Node)
			print('Bota ', Node.relaxation)

			if Node.objective == Node.relaxation:
				if solution and Node.objective > solution.objective: solution = Node
				elif solution is None: solution = Node

	if solution != None:
		variables = [0] * len(profits)
		for index, element in enumerate(profit_per_weight):
			variables[element[0]] = solution.variables[index]

	if solution != None: return [solution.objective, variables]

#Knapsack with read file
def knapsack_with_file(filepath, dimension):
	file = open(filepath, 'r')
    
	n = 0
	W = [0] * dimension

	for line in file:
		line_first = line.replace("\n", "").split(' ')
		n = int(line_first[0])
		break

	for line in file:
		line_first = line.replace("\n", "").split(' ')
		W[0] = float(line_first[0])
		W[1] = float(line_first[1])
		W[2] = float(line_first[2])
		break

	k = np.zeros((dimension, n), dtype=float)
	v = []
    
	i = 0
	for line in file:
		if i == n: break
		line_subseq = line.replace("\n", "").split(' ')
		v.append(float(line_subseq[0]))
		k[0][i] = (float(line_subseq[1]))
		k[1][i] = (float(line_subseq[2]))
		k[2][i] = (float(line_subseq[3]))
		i = i + 1

	return (W, k, v)


#capacity, weights, profits = knapsack_with_file("C:/Users/natandemorais/Desktop/knapsack/data/knapPI_1_2000_1000_1")
#capacity, weights, profits = knapsack_with_file('C:/Users/natandemorais/Desktop/key/media3', 3)
capacity = [52,52,104]
profits =  [60, 3456, 880, 1950, 924, 143, 4000, 5000, 1890, 247, 697, 1176, 2880, 3440, 1530, 2325, 1296, 3948, 324, 1000]
weights =  [[30, 48, 36, 50, 22, 11, 38, 38, 3, 19, 41, 21, 20, 40, 34, 31, 4, 47, 27, 50],
			  [1, 36, 40, 39, 14, 13, 21, 4, 3, 13, 17, 28, 48, 43, 15, 25, 27, 28, 12, 20],
			  [19, 35, 41, 39, 50, 49, 46, 2, 21, 6, 31, 45, 4, 39, 14, 39, 25, 47, 40, 19]]

#capacity, weights, profits = knapsack_with_file('C:/Users/natandemorais/Desktop/key/media3', 3)

print(branch_and_bound_knapsack(capacity, weights, profits))
#print(result)

#Knapsack with read file
def knapsack_with_file_s(filepath):
	file = open(filepath, 'r')
    
	n = 0
	W = 0
	k = []
	v = []

	for line in file:
		line_first = line.replace("\n", "").split(' ')
		W = int(line_first[1])
		n = int(line_first[0])
		break
    
	i = 0
	for line in file:
		if i == n: break
		line_subseq = line.replace("\n", "").split(' ')
		v.append(int(line_subseq[0]))
		k.append(int(line_subseq[1]))
		i = i + 1

	return (W, k, v)

#targetSum, weightArray, valueArray = knapsack_with_file_s("C:/Users/natandemorais/Desktop/knapsack/data/knapPI_1_2000_1000_1")
