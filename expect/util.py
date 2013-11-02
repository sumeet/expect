def singleton(cls):
    return cls()


def falsey_object(class_name):
    return singleton(type(class_name, (object,),
                          {'__nonzero__': lambda self: False}))
