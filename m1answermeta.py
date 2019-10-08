from m0answer import debugme
class DebugMeta(type):
	def __new__(cls, name, bases, clsdict):
		for key, val in clsdict.items():
			if callable(val):
				clsdict[key] = debugme(val)
		return super().__new__(cls, name, bases, clsdict)

class Maths(metaclass=DebugMeta):
	def add(self, a, b):
		return a + b

	def mul(self, a, b):
		return a * b

	def sub(self, a, b):
		return a - b