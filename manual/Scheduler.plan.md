# Observation Scheduler for SAGE Sky Survey

*Jie Zheng, 2016-07, Tucson* (_jiezheng(a)nao.cas.cn_)

----

## Files and directories structure

All angle in degrees.

RunCode rule: in most case, use the month of the run starts, format yyyymm. If there are more runs in same month, add postfix A, B, or C.

Date rule: use extra modified Julian day, emjd = jd - 2450000.5, for observing, use the jd of local 18:00. In following, use `jdddd` to present leading `j` and 4-digit julian day.

Time rule: in most case, use hhmmss format time. In some case, will use decimal format, use `tttt` or `ttttt` to present.

* `/`
    + `programs`

* `/tel/` telescope name brief, currently we have `bok` and `xao`

* `/tel/conf/`
    + `basic.txt` site and telescope basic data, longitude, latitude, altitude, timezone, exposure accessory time, field of view. Each datum in one line.
    + `field.txt` list of all fields, col: field ra dec gb gl. Note: field id is **NOT** continual int, some will be skipped for future use.
    + `block.txt` list of all blocks, col: block field list(up to 7)
    + `expplan.txt` plan of exposures, col: code filter expt repeat
    + `expfactor.txt` factors of exp, col: filter expt code factor, use filter+expt to locate code and factor sum factor to check finished or not
    + `dither.txt` dither between exposures of the same filter

* `/tel/obsed/yyyymm/` usually runcode is yyyymm, but can be others
    + `files.jdddd.lst` daily file list, only good files, col: full filename
    + `check.jdddd.lst` daily check list, col: filename filesn field filter expt
    + `obsed.lst` finished list of this run, col: field factorlist (by code)
    + `obsed.jddddtttt.bak` backup of finished list, `ddddtttt` is the backup time

* `/tel/schedule/runcode/jdddd/`
    + `plan.jdddd.txt` merged plan of this day
    + `note.jdddd.txt` note for plan. including field no, ra, dec, filter and exposure time, extra info including planned obsed time, alt and az, airmass, moon distance, alt and phase(even if moon is not visible), 
    + `snn.nnnnnn.txt` plan of one block, block sn, from 01, and block id
    + `snn.check.txt` check for choose one block, 
    + `plan.jdddd.eps` footprint of finished and planed fields, color legend: black point(k,) planed but not observed (all fields will be displayed, blue dot(b.) obsed before last night, yellow dot(y.) obsed last night, red cross(rx) plan for this night.

## Programs

### list

Use `ls` to generage a file list: `/tel/obsed/runcode/files.xxx.lst`.

*Not a python program but a shell operation*

### check

Check file header info, from `files.xxx.lst` to `/tel/obsed/runcode/check.xxx.lst`.

##### param
+ runcode: string, yyyymm
+ day: 4-digit mjd of the night

### collect

Collect file info from daily check list and generate obsed list.

##### param
+ runcode: string, yyyymm
+ day: 4-digit mjd of the night
 
### headerinfo

Extract info from fits file header, use this to adapt to different telescope.

##### param
+ filename: full filename
+ return: tuple of file header info: filesn, object, filter, exposure time, ra, dec

### planner

Make plan of each day.

##### param
+ runcode, string, yyyymm
+ day: 4-digit mjd

1. Load all blocks and fields
2. Load finished fields
3. Remove finished fields, get new blocks
4. Calc JD and sidereal time of midnight, and moon position
5. Remove blocks with moon angle lt 90
6. Choose a best block
    + Get current JD and sidereal time
    + Calc azi and alt of all blocks, remove alt gt 80
    + Select min of dec * 0.5 + (90-alt)*0.5
7. Make a script for the block, and calculate time cost
8. Get new "current" time, if before dawn, goto 4
9. Ending work

