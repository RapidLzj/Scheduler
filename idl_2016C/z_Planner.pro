pro z_Planner, yr, mn, dy, time0, time1, runcode, $
	moonanglelimit=moonanglelimit, $
	overwrite=overwrite, backup=backup, $
	silent=silent, $
	simulate=simulate

	@z_Planner_load

	;1. Load all blocks and fields, and exp plan
	;2. Load finished fields
	;3. Remove finished fields, get new blocks
	;4. Calc JD and sidereal time of midnight, and moon position
	;5. Remove blocks with moon angle lt 90
	;6. Choose a best block
	;   Algorithm for choose best
	;     Get current JD and sidereal time
	;     Calc azi and alt of all blocks, remove alt gt 80
	;     Select min of dec * 0.5 + (90-alt)*0.5
	;7. Make a script for the block, and calculate time cost
	;8. Get new "current" time, if before end time, goto 4
	;9. Ending work

	; make summary and report field count info
	file_mkdir, daypath
	openw, 77, daypath+'/summary_'+days+'.txt'
	printf, 77, runcode, days, time0, time1, format='("RUN ",A,"  DATE ",A, "  TIME ",A," --> ",A)'
	printf, 77, horline
	;2. Load finished fields
	;3. Find unfinished fields
	newfield = zj_loadunobsed(field, plan, nnew, silent=silent)
	ix = where(field.status eq 9, nskipped)
	ix = where(field.status eq 2, nfinished)
	ix = where(field.status eq 1, npartly)
	ix = where(field.status eq 0, nnew)


	print, nfield, nskipped, nfinished, npartly, nnew, $
		format='(I5," fields, ",I5," skipped, ",I5," finished,",I5," partly finished, ",I5," new")'
	printf, 77, nfield, nskipped, nfinished, npartly, nnew, $
		format='(I5," fields, ",I5," skipped, ",I5," finished,",I5," partly finished, ",I5," new")'
	print, horline
	printf, 77, horline

	; Calc JD of midnight, and moon/sun position
	jd = julday(mn, dy, yr, 24 - site_lon/15.0, 0, 0)
	moonpos, jd, mra, mdec
	mphase, jd, mph
	sunpos, jd, sra, sdec
	print, zj_radec2str(mra, mdec), mph*100.0, format='("Midnight Moon Coord: ",A,2x,A, "  Moon Phase: ", F5.1,"%")'
	printf, 77, zj_radec2str(mra, mdec), mph*100.0, format='("Midnight Moon Coord: ",A,2x,A, "  Moon Phase: ", F5.1,"%")'
	if ~keyword_set(moonanglelimit) then begin
		moonanglelimit = sin(mph * !pi / 2.0) * 60.0 + 10.0
		print, moonanglelimit, format='("Moon-star distance limit is default as ",F5.1)'
		printf, 77, moonanglelimit, format='("Moon-star distance limit is default as ",F5.1)'
	endif else begin
		print, moonanglelimit, format='("Moon-star distance limit is set as ",F5.1)'
		printf, 77, moonanglelimit, format='("Moon-star distance limit is set as ",F5.1)'
	endelse


	; Remove fields with moon angle < limit
	mangle = fltarr(nnew)
	for ff = 0, nnew-1 do mangle[ff] = (map_2points(mra, mdec, newfield[ff].ra, newfield[ff].dec))[0]
	ix = where(mangle le moonanglelimit, nix)
	print, nix, format='(I5," fields removed, too close to the Moon")'
	printf, 77, nix, format='(I5," fields removed, too close to the Moon")'
	if nix gt 0 then begin
		match, field.id, newfield[ix].id, ixf, ixn
		field[ixf].status = 8 ; removed
	endif
	ix = where(mangle gt moonanglelimit, nix)
	if nix eq 0 then begin
		message, '!! NO VALID UNOBSED FIELD FOUND !!', /cont
		printf, 77, '!! NO VALID UNOBSED FIELD FOUND !!'
		close, 77
		return
	end

	newfield = newfield[ix]

	; Remove fields with sun distance < 90
	sangle = fltarr(nix)
	for ff = 0, nix-1 do sangle[ff] = (map_2points(sra, sdec, newfield[ff].ra, newfield[ff].dec))[0]
	ix = where(sangle le 90, nix)
	print, nix, format='(I5," fields removed, too close to the Sun")'
	printf, 77, nix, format='(I5," fields removed, too close to the Sun")'
	if nix gt 0 then begin
		match, field.id, newfield[ix].id, ixf, ixn
		field[ixf].status = 8 ; removed
	endif
	ix = where(sangle gt 90, nix)
	if nix eq 0 then begin
		message, '!! NO VALID UNOBSED FIELD FOUND !!', /cont
		printf, 77, '!! NO VALID UNOBSED FIELD FOUND !!'
		close, 77
		return
	end
	newfield = newfield[ix]

	; new blocks
	nnewfield = n_elements(newfield)
	ixnewblock = uniq(newfield.block, sort(newfield.block))
	nnewblock = n_elements(ixnewblock)
	newblock = replicate({name:'', size:0, ctra:0.0d, ctdec:0.0d}, nnewblock)
	newblock.name = newfield[ixnewblock].block
	for k = 0, nnewblock-1 do begin
		ix = where(newfield.block eq newblock[k].name, nix)
		newblock[k].size = nix
		newblock[k].ctra  = mean(newfield[ix].ra )
		newblock[k].ctdec = mean(newfield[ix].dec)
	endfor

	print, nnewblock, nnewfield, format='("Found: ",I4," new blocks, ", I5," new fields")'
	printf, 77, nnewblock, nnewfield, format='("Found: ",I4," new blocks, ", I5," new fields")'

	; prepare for scripting
	jdnow = julday(mn, dy, yr, h0 - site_tz)
	jdend = julday(mn, dy, yr, h1 - site_tz)

	blocksn = 0
	expcount = 0
	timetotal = 0.0
	nb = intarr(nnewblock) + 1  ; flag to mark whether a block is used
	blockchosen = [-1L] ; indices of chosen block
	fieldchosen = [-1L] ; indices of chosen field

	; format of simulated obsed list
	simuformat = '("xxxx.fits",3x,"0000",3x,I5,3x,A,3x,F5.1,3x,"1")' ;fn1, sn1, object1, filter1, expt1, fr1
	file_mkdir, 'obsed/'+runcode
	if simulate then openw, 88, 'obsed/'+runcode+'/check.simu.'+days+'.lst'

	set_plot, 'ps'
	loadct, 39
	get_lun, lun

	; header of summary
	print, horline
	print, 'No', 'Block', 'Center-RA', 'Center-Dec', 'Alt', 'AirM', 'Field', 'Expo', 'Sec', 'Start', $
		format='(A2,":",A10,2x,A11,1x,A11,2x,A4,2x,A4,2x,A5,2x,A4,2x,A4,2x,A8)'
	printf, 77, horline
	printf, 77, 'No', 'Block', 'Center-RA', 'Center-Dec', 'Alt', 'AirM', 'Field', 'Expo', 'Sec', 'Start', $
		format='(A2,":",A10,2x,A11,1x,A11,2x,A4,2x,A4,2x,A5,2x,A4,2x,A4,2x,A8)'
	while jdnow lt jdend do begin
		; locate blocks unobsed
		nbix = where(nb, nix)
		if nix eq 0 then break ; if no block available, exit
		; find best block
		eq2hor, newblock.ctra, newblock.ctdec, jdnow, balt, baz, bha, lat=site_lat, lon=site_lon, alt=site_alt
		airm = zh_alt2air(balt)
		blockix = zj_chooseblock(newblock[nbix].ctra, newblock[nbix].ctdec, balt[nbix])

		if blockix eq -1 then break ; no available block, time may be wrong
		blockix = nbix[blockix]
		blockname = newblock[blockix].name

		f_ix = where(newfield.block eq blockname, nfix)
		blocksn++
		; mark block as used
		nb[blockix] = 0
		; record index
		blockchosen = [blockchosen, blockix]
		fieldchosen = [fieldchosen, f_ix]
		; mark chosen field as obsed this night
		match, field.id, newfield[f_ix].id, ixf, ixn
		field[ixf].status += 4 ; 0->4, 1->5

		planfile = string(daypath, blocksn, blockname, format='(A,"/block",I2.2,"_",A)')
		zh_plotairmass, planfile+'.eps', newblock.ctra, newblock.ctdec, airm, blockix

		timeused = 0
		nexp = 0
		; loop sequence: filter--object--expt(plan)--repeat
		openw, lun, planfile + '.txt'
		;;print, 'N_FILTER ', nfilter
		for fi = 0, nfilter-1 do begin
			p_ix = where(plan.filter eq filter[fi], npix)
			;;print, 'N_FIELD_WHERE', nfix
			for fld = 0, nfix-1 do begin
				f_ix1 = f_ix[fld]
				;;print, 'N_PLAN_WHERE', npix
				for p = 0, npix-1 do begin
					p_ix1 = p_ix[p]
					;;print, 'N_REP', newfield[f_ix1].rep[p_ix1]
					;;print, newfield[f_ix1].id, plan[p_ix1].filter, plan[p_ix1].expt, newfield[f_ix1].rep[p_ix1]
					fid = strtrim(newfield[f_ix1].id, 2)
					fra = newfield[f_ix1].ra & fdec = newfield[f_ix1].dec
					if plan[p_ix1].dither then begin
						fid += 'x'
						fra += ra_dither & fdec += dec_dither
					endif
					for r = 1, newfield[f_ix1].rep[p_ix1] do begin
						printf, lun, zj_obsline(fid, plan[p_ix1].filter, plan[p_ix1].expt, fra, fdec)
						if simulate then printf, 88, format=simuformat, $
							fid, plan[p_ix1].filter, plan[p_ix1].expt
						timeused += plan[p_ix1].expt + exptime_annex
						expcount++
						nexp++
					endfor
				endfor
			endfor
		endfor
		close, lun

		; summary for this block
		print, blocksn, blockname, zj_radec2str(newblock[blockix].ctra, newblock[blockix].ctdec), $
			balt[blockix], airm[blockix], nfix, nexp, timeused, zh_jd2str(jdnow, site_tz, 1), $
			format='(I2.2,":",A10,2x,A11,1x,A11,2x,F4.1,2x,F4.2,2x,I5,2x,I4,2x,I4,2x,A8)'
		printf, 77, blocksn, blockname, zj_radec2str(newblock[blockix].ctra, newblock[blockix].ctdec), $
			balt[blockix], airm[blockix], nfix, nexp, timeused, zh_jd2str(jdnow, site_tz, 1), $
			format='(I2.2,":",A10,2x,A11,1x,A11,2x,F4.1,2x,F4.2,2x,I5,2x,I4,2x,I4,2x,A8)'

		; simulate time going
		jdnow += timeused / 3600.0 / 24.0
		timetotal += timeused
	endwhile

	free_lun, lun
	if simulate then close, 88

	; final summary
	if blocksn eq 0 then begin
		message, 'Sorry, no available block found, please check!', /cont
		printf, 77, 'Sorry, no available block found, please check!'
		close, 77
		return
	endif
	blockchosen = blockchosen[1:*]
	fieldchosen = fieldchosen[1:*]
	nfieldchosen = n_elements(fieldchosen)
	print, '**', 'TOTAL', nfieldchosen, expcount, timetotal, zh_jd2str(jdnow, site_tz, 1), $
		format='(A2," ",A10,2x,11x,1x,11x,2x,4x,2x,4x,2x,I5,2x,I4, 1x,I5, 2x,A8)'
	printf, 77, '**', 'TOTAL', nfieldchosen, expcount, timetotal, zh_jd2str(jdnow, site_tz, 1), $
		format='(A2," ",A10,2x,11x,1x,11x,2x,4x,2x,4x,2x,I5,2x,I4, 1x,I5, 2x,A8)'
	print, horline
	if jdnow lt jdend then begin
		message, '!!!!! Warning: no block availble before the end time, please check!', /cont
		printf, 77, '!!!!! Warning: no block availble before the end time, please check!'
	endif

	; draw footprint
	;set_plot, 'ps'
	;loadct, 39
	device, file=daypath+'/map_'+days+'.eps', $
		/color,bits_per_pixel=16,xsize=24,ysize=12, $
		/encapsulated,yoffset=0,xoffset=0,/TT_FONT,/helvetica,/bold,font_size=10

	map_set, /grid, /mollweide, limit=[-10,-180,90,180], $
		/noborder, /label, latlab=-180, lonlab=-8, londel=30, latdel=10, reverse=1, $
		;position=[0.1,0.1, 0.9, 0.9], $
		title='Observation Plan for '+days
	; field status: 0 unobserved,  1 partly finished, 2 finished,
	;		4 totally new, 5 partly new, 9 skipped, 8 removed
	cl = [180, 220, 250, 0, 50, 70, 0, 0, 10, 190]
	for fld = 0, nfield-1 do begin
		polyfill, field[fld].ra+0.5*fieldsize*[-1,1,1,-1,-1]/cos(field[fld].dec/180.0*!pi), $
			field[fld].dec+0.5*fieldsize*[-1,-1,1,1,-1], $
			color=cl[field[fld].status]
	endfor
	xyouts, mra, mdec, string(mph*100, format='("* MOON",F5.1,"%")'), color=254
	xyouts, sra, sdec, '* SUN' , color=254

	xyouts, 180, -5, color=0, 'Color Legend:'
	xyouts, 150, -5, color=cl[0], 'Unobsevered'
	xyouts, 110, -5, color=cl[1], 'Partly Done'
	xyouts,  70, -5, color=cl[2], 'Full Done'
	xyouts,  30, -5, color=cl[4], 'Full Today'
	xyouts, -10, -5, color=cl[5], 'PartlyToday'
	xyouts, -50, -5, color=cl[8], 'Removed'
	xyouts, -90, -5, color=cl[9], 'Skipped'

	device, /close

	set_plot, 'x'

	printf, 77, horline
	printf, 77, 'Generated at ', systime()
	close, 77

	print, 'Merge block plan to day plan: '+daypath+'/merge_'+days+'.txt'
	spawn, 'cat '+daypath+'/block*.txt > '+daypath+'/merge_'+days+'.txt'
	print, 'Transfer to DOS format'
	spawn, 'unix2dos -q -k '+daypath+'/block*.txt '+daypath+'/merge_*.txt'

	if simulate then z_Collect, runcode

	print, 'DONE!   Bye.'
end
