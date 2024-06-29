import sys
import os

os.chdir(sys.path[0])
sys.path.append("..")

import unittest
from mbpc.classdef import classdef

@classdef()
def Cls(self):
    self.super.initialize()

Cls.a = 0
@Cls.method
def increased(by: int):
    Cls.a += by

class TestStaticMethod(unittest.TestCase):
    def testRunningStaticMethod(self):
        Cls.increased(by = 2)
        self.assertEqual(Cls.a, 2)

unittest.main()
