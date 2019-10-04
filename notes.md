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
  print("Generating the wrapped function.")
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

