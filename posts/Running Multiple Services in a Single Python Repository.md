# Running Multiple Services in a Single Python Repository

I ran into another issue yesterday setting up a python library with basically two, isolated services that needed to share utilities. I kept hitting the error with attempting relative imports because I was importing the utils relatively with `from ..utils import foo`.

After exploration and testing, I landed on the following structure that works pretty well.

This also uses python's click library for the command line entrypoint.


```
$ tree
.
├── src
│   ├── __pycache__
│   ├── service1
│   │   └── main.py
│   ├── service2
│   │   └── main.py
│   └── utils
│       ├── __init__.py
│       └── utils.py
└── start.py
```

## start.py
```python
import click

from src.service1.main import go as service1_go
from src.service2.main import go as service2_go

@click.command()
@click.option('--service', required=True)
def run(service: str):
    if service == "service1":
        service1_go()
    elif service == "service2":
        service2_go()
    else:
        raise NotImplemented()

if __name__ == '__main__':
    run()
```
## src/service1/main.py
```python
from ..utils.utils import say_hello

def go():
    print("Starting service1")
    say_hello()
```
## src/service2/main.py
```python
from ..utils.utils import say_hello

def go():
    print("Starting service2")
    say_hello()
```
## src/utils/utils.py

```python

def say_hello():
    print("Hello!")
```