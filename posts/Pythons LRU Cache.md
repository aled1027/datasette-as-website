# Python's LRU Cache

I've been using Python's LRU cache to cache methods that load files from disk or hit APIs. Because it's caching, I have to be careful to make sure I'm not creating any bugs.

Here are the general rules that I follow the LRU Cache:

- It's easiest to use on functions that aren't part of classes
- When using on classes and you want unique values per class instance (i.e., object), then pass an object identifier as an argument to the cached function.

Here's sample code for using LRU Cache on classes:

```python
from functools import lru_cache
import json

@lru_cache
def load_json_file(filename: str) -> dict:
    """Easiest way to use lru cache is on a function"""
    with open(filename) as fh:
        return json.load(fh)


class MyClass:
    def __init__(self, obj_id: str) -> None:
        # The obj_id could alternative be generatd here, instead of passed,
        # with uuid4
        self.obj_id = obj_id

    def do_work(self, input: str) -> None:
        x = self._shared_retrieve(input)
        y = self._non_shared_retrieve(self.obj_id, input)
        print(x, y)

    @lru_cache
    def _shared_retrieve(self, key: str) -> str:
        """This cache will be shared across all instances of the class"""
        return f"retrieved-value-for-{self.obj_id}-{key}"

    @lru_cache
    def _non_shared_retrieve(self, obj_id: str, key: str) -> str:
        """Assuming the obj id is unique, then this cache will not
        be shared across instances of MyClass
        """

        return f"retrieved-value-for-{self.obj_id}-{obj_id}-{key}"


# https://docs.python.org/3/faq/programming.html#faq-cache-method-calls
obj1 = MyClass("obj1")
obj2 = MyClass("obj2")

obj1.do_work("1")
obj1.do_work("1")
obj2.do_work("1")

# You can observe the cache behavior by seeing the number of hits and misses
# Caches are shared
print(obj1._shared_retrieve.cache_info())
print(obj2._shared_retrieve.cache_info())

# Non shared caches
print(obj1._non_shared_retrieve.cache_info())
print(obj2._non_shared_retrieve.cache_info())
```
