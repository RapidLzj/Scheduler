pro z_PlotRun, outfile, runcode, datestr

    ; load fields and plan
    zj_loadskydata, field, plan, factor, filter, ra_dither, dec_dither
	nfield  = n_elements(field )
	nplan   = n_elements(plan  )
	nfactor = n_elements(factor)
	nfilter = n_elements(filter)

    ; load obsed history
    newfield = zj_loadunobsed(field, plan, count, /silent)

    ; load obsed for this run or today
    if keyword_set(datestr) then begin
        checkfile = file_search('obsed/'+runcode, 'check.*'+datestr+'.lst', count=ncheck)
    endif else if keyword_set(runcode) then begin
        checkfile = file_search('obsed/'+runcode, 'check.*.lst', count=ncheck)
    endif else begin
        ncheck = 0
    endelse

    for c = 0, ncheck-1 do begin
        readcol, checkfile[c], cf, format='x,x,a,x,x,x', count=ncf, /silent
        for f = 0, ncf-1 do begin
            ix = where(field.id eq cf[f], nix)
            if nix gt 0 then field[ix].status = 4 ; no matter how much obsed, marked as this run
        endfor
    endfor

    ; plotting
    set_plot, 'ps'
	loadct, 39, /silent
	fieldsize=0.8
	device, file=outfile, $
		/color,bits_per_pixel=16,xsize=24,ysize=12, $
		/encapsulated,yoffset=0,xoffset=0,/TT_FONT,/helvetica,/bold,font_size=10

	map_set, /grid, /mollweide, limit=[-10,-180,90,180], $
		/noborder, /label, latlab=-180, lonlab=-8, londel=30, latdel=10, reverse=1, $
		;position=[0.1,0.1, 0.9, 0.9], $
		title='Survey Footprint'
	; field status: 0 unobserved,  1 partly finished, 2 finished,
	;		4 totally new, 5 partly new, 9 skipped, 8 removed
	cl = [180, 220, 250, 0, 50, 70, 0, 0, 10, 190]
	for fld = 0, nfield-1 do begin
		polyfill, field[fld].ra+0.5*fieldsize*[-1,1,1,-1,-1]/cos(field[fld].dec/180.0*!pi), $
		    field[fld].dec+0.5*fieldsize*[-1,-1,1,1,-1], $
			color=cl[field[fld].status]
	endfor
	;xyouts, mra, mdec, string(mph*100, format='("* MOON",F5.1,"%")'), color=254
	;xyouts, sra, sdec, '* SUN' , color=254

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

    ix = where(field.status eq 4, nix)
    print, nix, format='(I5," fields obsed in this run or day.")'

end