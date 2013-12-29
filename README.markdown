# expect

Tools for creating mocks and stubs. Inspired by [RSpec's test doubles][2] and
[Expecter Gadget][3].

Example:

```python
>>> def assert_equal(lhs, rhs):
...     assert lhs == rhs
>>> from expect.ui.expector import Expector
>>> expect = Expector(__eq__=assert_equal)
>>> expect(2) == 2
>>> expect(2) == 3
Traceback (most recent call last):
    ...
AssertionError

>>> class MyClass(object):
...     @classmethod
...     def my_method(cls, arg):
...         pass

>>> # Stubs don't have to be called.
>>> expect(MyClass).stub('my_method').with_(1).and_return(2)
>>> MyClass.my_method(1)
2
>>> expect.reset()

>>> # Mocks
>>> expect(MyClass).should_receive('my_method').with_(1).and_return(2)
>>> expect.verify()
Traceback (most recent call last):
    ...
AssertionError: Expected to be called once. Called 0 times.

```

[1]: http://www.voidspace.org.uk/python/mock/
[2]: https://github.com/rspec/rspec-mocks
[3]: https://github.com/garybernhardt/expecter
