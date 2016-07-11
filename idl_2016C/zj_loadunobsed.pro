function zj_loadunobsed, allfield, plan, count, silent=silent
	; input
	;   allfield: all fields
	;   plan: plan structure array
	; output
	;   count: count of unfinished fields, including new fields and partly finished fields
	;   return: structure array of unfinished fields:
	;	{id:long, ra:double, dec:double, block:string, factor:fltarr(nplan), rep:intarr(nplan)}
	;		factor: finished factor for each plan
	;		rep: repeat times need for each plan
	;	allfield.status
	;		0 unobserved,  1 partly finished, 2 finished,
	;		4 totally new, 5 partly new, 9 skipped, 8 removed

	; extent field structure with factor, rep and status
	nfield = n_elements(allfield)
	nplan = n_elements(plan)
	result = replicate({id:-1L, ra:0.0d, dec:0.0d, block:'', factor:fltarr(nplan), rep:intarr(nplan), status:0}, nfield)
	for k=0,3 do result.(k) = allfield.(k)

	; if skipped.lst exists, load skipped fields and mark
	if file_test('obsed/skipped.lst') then begin
		readcol, 'obsed/skipped.lst', sid, format='i', count=nskipped, /silent
		if ~keyword_set(silent) then print, nskipped, format='("Loading ",I5," skipped fields")'
		match, sid, result.id, six, rix
		result[rix].status = 9
	endif

	nplan = n_elements(plan)
	obsedfiles = file_search('obsed/', 'obsed.lst', count=nof)
	obsed1 = {f_id:-1L, factor:fltarr(nplan)}
	obsed = [obsed1]
	for ff = 0, nof-1 do begin
		obsed2 = r_readstruct(obsedfiles[ff], obsed1, count=nobsed, /silent)
		if ~keyword_set(silent) then print, nobsed, obsedfiles[ff], format='("Loading ",I5," obsed item from ",A)'
		obsed = [obsed, obsed2]
	endfor
	nobsed = n_elements(obsed) - 1

	;3. Remove finished fields, get new blocks
	; 3.1 merge finished factor
	if nobsed gt 0 then begin
		for ff = 0, nfield-1 do begin
			; find obsed factor for each field, then sum factor for each plan
			ix = where(obsed.f_id eq result[ff].id, nix)
			if nix gt 1 then $
				result[ff].factor = total(obsed[ix].factor, 2) $
			else if nix eq 1 then $
				result[ff].factor = obsed[ix].factor
			;;if nix gt 0 then print, result[ff]
			;result.rep = ceil((1.0 - result[ff].factor > 0.0) / plan.factor)
			;maxrep = max(result[ff].rep, min=minrep)
			;if maxrep eq 0 then result[ff].status = 2 ; finished
			;if maxrep gt 0 and minrep eq 0 then result[ff].status = 1 ; partly finished
		endfor
	endif

	; get repeat times for each unfinished field
	for k = 0, nplan-1 do $
		result.rep[k] = ceil((1.0 - result.factor[k] > 0.0) / plan[k].factor)

	maxfac = max(result.factor, dim=1, min=minfac)
	; set status for finished
	ix = where(minfac ge 1.0, nix)
	if nix gt 0 then result[ix].status = 2
	; set status for partly finished
	ix = where(minfac lt 1.0 and maxfac gt 0.0, nix)
	if nix gt 0 then result[ix].status = 1

	allfield.status = result.status

	; new block
	ix = where(result.status le 1, nix)  ; 0 or 1
	count = nix

	return, result[ix]
end