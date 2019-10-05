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
			raise Exception("No integer!")
		super().__set__(instance, value)

class AtLeast(Descriptor):
	def __init__(self, name, minimum):
		self.minimum = minimum
		super().__init__(name)

	def __set__(self, instance, value):
		if value < self.minimum:
			raise Exception("Too cheap!")
		super().__set__(instance, value)

class MinimumInt(Integer, AtLeast):  # Using descriptors as mixins here.
	pass

class Printer:
	price = MinimumInt("price", 2000)

	def __init__(self, extruders, price, has_misp):
		self.extruders = extruders
		self.price = price
		self.has_misp = has_misp

class Material:
	def __init__(self, color, density):
		self.color = color
		self.density = density