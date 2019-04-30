from abc import ABC

from injector import Injector, inject, Module, Binder, singleton, MappingKey, Key


class Greeter:
    def __init__(self, prefix: str, suffix: str) -> None:
        self._prefix = prefix
        self._suffix = suffix

    def greet(self, name: str) -> str:
        return '{}{}{}'.format(self._prefix, name, self._suffix)


class MessageGenerator:
    @inject
    def __init__(self, greeter: Greeter) -> None:
        self._greeter = greeter

    def make_message(self, name: str) -> str:
        return '{} How are you?'.format(self._greeter.greet(name))


class AppModule(Module):
    def __init__(self, greeting_prefix: str, greeting_suffix: str):
        self._greeting_prefix = greeting_prefix
        self._greeting_suffix = greeting_suffix

    def configure(self, binder: Binder):
        binder.bind(Greeter, to=Greeter(
            prefix=self._greeting_prefix,
            suffix=self._greeting_suffix
        ))


def test_dummy() -> None:
    injector = Injector([AppModule(
        greeting_prefix='Hi, ',
        greeting_suffix='!!!')])
    message_generator: MessageGenerator = injector.get(MessageGenerator)
    assert message_generator.make_message('Andrey') == 'Hi, Andrey!!! How are you?'


def test_multibind() -> None:
    class Handler(ABC): pass
    class Handler1(Handler): pass
    class Handler2(Handler): pass

    def configure(binder: Binder) -> None:
        binder.multibind(Handler, [Handler1()], scope=singleton)
        binder.multibind(Handler, [Handler2()], scope=singleton)

    injector = Injector([configure])
    handlers = injector.get(Handler)
    assert isinstance(handlers[0], Handler1)
    assert isinstance(handlers[1], Handler2)
