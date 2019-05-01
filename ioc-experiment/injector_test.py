from abc import ABC
from typing import cast

from injector import Injector, inject, Module, Binder, singleton, MappingKey, Key, provider, SequenceKey


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
    class Handler3(Handler):
        def __init__(self, something: str):
            self.something = something

    Handlers = SequenceKey('handlers')
    Something = Key('something')

    def configure(binder: Binder) -> None:
        binder.multibind(Handlers, [Handler1()], scope=singleton)
        binder.multibind(Handlers, [Handler2()], scope=singleton)
        binder.bind(Something, 'hello', scope=singleton)

    class OmgModule(Module):
        @singleton
        @provider
        def handler3(self, something: Something) -> Handlers:
            return [Handler3(cast(str, something))]

    injector = Injector([configure, OmgModule])
    handlers = injector.get(Handlers)
    assert isinstance(handlers[0], Handler1)
    assert isinstance(handlers[1], Handler2)
    assert isinstance(handlers[2], Handler3)
    assert handlers[2].something == 'hello'
