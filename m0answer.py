def debugme(func):
	print("Wrapping a function!")
	def wrapper(*args, **kwargs):
		print(func.__qualname__)
		return func(*args, **kwargs)
	return wrapper

def add(a, b):
	return a + b

def mul(a, b):
	return a * b

def sub(a, b):
	return a - b