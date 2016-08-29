# -*- coding: utf-8 -*-
"""
    2016-08-06, 2016M-1.0 lzj
    Utilities for pipeline, general operations
    Class logger, providing a log printer and writer.
"""

import time


class logger (object) :
    """ A log writer, print message to screen and log file
        Only message with level not lower than debug level will be printed
    """
    def __init__(self, log_file=None, task=None, screen_level=0, file_level=7, show_time=True) :
        """ Init class, open file for print
        args:
            log_file: log filename, relative or absolute
            task: task name, printed to show different work
            screen_level: debug level to screen
            file_level: debug level to file
            show_time: show time in log lines or not
        """
        self._screen_level = screen_level
        self._file_level = file_level
        self._task = "" if task is None else task
        self._file = log_file
        if log_file is not None :
            self._f = open(log_file, "w")
        else :
            self._f = None
        self._start = time.time()
        self._show_time = show_time
        # log start time
        tstr = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self._start))
        self.write("{t} ===== {task} START >>>>> [{log}]".format(
            task=self._task, log=log_file, t=tstr), level=-1, show_time=False)

    def __del__(self) :
        self.close()

    def close(self) :
        """ Close logger """
        if self._f is not None : # prevent close again
            # log finish time
            t_now = time.time()
            t_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t_now))
            t_span = t_now - self._start
            self.write("{t} ===== {task} FINISH <<<<< {s:.1f} sec".format(
                task=self._task, t=t_str, s=t_span), level=-1, show_time=False)
            # close file
            self._f.close()
            self._f = None

    def timespan(self) :
        """ Get time span from start, in seconds"""
        return time.time() - self._start

    def write(self, msg, level=0, show_time=None):
        """ Write log, to screen and log file
        args:
            msg: message, if is multi-line, use array like object (ndarray, list, tuple)
            level: level of message
            show_time: if true, current time (no date) will be displayed
                       before content in log file, if None, use init default
        """
        if show_time is None : show_time = self._show_time
        t = time.strftime("%H:%M:%S | ", time.gmtime()) if show_time else ""
        if type(msg) == str : msg = [msg]
        for m in msg :
            if self._f is not None and level <= self._file_level :
                self._f.write(t + m + "\n")
            if level <= self._screen_level :
                print (m)


    def __repr__(self) :
        return ("{t} Logger to <{f}>, level {s}&{d}".format(
            t=self._task, f=self._file, d=self._file_level, s=self._screen_level))
