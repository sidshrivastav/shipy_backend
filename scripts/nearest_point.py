
def sort_nearest_point(input) :
	result = sorted(input, key=lambda x: float(x[0]) / x[1])
	return result;
