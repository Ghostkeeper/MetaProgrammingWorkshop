from m0answer import debugme
def debugall(cls):
	for key, val in vars(cls).items():
		if callable(val):
			setattr(cls, key, debugme(val))
	return cls

@debugall
class Maths:
	def add(self, a, b):
		return a + b

	def mul(self, a, b):
		return a * b

	def sub(self, a, b):
		return a - b