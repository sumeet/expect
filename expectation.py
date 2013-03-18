class Expectation(object):

    def __init__(self, obj, method_name):
        self._obj = obj
        self._method_name = method_name

    def verify(self):
        if getattr(self._obj, self._method_name).called == False:
            raise AssertionError('Expected %r.%s to be called but it was not' %
                                 (self._obj, self._method_name))
