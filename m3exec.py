class Descriptor:
	def __init__(self, name):
		self.name = name

	def __get__(self, instance, cls):
		print("Get", self.name)
		return instance.__dict__[self.name]

	def __set__(self, instance, value):
		print("Set", self.name)
		instance.__dict__[self.name] = value

class Integer(Descriptor):
	def __set__(self, instance, value):
		if not isinstance(value, int):
			raise Exception("No int!")
		super().__set__(instance, value)

class AtLeast(Descriptor):
	def __init__(self, name, minimum):
		self.minimum = minimum
		super().__init__(name)

	def __set__(self, instance, value):
		if value < self.minimum:
			raise Exception("Not enough!")
		super().__set__(instance, value)

class MinimumInt(Integer, AtLeast):  # Using descriptors as mixins here.
	pass

class Bool(Descriptor):
	def __set__(self, instance, value):
		if not isinstance(value, bool):
			raise Exception("Not boolean!")
		super().__set__(instance, value)

class Printer:
	extruders = MinimumInt("extruders", 1)
	price = MinimumInt("price", 2000)
	has_misp = Bool("has_misp")

	def __init__(self, extruders, price, has_misp):
		self.extruders = extruders
		self.price = price
		self.has_misp = has_misp