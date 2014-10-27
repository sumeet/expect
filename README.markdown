# expect, a Python testing library

### TODO: create a setup.py and put this on PyPI. Sorry!

This library has two features I wanted to copy from RSpec.

1) "cute" assertions, at least that's what I'm calling 'em. For example,
`expect(1) == 1` instead of `assert_equal(1, 1)`. This
was already available for Python as [Expecter Gadget][3], but I rolled the
functionality into this library.

2) RSpec style stubs and mocks. [RSpec's test double syntax][2] is more terse
than using Mock vanilla, and allows for differentiation between mocks and stubs.

Mocks and stubs are two types of test doubles, and they indicate that different
things are happening in a program. Mocks are called `should_receive`
expectations in expect, and if a test includes
`expect(a).should_receive('method_name').with_(arg1, arg2)`, the test will fail
unless `a.method_name` is called with exactly `(arg1, arg2)` as parameters.

Typically, mocks indicate that a destructive or mutating call is happening.
Something where you care about the side effect. For example,
`expect(user_repository).should_receive('save').with_(user)` or
`expect(email_system).should_receive('send').with_(user, message).and_return(receipt)`.

Stubs are similar to mocks and in expect, one would look like this:
`expect(a).stub('method_name').with_(arg).and_return(ret_val)`. So if I called
`a.method_name(arg1)`, it would return `ret_val`. But if you called
`a.method_name` with different arguments, expect will raise `AssertionError`,
ensuring `ret_val` is only returned if the arguments were correct.

Stubs indicate that we expect the return value of a method to be a certain
value if it's called with certain arguments. They can be use to decouple from
a complex calculation that might be in flux: I need to integrate with some
component that tells me the current time but the current time changes every
time you run the test so it's impossible to hardcode it. Another way I typically
use them is to simplify expensive persistence layer setup:
`expect(user_repository).stub('load').with_(user_id).and_return(user)` results
in tests several orders of magnitude faster than tests with
`user = create_user() ; user_repository.save(user)` if we have to interact with
a real database. You can use a stub if you're looking to write a unit test
around a method and don't want to wait on persistence. Or if you don't want to
couple the test to user creation and saving since with the stub, the test no
longer needs to call `create_user` or `user_repository.save`)

The main difference between stubs and mocks is that stubs won't fail the test
if they aren't called. Using vanilla Mock, both `stub` and `should_receive` from
expect look the same:

```python
user_repository = Mock(name='user_repository')

def get_first_name(user_id):
    user = user_repository.load(user_id)
    return user.first_name

# This is a test written using what I've been calling the vanilla Mock style:
def test_returns_a_users_name(self):
    user = Mock(name='user', first_name='Bob')
    # Set up the return value.
    user_repository.load.return_value = user
    # Call the system under test and assert on the return value.
    expect(get_user_name(123)) == 'Bob'
    # Validate that user_repository.load was called correctly.
    user_repository.load.assert_called_once_with(123)

# Note that this was essentially a `should_receive` style test. Mock gives you a
# way to say "This function will return this if you call it, and then you can
# inspect the ways it was called later." but can't say "Only return this if this
# method is called with these arguments but I don't care if the method was ever
# called." So there is no differentiation between stubs and mocks.

# Here's the same test written with expect syntax:
def test_returns_a_users_name(self):
    user = Mock(name='user', first_name='Bob')
    expect(user_repository).stub('load').with_(123).and_return(user)
    expect(get_user_name(123)) == 'Bob'
```

Here's some actual code examples (and it's actually a doctest I keep passing!):

```python
# Just some boiler plate to create a new `expect` that we can start using.
>>> def assert_equal(lhs, rhs):
...     assert lhs == rhs
>>> from expect.ui.expector import Expector
>>> expect = Expector(__eq__=assert_equal)

# We can overload methods on `expect(var)`, including operators like the equals
# operator in this example.

# In this case, `assert_equal(2, 2)` passes silently.
>>> expect(2) == 2

# But in the next case, `assert_equal(2, 3)` raises `AssertionError`.
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
>>> expect.verify()
>>> # `reset()` undoes all patches made by expect.
>>> expect.reset()

>>> # Mocks must be called or `verify()` will raise `AssertionError`.
>>> expect(MyClass).should_receive('my_method').with_(1).and_return(2)
>>> expect.verify()
Traceback (most recent call last):
    ...
AssertionError: Expected <class '__main__.MyClass'>.my_method(1) to be called but it wasn't.

```

## Further reading

The goal of this library is to facilitate writing object-oriented systems with
small, isolated pieces, and to stress the fact that a program is composed of
objects that send messages to each other (i.e., the `stub` and `should_receive`)
terminology). If you're not trying to write software in this way, this library
might not be as useful to you. If you haven't written software in this way
before, you might be interested to hear how I learned about all this, and where
you might go to learn more.

When designing a maintainable system, I prefer smaller components with fewer
dependencies. Fewer dependencies simplify testing because the cost for setting
up the system you're testing is lower. You can decrease the number of
dependencies in a system by introducing abstractions. Good abstractions simplify
program maintenance by dividing distinct responsibilities into discrete pieces
of code and by giving the programmers names to refer to components by. In this
way, writing decoupled systems and unit testing go hand in hand.

I first learned about using mocks and stubs in the way I wrote about in this
README in the [Destroy All Software][4] screencast series, which was my
introduction to both test-driven development and object-oriented design.

[Domain Driven Design][5] discusses isolating and naming components and gives
a lot of terminology for describing components of a system. I don't think it
specifically addresses testing, but systems built the way described in this book
would be testable with expect. It's a really hard book to read and I haven't
even finished it, so while I don't recommend it, I don't know what else to
recommend.

I heard testing in this style is also used in [Growing Object Oriented Software
Guided By Tests][6]. Popular opinion seems to be that GOOS codifies usage of
testing with mocks and stubs but I haven't read it, so I can't say for sure.

[Mocks Aren't Stubs][7] is a popular article on the matter. It explains the
differences between mocks and stubs (and other types of test doubles) and the
relationship between testing and OOD a bit differently and in more detail than I
have.

[1]: http://www.voidspace.org.uk/python/mock/
[2]: https://github.com/rspec/rspec-mocks
[3]: https://github.com/garybernhardt/expecter
[4]: http://www.destroyallsoftware.com/screencasts
[5]: http://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215
[6]: http://www.growing-object-oriented-software.com/
[7]: http://martinfowler.com/articles/mocksArentStubs.html
