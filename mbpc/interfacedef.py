from mbpc.exceptions import InterfaceException
from inspect import signature

def InterfaceObject():
    interface = lambda: ...
    interface.methods = {}

    def method(func):
        interface.methods[func.__name__] = signature(func)

    interface.method = method
    return interface

def interfacedef(*superInterfaces):
    interface = InterfaceObject()

    for superInterface in list(reversed(superInterfaces)):
        interface.__dict__ |= superInterface.__interface__.__dict__

    def decorator(decoratedInterface):
        decoratedInterface(interface)
        interface.__interfacename__ = decoratedInterface.__name__

        def decorated(*args, **kwargs):
            raise InterfaceException("Cannot initialize an interface object.")
        
        decorated.__interface__ = interface
        decorated.__mbpctype__ = "interface"
        return decorated
    return decorator
