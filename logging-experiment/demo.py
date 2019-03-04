import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(processName)-5s %(threadName)-5s %(name)-12s %(message)s",
    level=logging.DEBUG)

logger = logging.getLogger("my-logger1")
logger.debug("hello world")
logger.info("hello world")
logger.warning("hello world")
logger.error("hello world")
logger.critical("hello world")
logger.info("hi there number is %d string is %s", 123, "qwerty")

child_logger = logger.getChild("child1")
child_logger.info("hi there!")
