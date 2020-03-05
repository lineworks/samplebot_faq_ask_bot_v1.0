#!/bin/env python
# -*- encoding: utf-8 -*-

# from gevent import monkey
# monkey.patch_all()
"""
main function for faq_bot
"""
import signal
from daemonize import Daemonize
from tornado.options import define, options
from faq_bot.faq_bot import *
from faq_bot.settings import *


define("daemonize", default=False, help="daemon mode")
define("pidfile", default=CALENDAR_PID_FILE,
       help="the path of pid file, default None")


if __name__ == "__main__":
    options.parse_command_line()

    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGQUIT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGHUP, sig_handler)

    if options.daemonize:
        daemon = Daemonize(app="faq_bot", action=start_faq_bot,
                           pid=options.pidfile)
        daemon.start()
    else:
        start_faq_bot()
