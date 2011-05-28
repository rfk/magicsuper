"""

autosuper:  backport the magical zero-argument super() to python2
=================================================================

This is an (awful, hacky, wtf-were-you-thinking) attempt to port the magical
zero-argument super() call from python3 to python2.

In standard python2 usage of the super() builtin, you have to repeat both the
class and instance objects when you call super, like this:

    class Hello(Base):
        def hello(self):
            super(Hello,self).hello()

Using autosuper, you can get the friendlier behaviour from python3 where it
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

"""


__ver_major__ = 0
__ver_minor__ = 1
__ver_patch__ = 0
__ver_sub__ = ""
__version__ = "%d.%d.%d%s" % (__ver_major__,__ver_minor__,__ver_patch__,__ver_sub__)


import sys
import __builtin__

_builtin_super = __builtin__.super

_sentinel = object()

def _auto_super(typ=_sentinel,type_or_obj=_sentinel):
    """Like buildin super(), but capable of magic.

    This acts just like the builtin super() function, but if you don't give
    it any arguments then it tries to infer them at runtime.
    """
    #  Infer the correct call if used without arguments.
    if typ is _sentinel:
        # We'll need to do some frame hacking.
        f = sys._getframe(1)
        # Get the first positional argument of the function.
        try:
            type_or_obj = f.f_locals[f.f_code.co_varnames[0]]
        except (IndexError,KeyError,):
            raise RuntimeError("super() used in a function with no args")
        # Get the MRO so we can crawl it.
        try:
            mro = type_or_obj.__mro__
        except AttributeError:
            try:
                mro = type_or_obj.__class__.__mro__
            except AttributeError:
                raise RuntimeError("super() used with a non-newstyle-class")
        #  Now, find the class owning the currently-executing method.
        for typ in mro:
            for meth in typ.__dict__.itervalues():
                if not isinstance(meth,type(_auto_super)):
                    continue
                if meth.func_code is f.f_code:
                    # Aha!  Found you.
                    break
            else:
                #  Not found, move on to the next class in the MRO.
                continue
            #  Found, break out of the search loop.
            break
        else:
            raise RuntimeError("super() called outside a method")
    #  Now just dispatch to builtin super.
    if type_or_obj is not _sentinel:
        return _builtin_super(typ,type_or_obj)
    return _builtin_super(typ)
    

__builtin__.super = _auto_super


