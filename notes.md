Intro
----
1. Metaprogramming is writing code that creates code.
2. Why metaprogramming: Automating boring task, removing duplicate code.
3. Why not metaprogramming: Hidden magic, complex code, hard to debug.

Function Decorators
----
1. Show m0debugging.py.
2. Use case: Write print statements on all 3 functions. Repetitive!
3. Write decorator at the top of m0debugging.py:
	```
	def debugme(func):
		print("Wrapping a function!")
		def wrapper(*args, **kwargs):
			print(func.__qualname__)
			return func(*args, **kwargs)
		return wrapper
	```
4. Modify code: Instead of prints, use @debugme.
5. Demonstrate effect with `python3`:
	```
	>>> from m0debugging import *
	Wrapping a function!
	Wrapping a function!
	Wrapping a function!
	>>> add(3, 4)
	add
	7
	>>> sub(3, 4)
	sub
	-1
	```
6. You could replace the prints with logging or profiling later, just in one place.

Class Decorators
----
1. All those @debugme are still repetitive. Want to debug an entire class?
2. Show m1classdec.py
3. Write decorator at the top of m1classdec.py
	```
	from m0answer import debugme
	def debugall(cls):
		for key, val in vars(cls).items():
			if callable(val):
				setattr(cls, key, debugme(val))
		return cls
	```
4. Demonstrate the result with `python3`:
	```
	>>> from m1classdec import *
	Wrapping a function!
	Wrapping a function!
	Wrapping a function!
	>>> m = Maths()
	>>> m.add(3, 4)
	Maths.add
	7
	>>> m.mul(3, 4)
	Maths.mul
	12
	```

Owning the Dot
----
1. Let's say we have a data structure. Show m2data.py.
2. Can go wrong with type checking. Demonstrate with `python3 -i m2data.py`:
	```
	>>> p = Printer(extruders = 2, price = 4000, has_misp = True)
	>>> p.price
	4000             (so far so good, but...)
	>>> q = Printer(extruders = "blue", price = 500, has_misp = 0.5)
	>>> q.price
	500
	>>> q.extruders
	'blue'
	```
3. We can do something about that: Properties (type of descriptor). Show m2properties.py.
4. Lots of code repetition! We can write our own descriptors. Add at the top of m2data.py:
	```
	class Descriptor:
		def __init__(self, name):
			self.name = name
	
		def __get__(self, instance, cls):
			print("Get", self.name)
			return instance.__dict__[self.name]
	
		def __set__(self, instance, value):
			print("Set", self.name)
			instance.__dict__[self.name] = value
	```
5. Now we modify the class to use this descriptor. Edit the Printer class:
	```
	class Printer:
		price = Descriptor("price")
		...
	```
6. Demonstrate the effect with `python3 -i m2data.py`:
	```
	>>> p = Printer(extruders = 2, price = 4000, has_misp = True)
	Set price
	>>> p.price
	Get price
	4000
	>>> p.price = 2000
	Set price
	>>> p.price
	Get price
	2000
	```
7. Using this we can enforce e.g. type checking. Add below Descriptor class:
	```
	class Integer(Descriptor):
		def __set__(self, instance, value):
			if not isinstance(value, int):
				raise Exception("No integer!")
			super().__set__(instance, value)
	```
8. And specify that our price must be integer:
	```
	class Printer:
		price = Integer("price")
		...
	```
9. Demonstrate this effect with `python3 -i m2data.py`:
	```
	>>> p = Printer(extruders = 2, price = 4000, has_misp = True)
	Set price
	>>> p = Printer(extruders = 2, price = "a coffee", has_misp = True)
	...
	Exception("No integer!") 
	```
10. Arbitrary restrictions! Add a minimum price:
	```
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
		...
	```

Exec
----
1. Descriptor performance cost: run:
	```
	python m2performance.py
	```
2. How can we do better? There must be a way. Here's a thought...
3. Modify m3exec.py, add at the top:
	```
	def generate_init(fields):
		s = "def __init__(self, "
		s += ", ".join(fields)
		s += "):\n"
		for field in fields:
			s += f"\tself.{field} = {field}\n"
		return s
	```
4. Demonstrate live with `python3 -i m3exec.py`:
	```
	>>> generate_init(["extruders", "price", "has_misp"])
	'def __init__(self, extruders, price, has_misp):\n ... '
	>>> print(generate_init(["extruders", "price", "has_misp"])
	def __init__(self, extruders, price, has_misp: ...
	```
5. Oh God, what atrocities is this guy up to! We can use that in our class. Modify m3exec.py in Printer class:
	```
	class Printer:
		_fields = ["extruders", "price", "has_misp"]
		exec(generate_init(_fields))
	```
	And remove the original init.
6. Demonstrate again with `python3 -i m3exec.py`:
	```
	>>> p = Printer(2, 4000, True)
	Set price
	```
	It still properly sets the price field. Powerful idea! namedtuple uses this.
7. Use that to improve performance. Modify m3exec.py, replacing __set__ in Descriptor class:
	```
	class Descriptor:
		...
		@staticmethod
		def set_code():
			return ["instance.__dict__[self.name] = value"]
	```
8. Stay with me. We add something similar to Integer:
	```
	@staticmethod
	def set_code():
		return [
			'if not isinstance(value, int):',
			'\traise Error("No integer!")'  # Pay attention to quotes!
		]
	```
9. And to AtLeast (job security going up):
	```
	@staticmethod
	def set_code():
		return [
			'if value < self.minimum:'
			'\traise Error("Too little!")'  # Quotes again!
		]
	```
10. And to Bool:
	```
	@staticmethod
	def set_code():
		return [
			'if not isinstance(value, bool):',
			'\traise Error("No bool!")'  # Quotes again!
		]
	```
11. What can we do with this? Well we could define the setter from these code fragments. Edit Descriptor's init:
	```
	def __init__(self, name):
		self.name = name
		code = "def __set__(self, instance, value):\n\t"
		for cls in self.__class__.__mro__:
			if "__set__" in cls.__dict__:
				code += "\n\t".join(cls.set_code()) + "\n\t"
		print(code)
	```
12. Now if we open this file with `python3 -i m3exec.py` it prints a bunch of code fragments.
13. We can exec these. Modify the Descriptor init again:
	```
	def __init__(self, name):
		... print(code)
		locals = {}
		exec(code, globals(), locals)
		setattr(self.__class__, "__set__", locals["__set__"])  # Technicality: def adds to locals.
	``` 
14. I really hope this works. Demonstrate with `python3 -i m3exec.py`:
	```
	>>> p = Printer(2, 4000, True)
	>>> p.price
	Get price   # Still there!
	4000
	>>> p.price = "bla"
	Exception: No integer!
	>>> p.price = 1000
	Exception: Too little!
	```

Bonus: Metaclass
----
[TODO: Prepare explanation about metaclasses in case there is time left]