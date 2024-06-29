from mbpc.interfacedef import interfacedef

@interfacedef()
def Hashable(interface):
    @interface.method
    def hash() -> int: ...
