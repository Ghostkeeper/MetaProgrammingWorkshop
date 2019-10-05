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
5. Demonstrate effect:
```
from m0debugging import *
add(3, 4)
div(3, 4)
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

Owning the Dot
----
[TODO: Explanation about getattr and setattr]

Exec
----
[TODO: Explanation about generating code as string and exec'ing it]

Bonus: Metaclass
----
[TODO: Prepare explanation about metaclasses in case there is time left]