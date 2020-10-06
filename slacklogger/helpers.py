import os
import inspect


def my_func_name(f):
    return f.__name__


def my_script_name(f):
    return os.path.abspath(inspect.getfile(f))


def my_details(f):
    return my_func_name(f), my_script_name(f)
