import functools
import logging

from .singleton import SingletonDecorator

logger = logging.getLogger(__name__)


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

    # print the log message
    msg = f"[DRYRUN] call to '{func.__name__}({', '.join(func_args)})'"
    logger.info(msg)


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
