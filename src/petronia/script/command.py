

class Command(object):
    def __init__(self, name, invoker):
        self.__name = name
        self.__invoker = invoker

    @property
    def name(self):
        return self.__name

    def matches(self, arg):
        return arg.strip().lower() == self.name

    def invoke(self, bus, args):
        self.__invoker(bus, *args)

    def describe(self):
        return self.__invoker.__doc__

    def __str__(self):
        print("Cmd({0})".format(self.__name))
