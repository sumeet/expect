from collections import namedtuple


class Args(namedtuple('Args', 'args kwargs')):

    @classmethod
    def make(cls, *args, **kwargs):
        return cls(args, kwargs)

    def __repr__(self):
        keywords = ['%s=%r' % (arg, value) for arg, value in
                    self.kwargs.iteritems()]
        positional = map(repr, self.args)
        return '(' + ', '.join(positional + keywords) + ')'


# XXX: move this util?
def singleton(cls):
    return cls()


@singleton
class NoArgs(object):

    def __nonzero__(self):
        return False
