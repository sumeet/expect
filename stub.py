from collections import namedtuple

from args import Args


class UnknownArgumentsError(Exception): pass


MethodCall = namedtuple('MethodCall', 'name args')


class ReturnValue(namedtuple('ReturnValue', 'args return_value')):

    has_value = True

    @classmethod
    def default(cls, return_value):
        return cls(cls._no_args, return_value)

    class _no_args(object): pass


class NoReturnValue(object):

    has_value = False


class Stub(object):

    def __init__(self, name):
        self._name = name
        self._return_values = []
        self.unset_default_return_value()

    @property
    def name(self):
        return self._name

    def add_return_value(self, args, return_value):
        self._return_values.append(ReturnValue(args, return_value))

    def set_default_return_value(self, return_value):
        self._default_return_value = ReturnValue.default(return_value)

    def unset_default_return_value(self):
        self._default_return_value = NoReturnValue

    def __call__(self, *args, **kwargs):
        args = Args(args, kwargs)
        return_value = self._get_return_value(args)
        if return_value.has_value:
            return return_value.return_value
        else:
            raise UnknownArgumentsError(args)

    def __repr__(self):
        return '%s(name=%r)' % (type(self).__name__, self.name)

    def _get_return_value(self, args):
        for return_value in self._return_values:
            if return_value.args == args:
                return return_value
        return self._default_return_value
