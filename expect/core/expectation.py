class Expectation(object):

    def __init__(self, obj, method_name, call_args):
        self._obj = obj
        self._method_name = method_name
        self._call_args = call_args

    def verify(self):
        if not self._call_args:
            self._assert_method_called_no_args()
        else:
            self._assert_method_called_with_args()
            self._method.assert_any_call(*self._call_args.args,
                                         **self._call_args.kwargs)

    @property
    def _method(self):
        return getattr(self._obj, self._method_name)

    def _assert_method_called_no_args(self):
        if self._method.called == False:
            raise AssertionError("Expected %r.%s to be called but it wasn't." %
                                 (self._obj, self._method_name))

    def _assert_method_called_with_args(self):
        if self._call_args not in self._method.call_args_list:
            raise AssertionError('Expected %r.%s%r to be called but it '
                                 "wasn't." % (self._obj, self._method_name,
                                              self._call_args))
