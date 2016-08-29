# -*- coding: utf-8 -*-
"""
    This is version 2016M of pipeline for sage sky survey.
    Rewrite using python, original version using IDL
    This file is for commandline arguments process.

    Author: Jie ZHENG: jiezheng@nao.cas.cn
    Version: 2016M (M for 2nd half of June)
    Location: Steward Observatory, University of Arizona, Tucson, AZ
"""


import sys
from math import isnan


def _isempty(v) :
    """ A private function check whether v is empty
        Empty value can be: None, or int maxsize, or float nan, or empty string
    """
    return (v is None or
        (type(v) is int and v == sys.maxsize) or
        (type(v) is float and isnan(v)) or
        (type(v) is str and v == "") )


def arg_trans (argv, default=None, restrict=True, silent=False, alias=None):
    """ A function reduce commandline arguments.
        Recognize them into two categories: arguments by order and by name.
        Directly arguments will be taken as ordered arguments, will be entitled as arg_01, arg_02, etc.
        Arguments like key=value will taken as named arguments, reuse its own name.
        The default key=value dict will provide missing arguments.
        If restrict is true, only names in default is valid, other names will be abandoned.
        Note: NOT use arg_xx as keyword for named arguments.
    args:
        argv: argument values from `sys.argv`
        default: providing default key-value dict, value None means this parameter is required
        restrict: bool, restrict names in default or not. If default is None, this will not effect.
        silent: display error message or not
        alias: a dict for alias of parameters, a=b for a is alias of b
    returns:
        dict of these arguments
    """
    # function arguments check
    if default is None :
        res = {}
        restrict = False  # if default is None, this argument is meaningless
    else :
        res = default.copy()
    if alias is None :
        alias = {}

    arg_cnt = 0
    for a in argv :
        kv = a.split("=")
        if len(kv) == 1 :
            # serial no of unnamed parameter
            k = "arg_{:02d}".format(arg_cnt)
            arg_cnt += 1
            v = kv[0]
        else :
            k = kv[0].lower()
            v = kv[1]
        # check parameter name alias
        if k in alias : k = alias[k]
        # check restrict name require
        if not restrict or k in res :
            if k in res :
                if type(res[k]) is int :
                    v = int(v)
                elif type(res[k]) is float :
                    v = float(v)
                elif type(res[k]) is bool :
                    v = v.lower().startswith("t") or v == ""

            res[k] = v
        else :
            if not silent : print ("Argument `{}` NOT recognized.".format(k))

    # check required but missing field, only check, no further action
    if not silent :
        for k in res :
            if _isempty(res[k]) :
                print ("Argument `{}` required but missing.".format(k))

    return res

