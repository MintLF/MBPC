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
        print(self, self.__dict__)
        if debug:
            return self.__dict__
        return f"{self.__classname__} object"
    
    return self

Base.__mbpctype__ = "class"
Base.__interfaces__ = []

def classdef(superClass = Base, *interfaces):
    interfaces = list(interfaces)
    if superClass.__mbpctype__ == "interface":
        interfaces.insert(0, superClass)
        superClass = Base
    interfaces.extend(superClass.__interfaces__)

    def decorator(decoratedClass):
        def decorated(*args, **kwargs):
            self = Self()
            args = list(args)
            if args and type(args[0]) == type(self): 
                self = args[0]
                args.pop(0)

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

        decorated.__dict__ = superClass.__dict__ | decorated.__dict__
        decorated.method = method
        decorated.__mbpctype__ = "class"
        decorated.__interfaces__ = interfaces

        def initialize():
            for interface in list(reversed(interfaces)):
                for k in interface.__methods__.keys():
                    if not k in decorated.__dict__:
                        raise InterfaceException(
                            f"Class \"{decoratedClass.__name__}\" does not implement the interface \"{interface.__interface__.__interfacename__}\" (missing the static method \"{k}\")."
                        )
                    
                    if not signature(decorated.__dict__[k]) == interface.__methods__[k]:
                        raise InterfaceException(
                            f"Class \"{decoratedClass.__name__}\" does not implement the interface \"{interface.__interface__.__interfacename__}\" (incorrectly defining the static method \"{k}\")."
                        )
                    
        decorated.initialize = initialize
        return decorated
    return decorator
