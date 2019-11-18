from abc import ABC
from dataclasses import dataclass
from typing import Union

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Benchmark(ABC):
    id: str
    name: str


@dataclass_json
@dataclass
class Dummy1Benchmark(Benchmark):
    min: float
    max: float


@dataclass_json
@dataclass
class Dummy2Benchmark(Benchmark):
    score: float


@dataclass_json
@dataclass
class BenchmarkContainer:
    benchmark: Union[Dummy1Benchmark, Dummy2Benchmark]


def test_it_works():
    assert BenchmarkContainer.schema().dump(BenchmarkContainer(
        benchmark=Dummy1Benchmark(id='one', name='The One', min=1.11, max=2.22 ))) == {
        'benchmark': {
            'max': 2.22,
            'name': 'The One',
            'id': 'one',
            'min': 1.11,
            '__type': 'Dummy1Benchmark'
        }
    }
    assert BenchmarkContainer.schema().dump(BenchmarkContainer(
        benchmark=Dummy2Benchmark(id='two', name='The Two', score=3.33))) == {
        'benchmark': {
            'name': 'The Two',
            'id': 'two',
            'score': 3.33,
            '__type': 'Dummy2Benchmark'
        }
    }

    assert BenchmarkContainer.schema().load({"benchmark": {
        "id": "one", "name": "The One", "min": 1.23, "max": 3.45, "__type": "Dummy1Benchmark"}
    }) == BenchmarkContainer(benchmark=Dummy1Benchmark(id='one', name='The One', min=1.23, max=3.45))
    assert BenchmarkContainer.schema().load({"benchmark": {
        "id": "two", "name": "The Two", "score": 12.34, "__type": "Dummy2Benchmark"}
    }) == BenchmarkContainer(benchmark=Dummy2Benchmark(id='two', name='The Two', score=12.34))
