pro z_Check, yr, mn, dy, runcode
; Check fits files in files.xxx.lst, and make check.xxx.lst

	if ~keyword_set(runcode) then $
  		runcode = string(yr, mn, format='(I4.4,I2.2)')
	days = string(yr, mn, dy, format='(I4.4,I2.2,I2.2)')

	filelst = 'obsed/'+runcode+'/files.'+days+'.lst'
	chklst  = 'obsed/'+runcode+'/check.'+days+'.lst'

	if ~file_test(filelst) then begin
		message, filelst + ' NOT exist. QUIT', /cont
		return
	endif
	;readcol, filelst, filename, filerank, format='a,i', count=nf, /silent
	readcol, filelst, filename, format='a', count=nf, /silent

	openw, 1, chklst
	fc = 0
	for ff = 0, nf-1 do begin
		z_HeaderInfo, filename[ff], sn, object, filter, expt, ra, dec
		if sn ne 0 then begin
			fc++
			printf, 1, filename[ff], sn, object, filter, expt, 1, $;filerank[ff], $
				format='(A,2x, I4.4,2x, A10,2x, A6,2x, F6.2,2x, I2)'
		endif
	endfor
	close, 1
	if fc eq 0 then file_delete, chklst

	print, days, nf, fc, format='("File info of ",A8," checked, ",I3," fits, ",I3," object fits")'
end
