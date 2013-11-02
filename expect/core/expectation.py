class Expectation(object):

    def __init__(self, obj, method_name, call_args):
        self._obj = obj
        self._method_name = method_name
        self._call_args = call_args

    def verify(self):
        self._assert_method_called()

    def _assert_method_called(self):
        if self._call_args not in self._method.call_args_list:
            raise AssertionError('Expected %r.%s%r to be called but it '
                                 "wasn't." % (self._obj, self._method_name,
                                              self._call_args))

    @property
    def _method(self):
        return getattr(self._obj, self._method_name)
