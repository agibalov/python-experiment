import asyncio
import contextvars

import pytest


def test_run():
    async def main():
        print('hello')
        await asyncio.sleep(0.1)
        print('world')
        return 123

    assert asyncio.run(main()) == 123


def test_create_task():
    async def main():
        async def sum(a: int, b: int):
            await asyncio.sleep(0.1)
            return a + b
        task = asyncio.create_task(sum(2, 3))
        return await task
    assert asyncio.run(main()) == 5


@pytest.mark.asyncio
async def test_cancel():
    async def get_message(delay: float):
        await asyncio.sleep(delay)
        return 'hello world'
    task = asyncio.create_task(get_message(1))
    await asyncio.sleep(0.1)
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert task.cancelled()


@pytest.mark.asyncio
async def test_gather():
    async def sum(a: int, b: int):
        await asyncio.sleep(0.1)
        return a + b

    assert await asyncio.gather(sum(2, 3), sum(5, 9)) == [5, 14]


@pytest.mark.asyncio
async def test_wait_for():
    async def get_message(delay: float):
        await asyncio.sleep(delay)
        return 'hello world'

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(get_message(0.1), timeout=0.01)

    assert await asyncio.wait_for(get_message(0.1), timeout=1) == 'hello world'

dummy_var = contextvars.ContextVar('dummy')


@pytest.mark.asyncio
async def test_context_var():
    async def get_dummy():
        await asyncio.sleep(0)
        return dummy_var.get()

    async def test(value: str):
        await asyncio.sleep(0)
        dummy_var.set(value)
        await asyncio.sleep(0)
        return await get_dummy()

    assert await asyncio.gather(test('hello'), test('world')) == ['hello', 'world']
