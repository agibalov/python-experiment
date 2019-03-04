import datetime
import io
import json
import logging
import pythonjsonlogger.jsonlogger


def test_basic_output():
    stream = io.StringIO()
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(processName)-5s %(threadName)-5s %(name)-12s %(message)s")
    stream_handler = logging.StreamHandler(stream)
    stream_handler.setFormatter(formatter)

    root_logger = logging.RootLogger(logging.DEBUG)
    root_logger.addHandler(stream_handler)
    manager = logging.Manager(root_logger)

    logger = manager.getLogger("the-logger-1")
    logger.info("I am the log message n=%d m=%s", 123, "qwerty")

    assert "INFO     MainProcess MainThread the-logger-1 I am the log message n=123 m=qwerty\n" in stream.getvalue()


def test_my_json_output():
    stream = io.StringIO()
    formatter = MyJsonFormatter()
    stream_handler = logging.StreamHandler(stream)
    stream_handler.setFormatter(formatter)

    root_logger = logging.RootLogger(logging.DEBUG)
    root_logger.addHandler(stream_handler)
    manager = logging.Manager(root_logger)

    logger = manager.getLogger("the-logger-1")
    logger.info("I am the log message n=%d m=%s", 123, "qwerty", extra={
        'someExtra': 'hi there!'
    })

    obj = json.loads(stream.getvalue())
    assert obj['timestamp'] != ''
    assert obj['name'] == 'the-logger-1'
    assert obj['level'] == 'INFO'
    assert obj['message'] == 'I am the log message n=123 m=qwerty'
    assert obj['someExtra'] == 'hi there!'


def test_python_json_logger_json_output():
    stream = io.StringIO()
    formatter = MyPythonJsonLoggerFormatter("(timestamp) (name) (level) (message)")
    stream_handler = logging.StreamHandler(stream)
    stream_handler.setFormatter(formatter)

    root_logger = logging.RootLogger(logging.DEBUG)
    root_logger.addHandler(stream_handler)
    manager = logging.Manager(root_logger)

    logger = manager.getLogger("the-logger-1")
    logger.info("I am the log message n=%d m=%s", 123, "qwerty", extra={
        'someExtra': 'hi there!'
    })

    obj = json.loads(stream.getvalue())
    assert obj['timestamp'] != ''
    assert obj['name'] == 'the-logger-1'
    assert obj['level'] == 'INFO'
    assert obj['message'] == 'I am the log message n=123 m=qwerty'
    assert obj['someExtra'] == 'hi there!'


class MyJsonFormatter(object):
    def format(self, log_record: logging.LogRecord):
        extra = {key: value for (key, value) in log_record.__dict__.items() if key not in [
            'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
            'funcName', 'levelname', 'levelno', 'lineno', 'module',
            'msecs', 'message', 'msg', 'name', 'pathname', 'process',
            'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName']}

        return json.dumps({
            **{
                'name': log_record.name,
                'level': log_record.levelname,
                'message': log_record.getMessage(),
                'timestamp': datetime.datetime.fromtimestamp(log_record.created).astimezone().isoformat()
            },
            **extra
        })


class MyPythonJsonLoggerFormatter(pythonjsonlogger.jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record: logging.LogRecord, message_dict):
        super(MyPythonJsonLoggerFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.datetime.fromtimestamp(record.created).astimezone().isoformat()
        log_record['level'] = record.levelname
