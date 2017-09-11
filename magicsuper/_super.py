# -*- coding: utf-8 -*-
import sys
from types import FunctionType
import __builtin__

_builtin_super = __builtin__.super
_SENTINEL = object()

def super(typ=_SENTINEL, type_or_obj=_SENTINEL, framedepth=1):
    '''Like builtin super(), but capable of magic.

    This acts just like the builtin super() function, but if called
    without any arguments it attempts to infer them at runtime.
    '''
    #  Infer the correct call if used without arguments.
    if typ is _SENTINEL:
        # We'll need to do some frame hacking.
        f = sys._getframe(framedepth)

        try:
            # Get the function's first positional argument.
            type_or_obj = f.f_locals[f.f_code.co_varnames[0]]
        except (IndexError,KeyError,):
            raise RuntimeError('super() used in a function with no args')

        try:
            # Get the MRO so we can crawl it.
            mro = type_or_obj.__mro__
        except AttributeError:
            try:
                mro = type_or_obj.__class__.__mro__
            except AttributeError:
                raise RuntimeError('super() used with a non-newstyle class')

        #   A ``for...else`` block?  Yes!  It's odd, but useful.
        #   If unfamiliar with for...else, see:
        #
        #       http://psung.blogspot.com/2007/12/for-else-in-python.html
        for typ in mro:
            #  Find the class that owns the currently-executing method.
            for meth in typ.__dict__.itervalues():
                # Drill down through any wrappers to the underlying func.
                # This handles e.g. classmethod() and staticmethod().
                try:
                    while not isinstance(meth,FunctionType):
                        try:
                            meth = meth.__func__
                        except AttributeError:
                            meth = meth.__get__(type_or_obj)
                except (AttributeError, TypeError):
                    continue
                if meth.func_code is f.f_code:
                    break   # Aha!  Found you.
            else:
                continue    #  Not found! Move onto the next class in MRO.
            break    #  Found! Break out of the search loop.
        else:
            raise RuntimeError('super() called outside a method')

    #  Dispatch to builtin super().
    if type_or_obj is not _SENTINEL:
        return _builtin_super(typ,type_or_obj)
    return _builtin_super(typ)


def superm(*args,**kwds):
    f = sys._getframe(1)
    nm = f.f_code.co_name
    return getattr(super(framedepth=2),nm)(*args,**kwds)


__builtin__.super = super
