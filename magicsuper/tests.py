"""

  magicsuper.tests:  testcases for magicsuper module.

"""

import os
import unittest 

import magicsuper

class TestMagicSuperDocs(unittest.TestCase):

    def test_readme_matches_docstring(self):
        """Ensure that the README is in sync with the docstring.

        This test should always pass; if the README is out of sync it just
        updates it with the contents of magicsuper.__doc__.
        """
        dirname = os.path.dirname
        readme = os.path.join(dirname(dirname(__file__)),"README.rst")
        if not os.path.isfile(readme):
            f = open(readme,"wb")
            f.write(magicsuper.__doc__.encode())
            f.close()
        else:
            f = open(readme,"rb")
            if f.read() != magicsuper.__doc__:
                f.close()
                f = open(readme,"wb")
                f.write(magicsuper.__doc__.encode())
                f.close()


class TestMagicSuper(unittest.TestCase):

    def test_basic_diamond(self):
        class Base(object):
            def calc(self,value):
                return 2 * value
        class Sub1(Base):
            def calc(self,value):
                return 7 + super().calc(value)
        class Sub2(Base):
            def calc(self,value):
                return super().calc(value) - 1
        class Diamond(Sub1,Sub2):
            def calc(self,value):
                return 3 * super().calc(value)
        b = Base()
        s1 = Sub1()
        s2 = Sub2()
        d = Diamond()
        for x in range(10):
            self.assertEquals(b.calc(x),2*x)
            self.assertEquals(s1.calc(x),7+(2*x))
            self.assertEquals(s2.calc(x),(2*x)-1)
            self.assertEquals(d.calc(x),3*(7+((2*x)-1)))

    def test_with_unrelated_methods(self):
        class Base(object):
            def hello(self):
                return "world"
        class Sub(Base):
            def hello(self):
                return "hello " + super().hello()
            def other(self):
                pass
        class SubSub(Sub):
            def other(self):
                return super().other()
        ss = SubSub()
        self.assertEquals(ss.hello(),"hello world")

    def test_fails_for_oldstyle_class(self):
        class OldStyle:
            def testme(self):
                return super().testme()
        o = OldStyle()
        self.assertRaises(RuntimeError,o.testme)

    def test_fails_for_raw_functions(self):
        def not_a_method():
            super().not_a_method()
        self.assertRaises(RuntimeError,not_a_method)
        def not_a_method(self):
            super().not_a_method()
        self.assertRaises(RuntimeError,not_a_method,self)

    def assertSuperEquals(self,sobj1,sobj2):
        assert sobj1.__self__ is sobj2.__self__
        assert sobj1.__self_class__ is sobj2.__self_class__
        assert sobj1.__thisclass__ is sobj2.__thisclass__

    def test_call_with_args_does_nothing(self):
        class Base(object):
            def calc(self,value):
                return 2 * value
        class Sub1(Base):
            def calc(self,value):
                return 7 + super().calc(value)
        class Sub2(Base):
            def calc(self,value):
                return super().calc(value) - 1
        class Diamond(Sub1,Sub2):
            def calc(self,value):
                return 3 * super().calc(value)
        for cls in (Base,Sub1,Sub2,Diamond,):
            obj = cls()
            self.assertSuperEquals(magicsuper._builtin_super(cls),super(cls))
            self.assertSuperEquals(magicsuper._builtin_super(cls,obj),
                                   super(cls,obj))

    def test_superm(self):
        class Base(object):
            def getit(self):
                return 2
        class Sub(Base):
            def getit(self):
                return 10 * magicsuper.superm()
        s = Sub()
        self.assertEquals(s.getit(),20)

    def test_use_inside_dunder_new(self):
        class Terminal(str):
            def __new__(cls, value, token_type):
                self = super().__new__(cls, value)
                self.token_type = token_type
                return self
        DOT = Terminal(".", "dit")
        self.assertTrue(isinstance(DOT, str))
        self.assertTrue(isinstance(DOT, Terminal))

    def test_use_inside_classmethod(self):
        class Base(object):
            @classmethod
            def getit(cls):
                return 42
        class Singleton(Base):
            @classmethod
            def getit(cls):
                print super()
                return super().getit() + 1
        self.assertEquals(Singleton.getit(), 43)


if __name__ == "__main__":
    unittest.main()
