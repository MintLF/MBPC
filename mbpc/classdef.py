from mbpc.exceptions import InterfaceException
from inspect import signature

def Self():
    self = lambda: ...

    def method(f):
        self.__dict__[f.__name__] = f

    self.method = method
    return self

def Base(self):
    @self.method
    def toString(debug: bool = False):
        if debug:
            return self.__dict__
        return f"{self.__classname__} object"
    
    return self

Base.__mbpctype__ = "class"

def classdef(superClass = Base, *interfaces):
    if superClass.__mbpctype__ == "interface":
        interfaces = list(interfaces)
        interfaces.insert(0, superClass)
        superClass = Base

    def decorator(decoratedClass):
        def decorated(*args, **kwargs):
            self = Self()

            def initialize(*args, **kwargs):
                self.__dict__ |= superClass(self, *args, **kwargs).__dict__

            super = lambda: ...
            for name in self.__dict__:
                super.__dict__[name] = self.__dict__[name]
            super.initialize = initialize
            self.super = super

            self.__classname__ = decoratedClass.__name__
            decoratedClass(self, *args, **kwargs)

            for interface in list(reversed(interfaces)):
                for k in interface.__interface__.methods.keys():
                    if not k in self.__dict__:
                        raise InterfaceException(
                            f"Class \"{self.__classname__}\" does not implement the interface \"{interface.__interface__.__interfacename__}\" (missing the method \"{k}\")."
                        )
                    
                    if not signature(self.__dict__[k]) == interface.__interface__.methods[k]:
                        raise InterfaceException(
                            f"Class \"{self.__classname__}\" does not implement the interface \"{interface.__interface__.__interfacename__}\" (incorrectly defining the method \"{k}\")."
                        )
            return self
        
        def method(f):
            decorated.__dict__[f.__name__] = f

        decorated.method = method
        decorated.__mbpctype__ = "class"
        return decorated
    return decorator
