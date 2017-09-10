'''
magicsuper:  backport the magical zero-argument super() to python2
==================================================================

This is an (awful, hacky, wtf-were-you-thinking) attempt to port the magical
zero-argument super() call from python3 to python2.

In standard python2 usage of the super() builtin, you have to repeat both the
class and instance objects when you call super, like this:

    class Hello(Base):
        def hello(self):
            super(Hello,self).hello()

Using magicsuper, you can get the friendlier behaviour from python3 where it
just figures out the correct call at runtime:

    class Hello(Base):
        def hello(self):
            super().hello()

Of course, you can still explicitly pass in the arguments if you want to do
something strange.  Sometimes you really do want that, e.g. to skip over
some classes in the method resolution order.

How does it work?  By inspecting the calling frame to determine the function
object being executed and the object on which it's being called, and then
walking the object's __mro__ chain to find out where that function was
defined.  Yuck, but it seems to work...

'''

__ver_major__ = 0
__ver_minor__ = 2
__ver_patch__ = 0
__ver_sub__ = ""
__version__ = "%d.%d.%d%s" % (__ver_major__,__ver_minor__,__ver_patch__,__ver_sub__)


import sys

if sys.version_info[0] == 2:
    from _super import super, superm, _builtin_super
