def knapsack_fractionary(W, k, v):

	p = MixedIntegerLinearProgram()
	x = p.new_variable(real=True, nonnegative=True)
	
	p.set_objective(p.sum(x[i]*v[i] for i in range(len(v))))

	p.add_constraint(p.sum(x[i]*k[i] for i in range(len(v))) <= W)

	for i in range(len(v)):
		p.add_constraint(x[i] <= 1)

	for i in range(len(v)):
		p.add_constraint(x[i] >= 0)

	print(round(p.solve(), 2))

def knapsack_no_repeat(W, k, v):

	p = MixedIntegerLinearProgram(maximization=True)
	x = p.new_variable(real=False, nonnegative=True)
	
	p.set_objective(p.sum(x[i]*v[i] for i in range(len(v))))

	p.add_constraint(p.sum(x[i]*k[i] for i in range(len(k))) <= W)

	p.set_binary(x)

	print(round(p.solve(), 2))

def knapsack_with_repeat(W, k, v):

	p = MixedIntegerLinearProgram(maximization=True)
	x = p.new_variable(integer=True, nonnegative=True)
	
	p.set_objective(p.sum(x[i]*v[i] for i in range(len(v))))

	p.add_constraint(p.sum(x[i]*k[i] for i in range(len(k))) <= W)

	print(round(p.solve(), 2))
	print(p.get_values(x))

def knapsack_with_file(filepath):
	file = open(filepath, 'r')
    
	W = 0
	k = []
	v = []

	for line in file:
		line_first = line.replace("\n", "").split(' ')
		W = int(line_first[1])
		break
    
	for line in file:
		line_subseq = line.replace("\n", "").split(' ')
		k.append(int(line_subseq[0]))
		v.append(int(line_subseq[1]))

	print(W)
	print(k)
	print(v)

	knapsack_with_repeat(W, k, v)

knapsack_with_file("C:/Users/natandemorais/Downloads/instances KP/large_scale/natan.txt")


#Ver o tempo de execução => time a = knapsack_no_repeat(W,k,v)

#generalizacao do exemplo, recebe como entrada um conjunto de preços, 
#limite de produção de cada um e limite diario total
def exemplo2(v,l,d):

	p = MixedIntegerLinearProgram()
	x = p.new_variable(real=True, nonnegative=True)
	

	p.set_objective(p.sum(x[i]*v[i] for i in range(len(v))))


	for i in range(len(v)):
		p.add_constraint(x[i] <= l[i])
	

	p.add_constraint(p.sum(x[i] for i in range(len(v))) <= d)

	print(round(p.solve(), 2))




#exemplo da loja de chocolate, dois tipos de chocolates que geram lucro de R$ 1 e R$2, 
#além dos respectivos limites de produção de 200 e 300, 
#e o limite total de produção de 400
def chocolate():

	p = MixedIntegerLinearProgram()
	x = p.new_variable(real=True, nonnegative=True)
	

	p.set_objective(x[1] + 6*x[2])

	p.add_constraint(x[1] <= 200)
	p.add_constraint(x[2] <= 300)
	p.add_constraint(x[1] + x[2] <= 400)

	print(round(p.solve(), 2))