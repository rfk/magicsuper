
Status: Unmaintained
====================

.. image:: http://unmaintained.tech/badge.svg
     :target: http://unmaintained.tech/
     :alt: No Maintenance Intended

I am `no longer actively maintaining this project <https://rfk.id.au/blog/entry/archiving-open-source-projects/>`_.


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

