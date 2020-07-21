#!/usr/bin/env python3
##
## Authors: Adriano Marques
##          Nathan Martins
##          Thales Ribeiro
##
## Copyright (C) 2019 Exponential Ventures LLC
##
##    This library is free software; you can redistribute it and/or
##    modify it under the terms of the GNU Library General Public
##    License as published by the Free Software Foundation; either
##    version 2 of the License, or (at your option) any later version.
##
##    This library is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##    Library General Public License for more details.
##
##    You should have received a copy of the GNU Library General Public
##    License along with this library; if not, write to the Free Software
##    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
##


import functools
import logging

from .singleton import SingletonDecorator


def log_call(func, *args, **kw):
    """
        Produce a info message which logs the *func* call.
    """
    # concatenate args and kw args transforming string values
    # from 'value' to '"value"' in order to pretty display
    func_args = []

    # concatenate positional args
    args = list(args)
    if args:
        for i, arg in enumerate(args):
            if type(arg) is str:
                args[i] = f'"{arg}"'
        func_args.extend([str(arg) for arg in args])

    # concatenate non positional args
    if kw:
        for key, value in kw.items():
            if type(value) is str:
                kw[key] = f'"{value}"'

        func_args.extend([f"{k}={v}" for k, v in kw.items()])

    logging.debug(f"[DRYRUN] call to '{func.__name__}({', '.join(func_args)})'")


def is_dry_run() -> bool:
    return Dehydrator().status


def dehydratable(func):
    """
    Decorator which makes a log the call of the target
    function without executing it.

    Example:
        >>> @dehydratable
        ... def foo(bar, baz=None):
        ...     return 42
        ...
        >>> foo('sport', baz=False)
        42
        >>> foo('sport', baz=False)
        INFO:aurum.dry_run:[DRYRUN] call to 'foo(sport, baz=False)'

    """

    @functools.wraps(func)
    def decorator(*args, **kw):
        # if dry run is disabled exec the original method
        if is_dry_run() is False:
            return func(*args, **kw)
        else:
            log_call(func, *args, **kw)
            return None

    return decorator


@SingletonDecorator
class Dehydrator:

    def __init__(self) -> None:
        self._status = False

    def on(self):
        self._status = True

    def off(self):
        self._status = False

    @property
    def status(self):
        return self._status
