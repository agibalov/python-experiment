from dependency_injector import containers, providers


class Greeter:
    def __init__(self, prefix: str, suffix: str) -> None:
        self._prefix = prefix
        self._suffix = suffix

    def greet(self, name: str) -> str:
        return '{}{}{}'.format(self._prefix, name, self._suffix)


class MessageGenerator:
    def __init__(self, greeter: Greeter) -> None:
        self._greeter = greeter

    def make_message(self, name) -> str:
        return '{} How are you?'.format(self._greeter.greet(name))


class IocContainer(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    greeter = providers.Singleton(
        Greeter,
        prefix=config.greetings.prefix,
        suffix=config.greetings.suffix)
    message_generator = providers.Singleton(
        MessageGenerator,
        greeter=greeter)


def test_dummy() -> None:
    container = IocContainer(config={
        'greetings': {
            'prefix': 'Hi, ',
            'suffix': '!!!'
        }
    })
    message_generator: MessageGenerator = container.message_generator()
    assert message_generator.make_message('Andrey') == 'Hi, Andrey!!! How are you?'
