import sys
import os

os.chdir(sys.path[0])
sys.path.append("..")

import unittest
from mbpc.classdef import classdef
from mbpc.interfaces import Hashable
from mbpc.interfacedef import interfacedef

@interfacedef(Hashable)
def Hashable2(interface):
    @interface.method
    def hash2() -> str: ...

@classdef(Hashable2)
def Cls(self, a: int = 1):
    self.super.initialize()
    self.a = a

    @self.method
    def increased(by: int):
        self.a += by

    @self.method
    def hash() -> int:
        return self.a.__hash__()
    
    @self.method
    def hash2() -> str:
        return str(self.a.__hash__())

class TestImplementInterface(unittest.TestCase):
    def setUp(self):
        self.obj = Cls(a = 2)

    def testRunningMethod(self):
        self.obj.increased(by = 3)
        self.assertEqual(self.obj.hash2(), str(hash(5)))

unittest.main()