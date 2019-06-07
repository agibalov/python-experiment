import sys
from typing import Any, Callable, Dict

from injector import Injector, Binder
from pytest import fixture


def register_injector_fixtures(definitions: Dict[str, Callable[[Injector], Any]]) -> None:
    def make_fixture(name: str, resolver: Callable[[Injector], Any]) -> Any:
        def f(injector: Injector):
            return resolver(injector)
        f.__name__ = name
        return f

    for (name, resolver) in definitions.items():
        f = make_fixture(name, resolver)
        setattr(sys.modules[__name__], name, fixture()(f))

class ServiceA: pass
class ServiceB: pass

@fixture
def injector():
    def configure(binder: Binder) -> None:
        binder.bind(ServiceA)
        binder.bind(ServiceB)
    injector = Injector([configure])
    return injector


register_injector_fixtures({
    'service_a': lambda i: i.get(ServiceA),
    'service_b': lambda i: i.get(ServiceB)
})

def test(service_a: ServiceA, service_b: ServiceB) -> None:
    print(service_a, service_b)
