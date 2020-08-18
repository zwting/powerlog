# -*- coding: utf-8 -*-
import logging, logging.handlers
from collections import deque
from time import sleep

from src.controller.log_client import PowerLogSockHandler

rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.DEBUG)
# socketHandler = logging.handlers.SocketHandler('localhost',
#                                                logging.handlers.DEFAULT_TCP_LOGGING_PORT)
def remote_handler(cmd):
    print cmd
socketHandler = PowerLogSockHandler('localhost', logging.handlers.DEFAULT_TCP_LOGGING_PORT, remote_handler)
# don't bother with a formatter, since a socket handler sends the event as
# an unformatted pickle
rootLogger.addHandler(socketHandler)

# Now, we can log to the root logger, or any other logger. First the root...
logging.info('Jackdaws love my big sphinx of quartz.')

# Now, define a couple of other loggers which might represent areas in your
# application:

logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')

logger1.debug('Quick zephyrs blow, vexing daft Jim.')
logger1.info('How quickly daft jumping zebras vex.How quickly daft jumping zebras vex.How quickly daft jumping zebras vex.How quickly daft jumping zebras vex.How quickly daft jumping zebras vex.')
logger2.warning('Jail zesty vixen who grabbed pay from quack.')
logger2.error('The five boxing wizards jump quickly.')

import time
while True:
    socketHandler.try_receive()
    sleep( 1.0 / 60)
    logger1.info("你好"* 50)
    print time.time()
