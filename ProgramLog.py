import os
import time

class ProgramLog:
    def __init__(self, logfile):
        self.logfile = logfile

    def afferent(self, start, message):
        with open(self.logfile, "a+", encoding="utf-8") as fp:
            _time_ = time.strftime("[%Y-%m-%d %H:%M:%S]", time.gmtime())
            fp.write(f"[{_time_}] | [{start}]  |  [{message}]\n")
            fp.close()
        print(f"[{_time_}] | [{start}]  |  [{message}]")