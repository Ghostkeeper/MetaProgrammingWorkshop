Intro
----
1. Metaprogramming is writing code that creates code.
2. Why metaprogramming: Automating boring task, removing duplicate code.
3. Why not metaprogramming: Hidden magic, complex code, hard to debug.

Function Decorators
----
1. Show m0debugging.py.
2. Use case: Print statements on many functions. Repetitive!
3. Write decorator:
```
def debugme(func):
  print("Generating the wrapped function.")
  def wrapper(*args, **kwargs):
    print(func.__qualname__)
    return func(*args, **kwargs)
  return wrapper
```
4. Modify m0debugging.py: Instead of prints, use @debugme.
5. Demonstrate effect:
```
add(3, 4)
div(3, 4)
```