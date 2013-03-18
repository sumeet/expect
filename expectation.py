class Expectation(object):

    def __init__(self, obj, method_name):
        self._obj = obj
        self._method_name = method_name
        self._args = None

    def verify(self):
        if not self._args:
            if self._method.called == False:
                raise AssertionError('Expected %r.%s to be called but it was not' %
                                    (self._obj, self._method_name))
        else:
            self._method.assert_any_call(*self._args.args, **self._args.kwargs)

    def set_args(self, args):
        self._args = args

    @property
    def _method(self):
        return getattr(self._obj, self._method_name)
