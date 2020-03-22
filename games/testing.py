import numpy as np

class Foo(float):
    def __new__(cls, value):
        i = float.__new__(cls, value)
        i._some_argument = "None"
        return i

print(np.array([8., 9.]))
