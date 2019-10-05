class Printer:
	def __init__(self, extruders, price, has_misp):
		self.extruders = extruders
		self.price = price
		self.has_misp = has_misp

	@property
	def extruders(self):
		print("Get extruders")
		return self._extruders

	@extruders.setter
	def extruders(self, value):
		if not isinstance(value, int):
			raise Exception("No integer!")
		if value < 1:
			raise Exception("Need at least one extruder!")
		print("Set extruders")
		self._extruders = value

	@property
	def price(self):
		print("Get price")
		return self._price

	@price.setter
	def price(self, value):
		if not isinstance(value, int):
			raise Exception("No integer!")
		if value < 2000:
			raise Exception("Too cheap!")
		print("Set price")
		self._price = value

	@property
	def has_misp(self):
		print("Get has_misp")
		return self._has_misp

	@has_misp.setter
	def has_misp(self, value):
		if not isinstance(value, bool):
			raise Exception("Must be boolean!")
		print("Set has_misp")
		self._has_misp = value