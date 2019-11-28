import asyncio
import json
import logging
from io import StringIO
from traceback import print_exception

from logbook import TestHandler, Processor, Handler
from logbook.compat import redirected_logging


def text_formatter(record, handler):
    extras = ', '.join([f'{k}={v}' for k, v in record.extra.items() if v is not None])

    exception_info = ''
    if record.exc_info is not None:
        (clazz, exception, traceback) = record.exc_info
        with StringIO() as f:
            print_exception(clazz, exception, traceback, file=f)
            exception_info = f.getvalue()

    return f'[{record.time:%Y-%m-%d %H:%M:%S.%f%z}] {record.level_name}: {record.channel}: ' \
           f'{record.message} <{extras}> {exception_info}'


def json_formatter(record, handler):
    exception_dictionary = {}
    if record.exc_info is not None:
        (clazz, exception, traceback) = record.exc_info
        with StringIO() as f:
            print_exception(clazz, exception, traceback, file=f)
            exception_info = f.getvalue()
            exception_dictionary = {'exception': exception_info}

    return json.dumps({
        **{
            'time': record.time.isoformat(),
            'level': record.level_name,
            'name': record.channel,
            'message': record.message
        },
        **{k: v for k, v in record.extra.items() if v is not None},
        **exception_dictionary
    })


def test_standard_logging_works():
    with TestHandler() as handler:
        logger = logging.getLogger('Dummy')
        with redirected_logging():
            logger.info('hello world')
        assert handler.formatted_records == [
            '[INFO] Dummy: hello world'
        ]


def test_mdc_works():
    def inject_extra(record):
        record.extra['ip'] = '127.0.0.1'
        record.extra['username'] = 'Andrey'

    with TestHandler() as handler:
        handler.formatter = text_formatter
        logger = logging.getLogger('Dummy')
        with redirected_logging():
            with Processor(inject_extra):
                logger.info('hello world')
        assert len(handler.formatted_records) == 1
        assert 'INFO: Dummy: hello world <ip=127.0.0.1, username=Andrey>' in handler.formatted_records[0]


def test_json_formatting_works():
    def inject_extra(record):
        record.extra['ip'] = '127.0.0.1'
        record.extra['username'] = 'Andrey'

    with TestHandler() as handler:
        handler.formatter = json_formatter
        logger = logging.getLogger('Dummy')
        with redirected_logging():
            with Processor(inject_extra):
                logger.info('hello world')
        assert len(handler.formatted_records) == 1
        record = json.loads(handler.formatted_records[0])
        assert record['level'] == 'INFO'
        assert record['name'] == 'Dummy'
        assert record['message'] == 'hello world'
        assert record['ip'] == '127.0.0.1'
        assert record['username'] == 'Andrey'


def test_exception_text_formatter():
    with TestHandler() as handler:
        handler.formatter = text_formatter
        logger = logging.getLogger('Dummy')
        with redirected_logging():
            try:
                raise Exception('Something bad!')
            except Exception:
                logger.error('hello world', exc_info=True)
        assert len(handler.formatted_records) == 1
        record = handler.formatted_records[0]
        assert 'ERROR: Dummy: hello world' in record
        assert '/logbook_test.py' in record
        assert 'Exception: Something bad!' in record


def test_exception_json_formatter():
    with TestHandler() as handler:
        handler.formatter = json_formatter
        logger = logging.getLogger('Dummy')
        with redirected_logging():
            try:
                raise Exception('Something bad!')
            except Exception:
                logger.error('hello world', exc_info=True)
        assert len(handler.formatted_records) == 1
        record = json.loads(handler.formatted_records[0])
        assert record['level'] == 'ERROR'
        assert record['name'] == 'Dummy'
        assert record['message'] == 'hello world'
        assert '/logbook_test.py' in record['exception']
        assert 'Exception: Something bad!' in record['exception']


def test_asyncio():
    logger = logging.getLogger('Dummy')

    async def util():
        for i in range(3):
            logger.info('I am the util function', extra={'iteration': i+1})
            await asyncio.sleep(0)

    async def task(task_name: str):
        def inject_extra(record):
            record.extra['task_name'] = task_name
            record.extra['task_id'] = id(asyncio.Task.current_task())

        with Handler(bubble=True).contextbound():
            with Processor(inject_extra).contextbound():
                logger.info('I am the task')
                await asyncio.sleep(0)
                await util()
                logger.info('I am still the task')

    root_handler = TestHandler()
    root_handler.formatter = text_formatter
    with root_handler.applicationbound():
        with redirected_logging():
            asyncio.get_event_loop().run_until_complete(asyncio.gather(task('one'), task('two'), task('three')))

    records = root_handler.formatted_records
    assert 'INFO: Dummy: I am the task <task_name=one' in records[1]
    assert 'INFO: Dummy: I am the task <task_name=two' in records[2]
    assert 'INFO: Dummy: I am the task <task_name=three' in records[3]
    assert 'INFO: Dummy: I am the util function <iteration=1, task_name=one' in records[4]
    assert 'INFO: Dummy: I am the util function <iteration=1, task_name=two' in records[5]
    assert 'INFO: Dummy: I am the util function <iteration=1, task_name=three' in records[6]
    assert 'INFO: Dummy: I am the util function <iteration=2, task_name=one' in records[7]
    assert 'INFO: Dummy: I am the util function <iteration=2, task_name=two' in records[8]
    assert 'INFO: Dummy: I am the util function <iteration=2, task_name=three' in records[9]
    assert 'INFO: Dummy: I am the util function <iteration=3, task_name=one' in records[10]
    assert 'INFO: Dummy: I am the util function <iteration=3, task_name=two' in records[11]
    assert 'INFO: Dummy: I am the util function <iteration=3, task_name=three' in records[12]
    assert 'INFO: Dummy: I am still the task <task_name=one' in records[13]
    assert 'INFO: Dummy: I am still the task <task_name=two' in records[14]
    assert 'INFO: Dummy: I am still the task <task_name=three' in records[15]
