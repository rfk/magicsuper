
magicsuper: backport of Python 3 ``super()`` to Python 2
=========================================================================

This is an (awful, hacky, WTF-were-you-thinking) attempt to port the magical
zero-argument ``super()`` call from Python 3 to Python 2.

In standard Python 2, you have to repeat both the
class and instance objects when calling ``super()``—like this:

    class Hello(Base):
        def hello(self):
            super(Hello,self).hello()

Using ``magicsuper``, you can get the friendlier behaviour from Python 3, which
just figures out the correct call at runtime:

    class Hello(Base):
        def hello(self):
            super().hello()

Of course, you can still explicitly pass in the arguments if you *want* to do
something strange.  Sometimes it’s desirable—for example, to skip over
some classes in the method resolution order.


How does it work?  
-----------------

By inspecting the calling frame to:

- determine the function object being executed
- determine the object on which it’s being called, and then
- walking the object’s ``__mro__`` chain to find out where that function was
defined.  

Yuck, but it seems to work...

