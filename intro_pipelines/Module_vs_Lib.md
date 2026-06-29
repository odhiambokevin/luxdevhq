# Difference between module, package and library in Python

A Python package and library often seem interchangeable and we hardly pay attention to them in our daily use. But indeed they are very different in technical practice. We will look at the inherent differences between them in this post. But first, let us look at what a Python module is.

## Modules
A Python module, in the simplest terms, is a python file. For example, `cleaning.py`. While they are mostly files and end in `.py` extension, there are exceptions to this.

### Built-in modules
Some of the most common modules like `sys, math, time` are not explicit files. They are embedded into the binary and are compiled directly into the Python interpreter. Since they are not files, they dont end in any extension, not even `.py`. Ww call them *built-in modules*.

### Bytecode compiled modules
When you run a python file, eg our `cleaning.py`, Python compiles the first into a bytecode `.pyc` format. These are very low level instructions that are platform independent and are stored in a `__Pycache__` folder. These help the code run faster the subsequent times it is run. You can even delete the `.py` files and import the `.pyc` files.

### Compiled C extensions
A module is a Python file. Some of these files end in `.so` in Mac/Linux and `.pyd`,`.dll` in Windows. The Python interpreter called **CPython** is written in **C**. It executes the bytecode `(.pyc)` line by line. Some libraries (and we will define a library soon) are actually written in **C** or **C++** and compiled. So when you `import numpy`, the compiled binaries `(modules in the library)`, are loaded just like the `.py` files. 

## Package
When python modules are contained in a directory/folder, we call it a python package. At it\'s basic, package is a folder that contains python modules. We can then import modules from from python packages. Python packages help organize modules into easy to maintain structure.

    streaming/
    │
    ├── __init__.py
    ├── video/
    │   ├── __init__.p
    │   └── visual.py
    │
    └── audio/
        ├── __init__.p
        └── sound.py

The `streaming` package has two sub-packages i.e `video` and `audio`. Module imports or function imports can be done directly as below.
```bash
from streaming.video import video #importing a module from package
from streaming.audio.sound import noice_cancellation #import function from module inside package
```

The `__init__.py` is no longer explicitly required in modern vesion of Python `(3.3+)` when it is empty. In older version it was necessary to be included to inform Python to treat the folder as a Python package. Excluding it would not allow you to import from the modules in that folder.

## Library
A Python library is a collection of reusable Python packages and modules meant to provide broad functionality. This collction is installed together usually using `pip`.

The `Built-in Python modules` discussed above usually come with the `Standard Python Library` when you install Python.