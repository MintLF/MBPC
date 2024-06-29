import sys
import os

os.chdir(sys.path[0])
sys.path.append("..")

import unittest
from mbpc.classdef import classdef

@classdef()
def Cls(self, a: int = 1):
    self.super.initialize()
    self.a = a

    @self.method
    def increased(by: int):
        self.a += by

class TestCreatingClass(unittest.TestCase):
    def setUp(self):
        self.obj = Cls(a = 2)

    def testInitialize(self):
        self.assertEqual(self.obj.a, 2)

    def testRunningMethod(self):
        self.obj.increased(by = 3)
        self.assertEqual(self.obj.a, 5)

    def testToString(self):
        self.assertEqual(self.obj.toString(), "Cls object")

unittest.main()
