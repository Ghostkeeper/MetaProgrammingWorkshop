class Descriptor:
	def __init__(self, name):
		self.name = name
		code = "def __set__(self, instance, value):\n\t"
		for cls in self.__class__.__mro__:
			if "set_code" in cls.__dict__:
				code += "\n\t".join(cls.set_code()) + "\n\t"
		locals = {}
		exec(code, globals(), locals)
		setattr(self.__class__, "__set__", locals["__set__"])

	def __get__(self, instance, cls):
		#print("Get", self.name)
		return instance.__dict__[self.name]

	@staticmethod
	def set_code():
		return ["instance.__dict__[self.name] = value"]

class Integer(Descriptor):
	@staticmethod
	def set_code():
		return ['if not isinstance(value, int):',
				'\traise Exception("No int!")']

class AtLeast(Descriptor):
	def __init__(self, name, minimum):
		self.minimum = minimum
		super().__init__(name)

	@staticmethod
	def set_code():
		return ['if value < self.minimum:',
				'\traise Exception("Not enough!")']

class MinimumInt(Integer, AtLeast):  # Using descriptors as mixins here.
	pass

class Bool(Descriptor):
	@staticmethod
	def set_code():
		return ['if not isinstance(value, bool):',
				'\traise Exception("Not boolean!")']

class Printer:
	extruders = MinimumInt("extruders", 1)
	price = MinimumInt("price", 2000)
	has_misp = Bool("has_misp")

	def __init__(self, extruders, price, has_misp):
		self.extruders = extruders
		self.price = price
		self.has_misp = has_misp