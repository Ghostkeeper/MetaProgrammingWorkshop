class Printer:
	def __init__(self, extruders, price, has_misp):
		self.extruders = extruders
		self.price = price
		self.has_misp = has_misp

class Material:
	def __init__(self, color, density):
		self.color = color
		self.density = density