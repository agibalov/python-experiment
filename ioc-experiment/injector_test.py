import threading
from abc import ABC
from contextlib import contextmanager
from dataclasses import dataclass
from typing import cast

import pytest
from injector import Injector, inject, Module, Binder, singleton, Key, provider, SequenceKey, Scope, \
    ScopeDecorator, UnsatisfiedRequirement, InstanceProvider


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


def test_custom_scope() -> None:
    @dataclass
    class Project:
        name: str
        special: bool

    class ProjectScope(Scope):
        def __init__(self, *args, **kwargs):
            super(ProjectScope, self).__init__(*args, **kwargs)
            self.context = None

        @contextmanager
        def __call__(self, project: Project):
            if self.context is not None:
                raise Exception('context is not None')
            self.context = {}
            binder = self.injector.get(Binder)
            binder.bind(Project, to=project, scope=ProjectScope)
            yield
            self.context = None

        def get(self, key, provider):
            if self.context is None:
                raise UnsatisfiedRequirement(None, key)

            try:
                return self.context[key]
            except KeyError:
                provider = InstanceProvider(provider.get(self.injector))
                self.context[key] = provider
                return provider

    class Handler(ABC):
        pass
    class OrdinaryHandler(Handler):
        def __init__(self, project: Project):
            self.project = project
    class SpecialHandler(Handler):
        def __init__(self, project: Project):
            self.project = project
    class SomeSingletonService: pass

    project_scope = ScopeDecorator(ProjectScope)

    class ProjectScopedHandlerModule(Module):
        @project_scope
        @provider
        def handler(self, project: Project) -> Handler:
            if project.special:
                return SpecialHandler(project)
            else:
                return OrdinaryHandler(project)

        @singleton
        @provider
        def some_singleton_service(self, handler: Handler) -> SomeSingletonService:
            return SomeSingletonService()

    injector = Injector([ProjectScopedHandlerModule()], auto_bind=False)

    scope = injector.get(ProjectScope)

    with scope(Project(name='proj1', special=False)):
        handler = injector.get(Handler)
    assert isinstance(handler, OrdinaryHandler)
    assert handler.project.name == 'proj1'

    with scope(Project(name='proj2', special=True)):
        handler = injector.get(Handler)
    assert isinstance(handler, SpecialHandler)
    assert handler.project.name == 'proj2'

    with scope(Project(name='proj3', special=True)):
        @inject
        def f(handler: Handler) -> str:
            return handler.project.name
        assert injector.call_with_injection(f) == 'proj3'

    with pytest.raises(UnsatisfiedRequirement):
        injector.get(SomeSingletonService)

    with scope(Project(name='proj4', special=True)):
        some_singleton_service = injector.get(SomeSingletonService)
    assert injector.get(SomeSingletonService) == some_singleton_service  # !!!


def test_child_injector():
    class ParentScopedService: pass
    class ChildScopedService: pass

    def configure_parent(binder: Binder):
        binder.bind(ParentScopedService, scope=singleton)
    def configure_child(binder: Binder):
        binder.bind(ChildScopedService, scope=singleton)

    parent_injector = Injector(configure_parent, auto_bind=False)
    child_injector = parent_injector.create_child_injector(configure_child, auto_bind=False)

    assert parent_injector.get(ParentScopedService) == parent_injector.get(ParentScopedService)
    assert child_injector.get(ParentScopedService) == child_injector.get(ParentScopedService)

    with pytest.raises(UnsatisfiedRequirement):
        parent_injector.get(ChildScopedService)

    assert child_injector.get(ChildScopedService) == child_injector.get(ChildScopedService)

    # Is this supposed to work or not?
    # https://injector.readthedocs.io/en/latest/terminology.html#child-injectors
    with pytest.raises(UnsatisfiedRequirement):
        parent_injector.get(ChildScopedService)
