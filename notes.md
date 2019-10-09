Intro
----
1. Metaprogramming is writing code that creates code.
2. Why metaprogramming: Automating boring task, removing duplicate code.
3. Why not metaprogramming: Hidden magic, complex code, hard to debug.
4. Generally a bad idea. Live coding, also a bad idea.

Function Decorators
----
1. Show m0debugging.py.
2. Use case: Write print statements on all 3 functions. Repetitive!
3. Write decorator at the top of m0debugging.py:
	```
	def debugme(func):
		print("Decorating a function!")
		def wrapper(*args, **kwargs):
			print(func.__qualname__)
			return func(*args, **kwargs)
		return wrapper
	```
4. Modify code: Instead of prints, use @debugme.
5. Demonstrate effect with `python3`:
	```
	>>> from m0debugging import *
	Decorating a function!
	Decorating a function!
	Decorating a function!
	>>> add(3, 4)
	add
	7
	>>> sub(3, 4)
	sub
	-1
	```
6. You could replace the prints with logging or profiling later, just in one place.
7. Present alternatives: Class decorator or going crazy with a metaclass?

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
	Decorating a function!
	Decorating a function!
	Decorating a function!
	>>> m = Maths()
	>>> m.add(3, 4)
	Maths.add
	7
	>>> m.mul(3, 4)
	Maths.mul
	12
	```

Alternative: Metaclasses
----
1. All those @debugme are still repetitive. Want to debug an entire class?
2. Show m1classdec.py
3. Present `metaclass=?` property of class definition.
4. Object is instance of class, class is instance of type. Demonstrate in `python3`:
	```
	>>> class Foo:
	>>>   pass
	>>> x = Foo()
	>>> type(x)
	<class '__main__.Foo'>
	>>> type(type(x))
	<class 'type'>
	```
5. Classes are instances of the metaclass "type". First-class citizen.
6. The function of the "type" is to create an instance, reserve memory, etc.
7. Demonstrate in m1classdec.py:
	```
	class DebugMeta(type):
		def __new__(typ, name, bases, clsdict):
			print("name:", name)
			print("bases:", bases)
			print("clsdict:", clsdict)
			return super().__new__(typ, name, bases, clsdict)

	class Maths(metaclass = DebugMeta): ...
	```
8. Now show what happens with `python3 -i m1classdec.py`:
	```
	name: Maths     # The name of our class.
	bases: ()       # Superclasses.
	clsdict: { ...} # All of the contents of the class.
	```
9. Modify the contents to wrap debugme! Edit m1classdec.py:
	```
	from m0answer import debugme
	class DebugMeta(type):
		def __new__(...)
			...print("clsdict:", clsdict)
			for key, val in clsdict.items():
				if callable(val):
					clsdict[key] = debugme(val)
			...return super().__new__(...)
	```
10. Demonstrate again in `python3 -i m1classdec.py`:
	```
	Decorating a function!
	Decorating a function!
	Decorating a function! (wrapped 3 times)
	>>> m = Maths()
	>>> m.add(3, 4)
	Maths.add
	7
	```
11. So it wrapped every function just like we told it to, during declaration of the class.
12. Most things that can be done with metaclasses can also be done with inheritance or class decorators (also this one).
13. Planned for C++20! As if it weren't complex enough there.

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
				raise ValueError("No int!")
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
	Exception("No int!")
	```
10. Arbitrary restrictions! Add a minimum price:
	```
	class AtLeast(Descriptor):
		def __init__(self, name, minimum):
			self.minimum = minimum
			super().__init__(name)
	
		def __set__(self, instance, value):
			if value < self.minimum:
				raise ValueError("Not enough!")
			super().__set__(instance, value)

	class MinimumInt(Integer, AtLeast):  # Using descriptors as mixins here.
		pass

	class Printer:
		price = MinimumInt("price", 2000)
		...
	```

Exec
----
1. Descriptor performance cost: run `python3 m2performance.py`
2. How can we do better? There must be a way. Here's a thought... Wrapping functions and inheritance costs performance.
3. Modify m3exec.py, replacing \_\_set\_\_ in Descriptor class:
	```
	class Descriptor:
		...
		@staticmethod
		def set_code():
			return ["instance.__dict__[self.name] = value"]
	```
4. Stay with me. We add something similar to Integer:
	```
	@staticmethod
	def set_code():
		return [
			'if not isinstance(value, int):',  # Commas!
			'\traise ValueError("No int!")'  # Pay attention to quotes!
		]
	```
5. And to AtLeast (job security going up):
	```
	@staticmethod
	def set_code():
		return [
			'if value < self.minimum:',
			'\traise ValueError("Not enough!")'  # Quotes again!
		]
	```
6. And to Bool:
	```
	@staticmethod
	def set_code():
		return [
			'if not isinstance(value, bool):',
			'\traise ValueError("No bool!")'  # Quotes again!
		]
	```
7. What can we do with this? Well we could define the setter from these code fragments. Edit Descriptor's init:
	```
	def __init__(self, name):
		self.name = name
		code = "def __set__(self, instance, value):\n\t"
		for cls in self.__class__.__mro__:
			if "set_code" in cls.__dict__:
				code += "\n\t".join(cls.set_code()) + "\n\t"
		print(code)
	```
8. Now if we open this file with `python3 -i m3exec.py` it prints a bunch of code fragments.
9. We can exec these. Modify the Descriptor init again:
	```
	def __init__(self, name):
		... print(code)
		locals = {}
		exec(code, globals(), locals)
		setattr(self.__class__, "__set__", locals["__set__"])  # Technicality: def adds to locals.
	``` 
10. I really hope this works. Demonstrate with `python3 -i m3exec.py`:
	```
	>>> p = Printer(2, 4000, True)
	>>> p.price
	Get price   # Still there!
	4000
	>>> p.price = "bla"
	Exception: No int!
	>>> p.price = 1000
	Exception: Not enough!
	```
11. Let's see if that makes it better: `python3 m3performance.py`
12. Still not as good, but we're doing type checking.

Onwards
----
1. Based on metaprogramming workshop from David Beazley.
2. He goes on to construct classes from XML files and override the import statement.
