    ; parameter check and transfer
	horline = strjoin(replicate('-', 80),'')
	simulate = keyword_set(simulate)
	if ~keyword_set(runcode) then runcode = string(yr, mn, format='(I4.4,I2.2)')
	days = string(yr, mn, dy, format='(I4.4,I2.2,I2.2)')
	daypath = 'plan/'+runcode+'/'+days
	nows = string((bin_date(systime()))[0:5], format='(I4.4,I2.2,I2.2,I2.2,I2.2,I2.2)')
	if ~keyword_set(time0) then begin
		message, 'Start time not provided, default as 18:00', /cont
		time0 = '18:00'
	endif
	if ~keyword_set(time1) then begin
		message, 'End time not provided, default as 06:00', /cont
		time1 = '06:00'
	endif
	h0 = zh_str2hour(time0, 99)
	h1 = zh_str2hour(time1, 99)
	if h0 gt 90.0 then begin
		message, 'Start time format invalid, default as 18:00', /cont
		h0 = 18.0
	endif
	if h1 gt 90.0 then begin
		message, 'End time format invalid, default as 06:00', /cont
		h1 = 30.0
	endif
	if h0 ge h1 then begin
		message, 'Start time must be earlier to end time. QUIT!', /cont
		return
	endif

	; Load basic data from configure file

	if ~file_test('conf/basic.txt') then begin
		message, 'Basic Configuration file "conf/basic.txt" is missing. QUIT.'
		return
	endif
	line = ''
	openr, 11, 'conf/basic.txt'

	readf, 11, line
	site_d = 0.0 & side_m = 0.0 & site_s = 0.0
	reads, line, site_d, side_m, site_s
	site_lon = ten(site_d, side_m, site_s)
	print, site_d, side_m, site_s, site_lon, format='("Site Longitude: ",F6.1,F5.1,F5.1,"-->",F10.5," deg")'

	readf, 11, line
	site_d = 0.0 & side_m = 0.0 & site_s = 0.0
	reads, line, site_d, side_m, site_s
	site_lat = ten(site_d, side_m, site_s)
	print, site_d, side_m, site_s, site_lat, format='("Site Latitude:  ",F6.1,F5.1,F5.1,"-->",F10.5," deg")'

	readf, 11, line
	site_alt = 0.0
	reads, line, site_alt
	print, site_alt, format='("Site Altitude: ",F7.1," meters above sea level")'

	readf, 11, line
	site_tz = 0
	reads, line, site_tz
	print, site_tz, format='("Site timezone: UTC",I+3)'

	readf, 11, line
	exptime_annex = 0.0
	reads, line, exptime_annex
	print, exptime_annex, format='("Extra time before and after exposure is estimated as ",F5.1," seconds")'

	readf, 11, line
	fieldsize = 1.0
	reads, line, fieldsize

	close, 11

    ; load field and plan data
	zj_loadskydata, field, plan, factor, filter, ra_dither, dec_dither
	nfield  = n_elements(field )
	nplan   = n_elements(plan  )
	nfactor = n_elements(factor)
	nfilter = n_elements(filter)

    ; check file exist
    if file_test(daypath) then begin
		if keyword_set(backup) then $
			ans = 'B' $
		else if keyword_set(overwrite) then $
			ans = 'O' $
		else begin $
			ans = '' & $
			read, ans, prompt='Plan for '+days+' already exists! Overwrite/Backup/[Quit] ?' & $
		endelse
		ans = strupcase(strmid(strtrim(ans,2),0,1))
		if ans eq 'B' then begin
			file_move, daypath, daypath+'_'+nows
			print, 'Original plan backup as "'+daypath+'_'+nows+'"'
		endif else if ans ne 'O' then begin
			print, 'Everything remains original.   Bye!'
			return
		endif
	endif
