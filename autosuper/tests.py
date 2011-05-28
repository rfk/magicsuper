"""

  autosuper.tests:  testcases for autosuper module.

"""

import os
import unittest 

import autosuper

class TestAutoSuperDocs(unittest.TestCase):

    def test_readme_matches_docstring(self):
        """Ensure that the README is in sync with the docstring.

        This test should always pass; if the README is out of sync it just
        updates it with the contents of autosuper.__doc__.
        """
        dirname = os.path.dirname
        readme = os.path.join(dirname(dirname(__file__)),"README.rst")
        if not os.path.isfile(readme):
            f = open(readme,"wb")
            f.write(autosuper.__doc__.encode())
            f.close()
        else:
            f = open(readme,"rb")
            if f.read() != autosuper.__doc__:
                f.close()
                f = open(readme,"wb")
                f.write(autosuper.__doc__.encode())
                f.close()


class TestAutoSuper(unittest.TestCase):

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
            self.assertSuperEquals(autosuper._builtin_super(cls),super(cls))
            self.assertSuperEquals(autosuper._builtin_super(cls,obj),
                                   super(cls,obj))
        


if __name__ == "__main__":
    unittest.main()
