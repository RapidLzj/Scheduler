#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Module makeblock : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    Make blocks from fields. Need to be run only once.
"""

import numpy as np


def makeblock ( tel, blocksize ) :
    """ make block from field
    Input file: field.bare.txt, col: id ra dec gl gb
    Output file: field.txt, col: id ra dec gl gb blockname
    Block name rule: 3 digit dec `round(dec * 10)`, 4 digit ra `round(radeg * 10)`
    Continual n fields will be a block. n = blocksize
    """
    # field files
    barefile = "{tel}/conf/field.bare.txt".format(tel=tel)
    outfile = "{tel}/conf/field.txt".format(tel=tel)

    # load bare fields
    bare = np.loadtxt(barefile)
    block = [""] * bare.shape[0]

    # make a key: dec*400+ra, and sort
    dera = np.round(bare[:,2], 1) * 500 + bare[:,1]
    ixsort = dera.argsort()

    # one by one scan, and split block
    lastra, lastde = -99.99, -99.99
    blockix = []
    for ix in ixsort :
        if len(blockix) >= blocksize or bare[ix, 2] != lastde or bare[ix, 1] - lastra > 5.0 :
            # end previous block
            blockde = np.median(bare[blockix, 2]) if len(blockix) > 0 else -9.9
            blockra = np.median(bare[blockix, 1]) if len(blockix) > 0 else -9.9
            blockname = "{:03d}{:04d}".format(int(round(blockde*10)), int(round(blockra*10)))
            for i in blockix :
                block[i] = blockname
            # open a new block
            blockix = []
        blockix.append(ix)
        lastra, lastde = bare[ix, 1], bare[ix, 2]
    # end the final block
    blockde = np.median(bare[blockix, 2]) if len(blockix) > 0 else -9.9
    blockra = np.median(bare[blockix, 1]) if len(blockix) > 0 else -9.9
    blockname = "{:03d}{:04d}".format(int(round(blockde*10)), int(round(blockra*10)))
    for i in blockix :
        block[i] = blockname

    # output to new list
    fmt = "{:<5d} {:>10.6f} {:>10.6f} {:>6.2f} {:>6.2f} {:7s}\n".format
    with open(outfile, "w") as f :
        for ix in ixsort :
            f.write(fmt(int(bare[ix, 0]), bare[ix, 1], bare[ix, 2], bare[ix, 3], bare[ix, 4], block[ix]))
    #f.close()


if __name__ == "__main__" :
    makeblock("xao", 5)