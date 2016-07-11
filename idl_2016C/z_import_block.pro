pro z_import_block

	file_field_old = 'conf/field.bok.txt'
	file_block_old = 'conf/block.bok.txt'
	file_field_new = 'conf/field.lst'
	file_block_new = 'conf/block.lst'
	block_size = 7
	
	; load fields
	readcol, file_field_old, f_ra, f_dec, f_id, format='d,d,l', count=nf
	f_b_id = lonarr(nf)
	; load blocks
	readcol, file_block_old, b_name, b_size, format='a,i', count=nb
	block_size = max(b_size)
	b_f_id = lonarr(nb, block_size)
	openr, 11, file_block_old
	line = ''
	lineno = 0
	while ~ eof(11) do begin
		readf, 11, line
		part = strsplit(line, '**', /extract)
		ff_id = lonarr(b_size[lineno])
		reads, part[1], ff_id
		b_f_id[0:b_size[lineno]-1] = ff_id
		match, f_id, ff_id, ixf, ixff
		f_b_id[ixf] = lineno
		lineno++
	endwhile
	close, 11
	
	; write new field file
	openw, 11, file_field_new
	for k = 0, nf-1 do begin
		printf, 11, f_id[k], f_ra[k], f_dec[k], b_name[f_b_id[k]], $
			format='(I6,2x,D10.6,2x,D10.6,2x,A9)'
	endfor
	close, 11
	
	; write new block file
	; only 2 heading columns needed, so directly copy file
	file_copy, file_block_old, file_block_new
end