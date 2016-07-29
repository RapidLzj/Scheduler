#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Module takeoff : part of SAGE Digital Sky Survey Observation Scheduler
    v 1.0 : By Jie Zheng, 201607, Tucson, AZ, USA

    Most important module in this system. This is the main schedule maker.
"""


import os
import sys
import numpy as np
from astropy.time import Time
import astropy.coordinates
from myPyLib.Mollweide import moll
from matplotlib import pyplot as plt
import util
import schdutil
import moon
import plotmap
import collect


def tea ( rep_file, rep_info ) :
    """ write info to both screen and report file
    args:
        rep_file: file handler of report file
        rep_info: text to be write
    """
    rep_file.write(rep_info + "\n")
    print (rep_info)


def takeoff ( tel, yr, mn, dy, run=None,
              obs_begin=None, obs_end=None,
              moon_dis_limit=50.0,
              airmass_limit = 1.75,
              ha_limit = 4.0,
              overwrite=False, simulate=False, check=False ) :
    """ Generate observation script
    args:
        tel: telescope code
        yr: year of obs date, 4-digit year
        mn: year of obs date, 1 to 12
        dy: day of obs date, 0 to 31, or extended
        run: run code, default is `yyyymm`
        obs_begin: obs begin hour, float, default 1.25 hours after sunset
        obs_end, obs end hour, float, default, 1.25 hours before sunrise
        moon_dis_limit: limit of distance of good field to the moon, default 50 deg
        airmass_limit: limit of airmass, default 1.75, but for pole area, this should be greater
        ha_limit: limit of hour angle, default 3.0, should be greater for pole area
        overwrite: bool, when output dir already exists, overwrite or not
        simulate: bool, generate a obsed list or not
        check: bool, if check is true, will report for each block's selection
    """

	# all var starts with `rep_` contains report info
    rep_start_time = Time.now()

    # load site and telescope basic data
    site = schdutil.load_basic(tel)

    # airmass lower limit, set this to avoid zenith
    airmass_lbound = 1.005  # about 84 deg

    # night parameters
    # mjd of 18:00 of site timezone, as code of tonight
    mjd18 = schdutil.mjd_of_night(yr, mn, dy, site)
    # mjd of local midnight, as calculate center
    mjd24 = schdutil.mjd(yr, mn, dy, 24 - site.lon / 15.0, 0, 0,  0)
    tmjd24 = Time(mjd24, format="mjd")
    # night length (hour)
    night_len = schdutil.night_len(mjd24, site.lat)
    dark_len = night_len - 2.5  # assume twilight 1.25 hours
    # local sidereal time of midnight
    lst24 = schdutil.fmst (yr, mn, dy, site.lon)
    #lst24 = tmjd24.sidereal_time("mean", site.lon).hour
    # timezone correction: between local time and timezone standard time
    tzcorr = site.tz - site.lon / 15.0
    # observation start and end time, in timezone time
    sunset_time, sunrise_time = 24 + tzcorr - night_len / 2, 24 + tzcorr + night_len / 2
    # if obs time is given, use given time
    if obs_begin is None :
        obs_begin = 24 + tzcorr - dark_len / 2
    else :
        if obs_begin < 12.0 : obs_begin += 24
    if obs_end is None :
        obs_end = 24 + tzcorr + dark_len / 2
    else :
        if obs_end < 12.0 : obs_end += 24
    # moon position at midnight, as mean coord to calculate moon-object distance
    mpos = moon.moon_pos(mjd24) #astropy.coordinates.get_moon(tmjd24)
    mphase = moon.moon_phase(mjd24)
    # sun position at midnight
    spos = moon.sun_pos(mjd24) #astropy.coordinates.get_sun(tmjd24)

    ######################################################################################

    # default run name rule
    if run is None :
        run = "{year:04d}{month:02d}".format(year=yr, month=mn)
    daystr = "{year:04d}.{month:02d}.{day:02d}".format(year=yr, month=mn, day=dy)
    # schedule dir
    daypath = "{tel}/schedule/{run}/J{mjd:0>4d}/".format(tel=tel, run=run, mjd=mjd18)
    if os.path.isdir(daypath) :
        if not overwrite :
            print (util.msgbox(["Schedule dir already exists.",
                                "If you want to overwrite, please set `overwrite=True`"],
                                title="ERROR", border="*"))
            return
    os.system("mkdir -p " + daypath)
    if not os.path.isdir(daypath) :
        print (util.msgbox("Can NOT make schedule dir `{}`".format(daypath),
                           title="ERROR", border="*"))

    ######################################################################################

    # output filename or filename format
    rep_fn  = "{path}report.{mjd:04}.{days}.txt"  .format(path=daypath, mjd=mjd18, days=daystr)
    sumb_fn = "{path}sumblock.{mjd:04}.{days}.txt".format(path=daypath, mjd=mjd18, days=daystr)
    sumf_fn = "{path}sumfield.{mjd:04}.{days}.txt".format(path=daypath, mjd=mjd18, days=daystr)
    plan_fn = "{path}plan.{mjd:04}.{days}.txt"    .format(path=daypath, mjd=mjd18, days=daystr)
    eps_fn  = "{path}plan.{mjd:04}.{days}.eps"    .format(path=daypath, mjd=mjd18, days=daystr)
    png_fn  = "{path}plan.{mjd:04}.{days}.png"    .format(path=daypath, mjd=mjd18, days=daystr)
    chk_fn_fmt = "{path}chk.{mjd:04}.{sn:02}.{bname}.txt".format
    see_fn_fmt = "{path}see.{mjd:04}.{sn:02}.{bname}.png".format
    scr_fn_fmt = "{path}scr.{mjd:04}.{sn:02}.{bname}.txt".format

    rep_f = open(rep_fn, "w")
    tea(rep_f, "        --------========  Start : {}  ========--------\n".format(rep_start_time.iso))

    # load fields and plan
    plans  = schdutil.load_expplan(tel)
    fields = schdutil.load_field(tel)
    active_plans = {p:plans[p] for p in plans if plans[p].active}

    # find all obsed file, and mark them
    obsedlist = schdutil.ls_files("{tel}/obsed/*/obsed.J*.lst".format(tel=tel))
    schdutil.load_obsed(fields, obsedlist, plans)
    afields = np.array(fields.values())
    ara = np.array([f.ra for f in afields])
    ade = np.array([f.de for f in afields])

    # mark fields near moon and sun
    moon_dis = moon.distance(mpos.ra, mpos.dec, ara, ade)
    for f in afields[np.where(moon_dis < moon_dis_limit)]:
        f.tag |= 0x10
    sun_dis = moon.distance(spos.ra, spos.dec, ara, ade)
    for f in afields[np.where(sun_dis < 60)]:
        f.tag |= 0x10
    atag = np.array([f.tag for f in afields])

    # keep only unfinished fields, and must away from moon
    newfield = afields[np.where(atag <= 1)]

    # count histogram
    n_tag = len(afields)
    n_tag_01 = sum((atag == 0x00) | (atag == 0x01))
    n_tag_2  = sum((atag == 0x02) | (atag == 0x12))
    n_tag_10 = sum((atag == 0x10) | (atag == 0x11))

    # blocks and unique blocks
    newfieldblock = np.array([f.bk for f in newfield])
    newblockset = set(newfieldblock)
    n_block = len(newblockset)

    # block parameter
    newblock = {}
    for b in newblockset :
        f_in_b = newfield[np.where(newfieldblock == b)]
        newblock[b] = schdutil.block_info(b, f_in_b)

    # show prepare message
    tea(rep_f, util.msgbox([
        "## {tel}, on {days} (J{mjd:04}) of run {run}".
            format(tel=tel,days=daystr,mjd=mjd18, run=run),
        "Sun set at {s:5}, rise at {r:5}, obs time is {os:5} ==> {oe:5}".
            format( s=util.hour2str(sunset_time),  r=util.hour2str(sunrise_time-24.0),
                   os=util.hour2str(obs_begin), oe=util.hour2str(obs_end-24.0)),
        "Obs hours is {ol:5}, LST of midnight is {mst:5}".
            format(ol=util.hour2str(obs_end-obs_begin), mst=util.hour2str(lst24)),
        "Moon mean position is {ra:11} {de:11}, phase is {ph:4.1%}".
            format(ra=util.dec2hms(mpos.ra), de=util.dec2dms(mpos.dec), ph=mphase),
        ("Simulation included" if simulate else "No simulation"),],
        title="Night General Info", align="^<<<>"))
    tea(rep_f, util.msgbox([
        "{:<20} {:>5}       {:26}".       format("All Fields",        n_tag,""),
        "{:<20} {:>5}   |   {:<20} {:>5}".format("x: Finished",       n_tag_2,
                                                 "x: Near Moon/Sun",  n_tag_10),
        "{:<20} {:>5}   |   {:<20} {:>5}".format("Available Fields",  n_tag_01,
                                                 "Available Blocks",  n_block) ],
        title="Fields Count", align="^^"))

    ######################################################################################

    # start to make schedule
    clock_now = obs_begin
    lst_clock = lambda c : (lst24 + c) % 24.0  # lst of start, use lst_clock(clock_now) to call this

    tea(rep_f, "Begin to schedule from {clock}, LST {lst}\n".format(
        clock=util.hour2str(clock_now), lst=util.hour2str(lst_clock(clock_now))))

    # define a lambda rank function
    rank = lambda aa : aa.argsort().argsort()

    # simulation working
    if simulate :
        simu_path = "{tel}/obsed/{run}/".format(tel=tel, run=run)
        os.system("mkdir -p " + simu_path)
        simu_check_fn = simu_path + "check.J{mjd:04d}.lst".format(mjd=mjd18)
        sim_f = open(simu_check_fn, "w")
        tea(rep_f, "Simulation file: " + simu_check_fn)

    # format of output
    rep_tit = "{sn:2}   {bn:^7} ({ra:^9} {de:^9}) {airm:4} @ {clock:5} [{lst:^5}] {btime:>5}".format(
        sn="No", bn="Block", ra="RA", de="Dec", airm="Airm", clock="Time", lst="LST", btime="Cost")
    rep_fmt = "{sn:02}: #{bn:7} ({ra:9.5f} {de:+9.5f}) {airm:4.2f} @ {clock:5} [{lst:5}] {btime:>4d}s".format
    rep_war = "**:  {skip:>7} minutes SKIPPED !! {skipbegin:5} ==> {clock:5} [{lst:5}]".format

    sum_tit = "#{mjd:3} {clock:5} {sn:>2} {bn:^7} {ra:^9} {de:^9} {airm:4} {lst:^5} {btime:>4}\n".format(
        mjd="MJD", clock="Time", sn="No", bn="Object", ra="RA", de="Dec", airm="Airm", lst="LST", btime="Cost")
    sum_fmt = "{mjd:04d} {clock:5s} {sn:02d} {bn:7} {ra:9.5f} {de:+9.5f} {airm:4.2f} {lst:5s} {btime:>4d}\n".format

    chk_fmt = "{ord:03d} {bn:7s} ({ra:9.5f} {de:+9.5f}) {airm:4.2f} {ha:5.2f} {key:>5.1f} {other}\n".format
    chk_tit = "#{ord:>2} {bn:^7} ({ra:>9} {de:>9}) {airm:>4} {ha:5} {key:>5} {other}\n".format(
                ord="No",bn="Block", ra="RA", de="Dec", airm="Airm", ha="HA", key="Key", other="Other")

    scr_fmt = (site.fmt + "\n").format

    tea(rep_f, rep_tit)
    sumb_f = open(sumb_fn, "w")
    sumf_f = open(sumf_fn, "w")
    plan_f = open(plan_fn, "w")
    sumb_f.write(sum_tit)
    sumf_f.write(sum_tit)

    # init before loop
    block_sn = 0  # block sn, count blocks, and also for output
    skip_begin = None # time begin to skip, when no good block available
    span_skip = 1.0 / 60.0 # how long skipped each loop
    skip_count = 0
    skip_total = 0.0
    exp_airmass = [] # collect airmass
    lra, lde = 999.99, 99.99 # last field ra, dec
    # time need of a full round for a field
    plan_time = sum([(plans[p].expt + site.inter) * plans[p].repeat for p in active_plans]) / 3600.0

    ######################################################################################
    while clock_now < obs_end :
        lst_now = lst_clock(clock_now)

        if len(newblock) == 0 :
            # no available block, print error message, and end procedure
            skip_begin = clock_now
            break

        bra = np.array([b.ra for b in newblock.values()])
        bde = np.array([b.de for b in newblock.values()])
        bsize = np.array([len(b.fields) for b in newblock.values()])
        bname = np.array(newblock.keys())

        # assume all fields need a full round, this is estimated center lst
        blst = lst_now + plan_time * bsize / 2.0
        # calculate airmass for all available block
        ha = util.angle_dis(blst * 15.0, bra) / 15.0
        airm = schdutil.airmass(site.lat, blst, bra, bde)

        # keep blocks with airm < airmlimit & hour angle < ha_limit, and then dec < min dec + 4 deg
        ix_1 = np.where((airm < airmass_limit) & (airm > airmass_lbound) & (np.abs(ha) < ha_limit))
        # no available block handler
        if len(ix_1[0]) == 0 :
            # no good block, have bad block
            # maybe not good time, skip 5 min and check again
            # set skip mark, if found new block, print warning for skipped time
            if skip_begin is None : skip_begin = clock_now
            clock_now += span_skip
            continue
        elif skip_begin is not None :
            # found good block, but before this, some time skipped, print a warning
            tea(rep_f, rep_war( skip=int((clock_now - skip_begin) * 60),
                skipbegin=util.hour2str(skip_begin),
                clock=util.hour2str(clock_now), lst=util.hour2str(lst_now) ))
            sum_f.write(sum_fmt(mjd=mjd18, clock=util.hour2str(skip_begin), sn=0,
                bn="SKIP!!!", ra=0.0, de=0.0, airm=0.0,
                lst=util.hour2str(lst_now), btime=int(int((clock_now - skip_begin) * 3600)) ))
            skip_count += 1
            skip_total += clock_now - skip_begin
            skip_begin = None

        # add 2nd condition, dec <= min dec + 4
        ix_2 = np.where((airm < airmass_limit) & (airm > airmass_lbound) & (np.abs(ha) < ha_limit) &
                        (bde <= bde[ix_1].min() + 4.0))

        # make key for each block, key = airmass rank + ra rank + de rank
        airm_2, ha_2 = airm[ix_2], ha[ix_2]
        bra_2, bde_2, bname_2 = bra[ix_2], bde[ix_2], bname[ix_2]
        # key formular is MOST important
        #if lst_now < 5.0 or 19.0 < lst_now :  # use ha instead of ra, ha is already 360 moded
        #    bra_2[np.where(bra_2 > 180.0)] -= 360.0
        #key_2 = rank(airm_2) + rank(bra_2) + rank(bde_2)
        key_2 = rank(airm_2) + rank(-ha_2) + rank(bde_2)
        # choose the best block
        ix_best = key_2.argmin() # the best block
        bname_best = bname_2[ix_best]
        block_best = newblock[bname_best]
        # inc sn
        block_sn += 1
        # mark candidate blocks, just for check plot
        for b in bname_2 :
            for f in newblock[b].fields :
                f.tag |= 0x04
        # mark fields in selected block
        for f in block_best.fields :
            f.tag = 0x07  # use this code, when clean candidate, it will be back to 3

        # generate a check file about selection
        if check :
            # check file, list blocks: name, ra, dec, fields, airmass, rank
            chk_fn = chk_fn_fmt(path=daypath, mjd=mjd18, sn=block_sn, bname=bname_best)
            with open(chk_fn, "w") as chk_f :
                chk_f.write(chk_tit)
                i = 0
                for s in key_2.argsort() :
                    i += 1
                    b = newblock[bname_2[s]]
                    chk_f.write(chk_fmt(ord=i, bn=b.bname, ra=b.ra, de=b.de, airm=airm_2[s], ha=ha_2[s], key=key_2[s], other="*"))
                #for b in range(len(newblock)) :
                #    chk_f.write(chk_fmt(ord=0, bn=bname[b], ra=bra[b], de=bde[b],
                #        airm=airm[b], ha=ha[b], key=0.0, other="*" if b in ix_2[0] else " "))

            # plot a check map
            plotmap.plotmap(ara, ade, np.array([f.tag for f in afields]),
                title=tel+" "+daystr+" "+util.hour2str(clock_now),
                pngfile=see_fn_fmt(path=daypath, mjd=mjd18, sn=block_sn, bname=bname_best),
                mpos=(mpos.ra, mpos.dec),
                spos=(spos.ra, spos.dec),
                zenith=(lst_now * 15.0, site.lat) )

        # clear candidate
        for b in bname_2 :
            for f in newblock[b].fields :
                f.tag &= 0x03

        # script file, using format from configuration
        scr_fn = scr_fn_fmt(path=daypath, mjd=mjd18, sn=block_sn, bname=bname_best)
        block_time = 0  # time cost for this block, in seconds
        with open(scr_fn, "w") as scr_f :
            # script: plan loop, field loop, do only factor < 1
            for p in active_plans :
                for f in block_best.fields :
                    factor_work = 1.0 - f.factor[p]
                    nrepeat = int(np.ceil(factor_work / plans[p].factor))
                    for i in range(nrepeat) :
                        if max(abs(util.angle_dis(lra, f.ra)), abs(lde - f.de)) > 15 :
                            plan_f.write("\n") # a mark about big move, for bok not for xao
                        scr = scr_fmt(e=schdutil.exposure_info.make(plans[p], f))
                        scr_f.write(scr)
                        plan_f.write(scr)
                        if simulate :
                            sim_f.write("{}\n".format(schdutil.check_info.simulate(plans[p], f)))
                        block_time += plans[p].expt + site.inter
                        clock_field = clock_now + block_time / 3600.0
                        am = f.airmass(site.lat, lst_clock(clock_field))
                        exp_airmass.append(am)
                        sumf_f.write(sum_fmt(mjd=mjd18, clock=util.hour2str(clock_field), sn=block_sn,
                            bn=f.id, ra=f.ra, de=f.de, airm=am,
                            lst=util.hour2str(lst_clock(clock_field)), btime=int(plans[p].expt + site.inter) ))
        plan_f.write("\n")  # write a blank line to seperate blocks

        # report & summary
        tea(rep_f, rep_fmt( sn=block_sn,
            bn=bname_best, ra=block_best.ra, de=block_best.de, airm=airm_2[ix_best],
            clock=util.hour2str(clock_now), lst=util.hour2str(lst_now), btime=int(block_time) ))
        sumb_f.write(sum_fmt(mjd=mjd18, clock=util.hour2str(clock_now), sn=block_sn,
            bn=bname_best, ra=block_best.ra, de=block_best.de, airm=airm_2[ix_best],
            lst=util.hour2str(lst_now), btime=int(block_time) ))

        # remove used block from newblock
        del newblock[bname_best]
        # clock forward
        clock_now += block_time / 3600.0

    # handle event: in last time no block available
    if skip_begin is not None :
        # found good block, but before this, some time skipped, print a warning
        tea(rep_f, rep_war( skip=int((clock_now - skip_begin) * 60),
            skipbegin=util.hour2str(skip_begin),
            clock=util.hour2str(clock_now), lst=util.hour2str(lst_clock(clock_now)) ))
        sum_f.write(sum_fmt(mjd=mjd18, clock=util.hour2str(skip_begin), sn=0,
            bn="SKIP!!!", ra=0.0, de=0.0, airm=0.0,
            lst=util.hour2str(lst_clock(clock_now)), btime=int(int((clock_now - skip_begin) * 3600)) ))
        skip_count += 1
        skip_total += clock_now - skip_begin
        skip_begin = None

    ######################################################################################

    sumb_f.close()
    sumf_f.close()
    if simulate:
        sim_f.close()

    # total of schedule
    tea(rep_f, util.msgbox([
        "Total {b} blocks, {e} exposures, {t} costed. From {s} to {f}".format(
            b=block_sn, e=len(exp_airmass), t=util.hour2str(clock_now-obs_begin),
            s=util.hour2str(obs_begin), f=util.hour2str(clock_now)),
        "Estimate airmass: {me:5.3f}+-{st:5.3f}, range: {mi:4.2f} -> {ma:4.2f}".format(
            me=np.mean(exp_airmass), st=np.std(exp_airmass),
            mi=np.min(exp_airmass), ma=np.max(exp_airmass)),
        "SKIP: {sc} sessions encounted, {st} time wasted.".format(
            sc=skip_count, st=util.hour2str(skip_total)) ],
        title="Summary") )

    # plot task map of this night
    plotmap.plotmap(ara, ade, np.array([f.tag for f in afields]),
        title="{tel} {days} ({mjd})".format(tel=tel, days=daystr, mjd=mjd18),
        epsfile=eps_fn,
        pngfile=png_fn,
        mpos=(mpos.ra, mpos.dec),
        spos=(spos.ra, spos.dec) )

    # closing report and summary
    rep_end_time = Time.now()
    tea(rep_f, "\n        --------========  End : {}  ========--------\n{:.1f} seconds used.\n".format(
        rep_end_time.iso, (rep_end_time - rep_start_time).sec))
    rep_f.close()

    # call collect to finish simulation
    if simulate :
        collect.collect(tel, yr, mn, dy, run)


###############################################################################

if __name__ == "__main__" :
    if len(sys.argv) < 4 :
        print ("""Syntax:
    python takeoff.py tel year month day [run] [overwrite] [simulate] [check]
        tel: 3 letter code of telescope, we now have bok and xao
        year: 4 digit year
        month: month, 1-12
        day: day, 1-31, or extented
        run: code of run, if not yyyymm format
        overwrite: anything to present overwrite
        simulate: simulate observation results
        check: generate check files
    """)
    else :
        ov, si, ch = False, False, False
        for a in sys.argv :
            if a.lower().startswith("over") :
                ov = True
            elif a.lower().startswith("simu") :
                si = True
            elif a.lower().startswith("check") :
                ch = True
        if len(sys.argv) > 5 :
            run = sys.argv[5]
        else :
            run = None
        takeoff(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), run,
                overwrite=ov, simulate=si, check=ch)
