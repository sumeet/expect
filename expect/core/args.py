from collections import namedtuple

from expect.util import singleton


class Args(namedtuple('Args', 'args kwargs')):

    @classmethod
    def make(cls, *args, **kwargs):
        return cls(args, kwargs)

    def __repr__(self):
        keywords = ['%s=%r' % (arg, value) for arg, value in
                    self.kwargs.iteritems()]
        positional = map(repr, self.args)
        return '(' + ', '.join(positional + keywords) + ')'

    def matches_args(self, args):
        return self == args


@singleton
class AnyArgs(object):

    def matches_args(self, args):
        return True

    def __repr__(self):
        return '(*ANY ARGS)'
