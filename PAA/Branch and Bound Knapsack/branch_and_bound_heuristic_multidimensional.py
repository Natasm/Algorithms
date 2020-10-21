from stack import Stack 
from node_tree import NodeTree
import numpy as np

#Return weights and profits sorteds, with division of profits per weights and initial Node
def init_solution(capacity, weights, profits):
	profit_per_weight = [(element[0][0], element[0][1] / (element[1][0] + element[1][1] + element[1][2])) for element in zip(enumerate(profits), weights)]

	profit_per_weight.sort(key=lambda element:element[1], reverse=True)

	weights = [weights[element[0]] for element in profit_per_weight]
	profits = [profits[element[0]] for element in profit_per_weight]

	Node = NodeTree()
	Node.id = -1
	Node.capacity = capacity
	Node.objective = 0
	Node.variables = [0] * len(profits)
	Node.relaxation = bound(Node, weights, profits, profit_per_weight)

	return (weights, profits, profit_per_weight, Node)

#Exist space? >= 0?
def exist_space(node_id, node_capacity,weights):
	if node_capacity[0] >= weights[node_id + 1][0] and node_capacity[1] >= weights[node_id + 1][1] and node_capacity[2] >= weights[node_id + 1][2]:
			return True
	else: return False

#Capacity is > 0?
def valid_space(node_capacity):
	if node_capacity[0] > 0 and node_capacity[1] > 0 and node_capacity[2] > 0: return True
	else: return False

#Return best solution given configurations
def bound(node, weights, profits, profit_per_weight):
	node_id = node.id
	node_capacity = []
	for element in node.capacity: node_capacity.append(element)
	node_objective = node.objective

	while node_id < (len(profits) - 1) and exist_space(node_id, node_capacity, weights):
		node_objective+= profits[node_id + 1]
		node_capacity[0]-= weights[node_id + 1][0]
		node_capacity[1]-= weights[node_id + 1][1]
		node_capacity[2]-= weights[node_id + 1][2]
		node_id+= 1

	if node_id < (len(profits) - 1) and valid_space(node_capacity):
		node_objective+= min(node_capacity[0] + node_capacity[1] + node_capacity[2], weights[node_id + 1][0] + weights[node_id + 1][1] + weights[node_id + 1][2]) * profit_per_weight[node_id + 1][1]

	return node_objective

#Branch and bound
def branch_and_bound_knapsack(capacity, weights, profits):
	stack = Stack()

	weights, profits, profit_per_weight, root = init_solution(capacity, weights, profits)

	stack.add_stack(root)

	solution = None

	while not stack.isEmpty():
		root = stack.pop_stack()

		if solution and root.relaxation < solution.relaxation: continue
		elif root.id == (len(profits) - 1): continue

		Node = NodeTree(root.id + 1, root.capacity, root.objective, root.variables)
		if Node.capacity[0] >= 0 and Node.capacity[1] >= 0 and Node.capacity[2] >= 0:
			Node.relaxation = bound(Node, weights, profits, profit_per_weight)
			stack.add_stack(Node)

			if Node.objective == Node.relaxation:
				if solution and Node.objective > solution.objective: solution = Node
				elif solution is None: solution = Node

		Node = NodeTree(root.id + 1)
		new_capacity = []
		new_capacity.append(root.capacity[0] - weights[Node.id][0])
		new_capacity.append(root.capacity[1] - weights[Node.id][1])
		new_capacity.append(root.capacity[2] - weights[Node.id][2])
		Node.capacity = new_capacity

		if Node.capacity[0] >= 0 and Node.capacity[1] >= 0 and Node.capacity[2] >= 0:
			Node.objective = root.objective + profits[Node.id]
			Node.variables = list(root.variables)
			Node.variables[Node.id] = 1
			Node.relaxation = bound(Node, weights, profits, profit_per_weight)
			stack.add_stack(Node)

			if Node.objective == Node.relaxation:
				if solution and Node.objective > solution.objective: solution = Node
				elif solution is None: solution = Node

	variables = [0] * len(profits)
	for index, element in enumerate(profit_per_weight):
		variables[element[0]] = solution.variables[index]

	return [solution.objective, variables]

#Knapsack with read file
def knapsack_with_file(filepath, dimension):
	file = open(filepath, 'r')
    
	n = 0
	W = [0] * dimension

	for line in file:
		line_first = line.replace("\n", "").split(' ')
		n = int(line_first[0])
		W[0] = int(line_first[1])
		W[1] = int(line_first[2])
		W[2] = int(line_first[3])
		break

	k = np.zeros((n, dimension), dtype=float)
	v = []
    
	i = 0
	for line in file:
		if i == n: break
		line_subseq = line.replace("\n", "").split(' ')
		k[i][0] = (int(line_subseq[0]))
		k[i][1] = (int(line_subseq[1]))
		k[i][2] = (int(line_subseq[2]))
		v.append(int(line_subseq[3]))
		i = i + 1

	return (W, k, v)

capacity, weights, profits = knapsack_with_file("C:/Users/natandemorais/Downloads/instances KP/large_scale/natan.txt", 3)
print(branch_and_bound_knapsack(capacity, weights, profits))

