from m2answer import *

class PrinterBasic:
	def __init__(self, extruders, price, has_misp):
		self.extruders = extruders
		self.price = price
		self.has_misp = has_misp

import time
repeats = 1_000_000

print("SIMPLE STRUCTURE")
t = 0
for _ in range(repeats):
	t0 = time.time()
	PrinterBasic(2, 4000, True)
	t1 = time.time()
	t += t1 - t0
print("Constructor:", round(t, 2))

t = 0
p = PrinterBasic(2, 4000, True)
for _ in range(repeats):
	t0 = time.time()
	x = p.price
	t1 = time.time()
	t += t1 - t0
print("Get:", round(t, 2))

t = 0
for _ in range(repeats):
	t0 = time.time()
	p.price = 3333
	t1 = time.time()
	t += t1 - t0
print("Set:", round(t, 2))

print("\nDESCRIPTORS")
t = 0
for _ in range(repeats):
	t0 = time.time()
	Printer(2, 4000, True)
	t1 = time.time()
	t += t1 - t0
print("Constructor:", round(t, 2))

t = 0
p = Printer(2, 4000, True)
for _ in range(repeats):
	t0 = time.time()
	x = p.price
	t1 = time.time()
	t += t1 - t0
print("Get:", round(t, 2))

t = 0
for _ in range(repeats):
	t0 = time.time()
	p.price = 3333
	t1 = time.time()
	t += t1 - t0
print("Set:", round(t, 2))