import math

#Return true if exist some fractionary element in array
def existFractionary(array):
	for element in array:
		f, i = math.modf(element)
		if f != 0: return True
	return False

#Return true if a array is equal a other array
def isEqual(arrX, arrY):
	if len(arrX) != len(arrY): return False
	for i in range(len(arrX)):
		if arrX[i] != arrY[i]: return False
	return True

#Verify if problem ready solved
def isReadySolved(array, search):
	for element in array:
		#sol, var = element
		#sol_, var_ = search
		#if (sol == sol_) and isEqual(var, var_): return True
		if element == search: return True
	return False