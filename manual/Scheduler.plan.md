# Observation Scheduler for SAGE Sky Survey

*Jie Zheng, 2016-07, Tucson* (_jiezheng(a)nao.cas.cn_)

----

## Files and directories structure

###Basic File Rules:

All angle in degrees, except ra/dec in observation list, it depends on telescope need, usually in sexagesimal hms/dms mode.

RunCode rule: in most case, use the month of the run starts, format yyyymm. If there are more runs in same month, add postfix A, B, or C.

Date rule: use extra modified Julian day, emjd = jd - 2450000.5, for observing, use the jd of local 18:00. In following, use `jdddd` to present leading `j` and 4-digit julian day.

Time rule: in most case, use hhmmss format time. In some case, will use decimal format, use `tttt` or `ttttt` to present.

Column seperator: if not specified, use space to seperate, First column left aligned, others right aligned for numerical and left or right for string.

* `/`
    + `programs`

* `/tel/` telescope name brief, currently we have `bok` and `xao`

* `/tel/conf/`
    + `basic.txt` site and telescope basic data, longitude, latitude, altitude, timezone, exposure accessory time, field of view.
    + `field.txt` list of all fields, col: field, ra, dec, gl, gb. Note: field id is **NOT** continual int, some will be skipped for future use.
    + `block.txt` list of all blocks, col: block field list(up to 7)
    + `expplan.txt` plan of exposures, col: code name filter expt repeat factor dither1 dither2
    + `expmode.txt` mode of exposures, col: filter expt code factor, use filter+expt to locate code and factor sum factor to check finished or not. Mode is a connection between real exposure and exposure plan.

* `/tel/obsed/yyyymm/` usually runcode is yyyymm, but can be others
    + `files.Jdddd.lst` daily file list, only good files, col: full filename
    + `check.Jdddd.lst` daily check list, col: filesn, imagetype, field/object, filter, exptime, ra, dec, filename
    + `obsed.Jdddd.lst` finished list of the day, col: field factorlist (by code)

* `/tel/schedule/runcode/jdddd/`
    + `plan.Jdddd.txt` merged plan of this day
    + `note.Jdddd.txt` note for plan. including field no, ra, dec, filter and exposure time, extra info including planned obsed time, alt and az, airmass, moon distance, alt and phase(even if moon is not visible), 
    + `snn.nnnnnn.txt` plan of one block, block sn, from 01, and block id
    + `snn.check.txt` check for choose one block, 
    + `plan.Jdddd.eps` footprint of finished and planed fields, color legend: black point(k,) planed but not observed (all fields will be displayed, blue dot(b.) obsed before last night, yellow dot(y.) obsed last night, red cross(rx) plan for this night.

## Programs

### list

Use `ls` to generage a file list: `/tel/obsed/runcode/files.xxx.lst`.

*Not a python program but a shell operation*

### check

Check file header info, from `files.xxx.lst` to `/tel/obsed/runcode/check.xxx.lst`, and `tel/obsed/runcode/obsed.xxx.lst`.

##### param
+ `tel`: string, telescope brief
+ `runcode`: string, yyyymm
+ `day`: 4-digit mjd of the night

### collect

Collect file info from daily check list and generate daily obsed list.

##### param
+ `tel`: string, telescope brief
+ `runcode`: string, yyyymm
+ `day`: 4-digit mjd of the night

*Divide check and collect into 2 steps, so we can `check` on server and then `collect` in any machine without fits. If we altered plan or mode, we do not need to scan fits again.*
 
### headerinfo

Extract info from fits file header, use this to adapt to different telescope.

##### param
+ `filename`: full filename
+ `return`: instance of file header info: filename, filesn, image/object type, object, filter, exposure time, ra (deg), dec (deg)

### footprint

Plot footprint map from obsed data, on a mollweide projected sky. It will generate a text report and two figure, in Equatorial and Galactic system. If specified run or day, then fields in the run or day will be red. If `before` set true, will obly draw fields before it.

##### param
+ `tel`: telescope, must provide
+ `reportfile`: text report filename. If not given, use current date and time. If given empty string, will not generate this report. Same rule for `equfile` and `galfile`.
+ `equfile`: filename of footprint in Equatorial system
+ `galfile`: filename of footprint in Galactic system
+ `runcode`: optional, if specified, only draw this run, else draw all
+ `day`: optional, if provided, only draw this day. If without runcode, this is ommitted
+ `plan`: specified which plan to be drawn, if not, all plan
+ `before`: optional, if set True, will only draw fields before specified day or run

### planner

Make plan of each day.

##### param
+ `tel`: string, telescope brief
+ `runcode`, string, yyyymm
+ `day`: 4-digit mjd

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

### util

Utilities for common usage.

##### function
+ dms2dec
+ hmd2dec
+ dec2hms
+ dec2dms
+ sxpar
+ progress_bar
+ read_conf

### schdutil

Utilities for scheduler.

##### function
+ load_expplan
+ load_expmode
+ class plan_info
+ class mode_info
+ class check_info
