# -*- coding: utf-8 -*-
"""
    2016-08-06, 2016M-1.0 lzj
    Utilities for pipeline, general operations
    Progress bar display and update.
"""


from sys import stdout as out


class progress_bar (object) :
    """ Display a progress bar in line, and overwrite it on next display
    """
    def __init__(self, value_init=0, value_step=1,
                 value_to=100, value_from=0, length=80,
                 format_percent="{:>6.1%}", format_value="{:>5d}",
                 char_brace=("[","]"), char_done="=", char_wait=" "):
        """ Init the progress bar
        args:
            value_init: progress bar initial value
            value_step: step value when call method step
            value_to: right end value of progress bar
            value_from: left end value of progress bar
            length: length of progress bar body, between bar brace
            format_percent: format of percent display, set None to suppress display
            format_value: format of value display, set None to suppress display
            char_brace: char of brace enclosing the bar, a 2-item tuple or list
            char_done: char of done part of progress bar, left part
            char_wait: char of waiting part of progress bar, right part
        """
        self._value = value_init
        self._value_step = value_step
        self._value_to = value_to
        self._value_from = value_from
        self._length = int(round(length))
        self._format_percent = format_percent
        self._format_value = format_value
        self._char_brace = char_brace
        self._char_done = char_done[0]
        self._char_wait = char_wait[0]

    def goto(self, value) :
        """ Walk the progress bar to specified value, and flush the display
        args:
            value: position of progress bar. If out of range, will display 0% or 100%
        """
        self._value = float(value)
        pcnt = (self._value - self._value_from) / (self._value_to - self._value_from)
        pcnt = 0.0 if pcnt < 0.0 else 1.0 if pcnt > 1.0 else pcnt
        len_done = int(round(pcnt * self._length))
        len_wait = self._length - len_done
        str_done = self._char_done * len_done
        str_wait = self._char_wait * len_wait

        if self._format_percent is not None:
            out.write(self._format_percent.format(pcnt))
        out.write(" {brace[0]}{str_done}{str_wait}{brace[1]} ".format(
            brace=self._char_brace, str_done=str_done, str_wait=str_wait))
        if self._format_value is not None:
            out.write(self._format_value.format(int(value)))
        out.write("\r")
        out.flush()

    def step(self, step=None) :
        """ Step the bar
        args:
            step: how much to add to current value, default is as set in init
        """
        if step is None : step = self._value_step
        self.goto(self._value+step)

    def clear(self) :
        """ Clear the progress bar. Use space to cover """
        out.write(" " * (self._length + 15) + "\r")
        out.flush()

    def end(self) :
        """ End this progress bar, keep bar status on previous line """
        out.write("\n")
        out.flush()

    def __repr__(self) :
        fmt = "ProgressBar ["+self._format_value+"] @ ("+self._format_value+"-->"+self._format_value+")"
        return fmt.format(self._value, self._value_from, self._value_to)

    @property
    def finished(self) :
        """ The progress bar is finished or not, go beyond value_to
        """
        if self._value_from < self._value_to :
            f = self._value >= self._value_to
        else :
            f = self._value <= self._value_to
        return f