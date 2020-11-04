from stack import Stack 
from node_tree import NodeTree
import math

#Return weights and profits sorteds, with division of profits per weights and initial Node
def init_solution(capacity, weights, profits):
	profit_per_weight = [(element[0][0], element[0][1] / element[1]) for element in zip(enumerate(profits), weights)]

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

#Return best solution given configurations
def bound(node, weights, profits, profit_per_weight):
	node_id = node.id
	node_capacity = node.capacity
	node_objective = node.objective

	#while node_id < (len(profits) - 1) and node_capacity >= weights[node_id + 1]:
	if node_id < (len(profits) - 1) and node_capacity >= weights[node_id + 1]: 
		node_objective+= int(node_capacity / weights[node_id + 1]) * profits[node_id + 1]
		node_capacity-= int(node_capacity / weights[node_id + 1]) * weights[node_id + 1]
		node_id+= 1

	if node_id < (len(profits) - 1) and node_capacity > 0:
		node_objective+= min(node_capacity, weights[node_id + 1]) * profit_per_weight[node_id + 1][1]

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
		if Node.capacity >= 0:
			Node.relaxation = bound(Node, weights, profits, profit_per_weight)
			stack.add_stack(Node)

			if Node.objective == Node.relaxation:
				if solution and Node.objective > solution.objective: solution = Node
				elif solution is None: solution = Node

		Node = NodeTree(root.id + 1)
		Node.capacity = root.capacity - int(root.capacity / weights[Node.id]) * weights[Node.id]

		if Node.capacity >= 0:
			Node.objective = root.objective + int(root.capacity / weights[Node.id]) * profits[Node.id]
			Node.variables = list(root.variables)
			Node.variables[Node.id] = int(root.capacity / weights[Node.id])
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
def knapsack_with_file(filepath):
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

capacity, weights, profits = knapsack_with_file("C:/Users/natandemorais/Desktop/knapsack/data/knapPI_1_2000_1000_1")
print(branch_and_bound_knapsack(capacity, weights, profits))

#capacity, weights, profits = knapsack_with_file("C:/Users/natandemorais/Downloads/instances KP/large_scale/natan.txt")
#print(branch_and_bound_knapsack(capacity, weights, profits))

capacity = [52,52,104]
profits =  [60, 3456, 880, 1950, 924, 143, 4000, 5000, 1890, 247, 697, 1176, 2880, 3440, 1530, 2325, 1296, 3948, 324, 1000]
weights =  [[30, 48, 36, 50, 22, 11, 38, 38, 3, 19, 41, 21, 20, 40, 34, 31, 4, 47, 27, 50],
			  [1, 36, 40, 39, 14, 13, 21, 4, 3, 13, 17, 28, 48, 43, 15, 25, 27, 28, 12, 20],
			  [19, 35, 41, 39, 50, 49, 46, 2, 21, 6, 31, 45, 4, 39, 14, 39, 25, 47, 40, 19]]
result = branch_and_bound_knapsack(capacity[0], weights[0], profits)
print(result[0], result[1])

result = branch_and_bound_knapsack(capacity[1], weights[1], profits)
print(result[0], result[1])

result = branch_and_bound_knapsack(capacity[2], weights[2], profits)
print(result[0], result[1])