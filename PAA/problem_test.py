class Problem(object):

	def resolve(self, var_index=None, inequality=None, value=None):
		p = MixedIntegerLinearProgram()
		x = p.new_variable(real=True, nonnegative=True)

		p.set_objective(17*x[0] + 12*x[1])

		p.add_constraint(10*x[0] + 7*x[1] <= 40)

		p.add_constraint(x[0] + x[1] <= 5)

		p.add_constraint(x[0] >= 0)

		p.add_constraint(x[1] >= 0)

		if inequality == '<=': p.add_constraint(x[var_index] <= value)
		elif inequality == '>=': p.add_constraint(x[var_index] >= value)
		
		try:
			value_solution = round(p.solve(), 2)
			solution = p.get_values(x)

			variables = []
			for i in solution: variables.append(round(solution[i], 2))
    
			return[value_solution, variables]
		
		except:
		 	print("Solver failed: :(")
		 	return None
