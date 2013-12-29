def singleton(cls):
    return cls()


def falsey_object(class_name):
    return type(class_name, (object,),
                {'__nonzero__': lambda self: False,
                 '__repr__': lambda self: 'falsey_object: ' + class_name})()
