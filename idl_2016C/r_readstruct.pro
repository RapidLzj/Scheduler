function r_readstruct, filename, stru, tags, $
	SILENT = silent, SKIPLINE = skipline, $
	NUMLINE = numline, COUNT=count, $
	DELIMITER =  delimiter, COMMENT=comment

	; parameters
	silent = keyword_set(silent)
	if ~keyword_set(delimiter) then delimiter = ' '
	if ~keyword_set(comment)   then comment   = '#'
	commentlen = strlen(comment)

	; file line number process
	nlines = FILE_LINES( filename )
 
	if ~keyword_set( SKIPLINE ) then skipline = 0
	if keyword_set( NUMLINE) then nlines = numline < nlines else nlines = nlines - skipline
 
	if nlines LE 0 then begin
		message,'ERROR - File ' + name+' contains no valid data',/CON
		return,''
	endif
	
	; structure tags process
	ntag = N_tags(stru) ; number of directly tags
	nitem = intarr(ntag) ; item number of each tag (if array tag)
	for t = 0, ntag-1 do nitem[t] = n_elements(stru.(t))
	if ~keyword_set(tags) then tags = indgen(ntag)
	ntag = n_elements(tags)
	
	; total cols needed
	ixr = where(tags ge 0, nixr) & ixx = where(tags lt 0, nixx)
	ncol = total(nitem[ixr])
	if nixx gt 0 then ncol += nixx
		
	; create result structure array
	res = replicate(stru, nlines)
	linevalid = intarr(nlines) + 1 ; valid flag
	
	; read
	openr, lun, filename, /get_lun
	skip_lun, lun, skipline, /lines

	line = ''
	space = strtrim(delimiter) eq ''
	for k = 0, nlines-1 do begin
		readf, lun, line
		; comment check
		if strmid(line, 0, commentlen) eq comment then begin
			if ~silent then message, 'Skip comment line ' + strtrim(skipline+k+1,2),/CON
			linevalid[k] = 0
			continue
		endif
		; empty line
		if strtrim(line, 2) eq '' then begin
			linevalid[k] = 0
			continue
		endif
		; split, and field number check
		if space then $
			part = strsplit(line, count=npart, /extract) $
		else $
			part = strsplit(line, delimiter, count=npart, /extract, /preserve)
		if npart lt ncol then begin
			if ~silent then message, 'Error reading line ' + strtrim(skipline+k+1,2),/CON
			linevalid[k] = 0
			continue
		endif
		; trap for format check
		catch, error_flag
		if error_flag ne 0 then begin
			if ~silent then message, 'Error reading line ' + strtrim(skipline+k+1,2),/CON
			linevalid[k] = 0
			catch, /cancel
			continue
		endif
		; read each col
		pcol = 0
		for t = 0, ntag-1 do begin
			tt = tags[t]
			if tt lt 0 then begin
				pcol ++
			endif else begin
				part1 = strjoin(part[pcol:pcol+nitem[tt]-1], ' ')
				pcol += nitem[tt]
				one = res[k].(tt)
				reads, part1, one
				res[k].(tt) = one
			endelse
		endfor
	endfor
	catch, /cancel
	close, lun
	free_lun, lun
	
	goodix = where(linevalid, ngood)
	count = ngood
	res = res[goodix]
	if ~silent then message, strtrim(count,2)+' line(s) read', /CON
	return, res
end