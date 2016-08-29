# -*- coding: utf-8 -*-
"""
    2016-08-06, 2016M-1.0 lzj
    Utilities for pipeline, general operations
    Class info, providing a structure like class, it also base of similar class.
"""


class info (object) :
    """ A class like struct, just info container
    """
    def __init__(self, name, **kwargs) :
        self.__dict__ = kwargs
        self._name = name

    def __repr__(self) :
        res = "Info of `{name}`:\n".format(name=self._name)
        for k in self.__dict__ :
            res += "{key} = {value}\n".format(key=k, value=self.__dict__[k])
        return res
