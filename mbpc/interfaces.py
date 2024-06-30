from mbpc.interfacedef import interfacedef

@interfacedef()
def Hashable(interface):
    @interface.method
    def hash() -> int: ...

@interfacedef()
def Equatable(interface):
    @interface.method
    def equals(object) -> bool: ...
