pro zj_loadskydata, field, plan, factor, filter, ra_dither, dec_dither

	;1. Load all blocks and fields, and exp plan
	;1.1 fields
	field = r_readstruct('conf/field.lst', /silent, count=nfield, $
		{id:-1L, ra:0.0d, dec:0.0d, block:'', status:0}, [0,1,2,3])
	;1.2 blocks (abandoned, no use!)
	;block = r_readstruct('conf/block.lst', /silent, count=nblock, $
	;	{name:'', size:0, ctra:0.0d, ctdec:0.0d}, [0,1])
	;1.3 exp plan and factor
	plan = r_readstruct('conf/exp_plan.txt', /silent, count=nplan, $
		{code:-1, filter:'', expt:0.0, rep:0, factor:0.0, dither:0, name:''}, [0,1,2,3,4,5,6])
	factor = r_readstruct('conf/exp_factor.txt', /silent, count=nfactor, $
		{filter:'', expt:0.0, code:-1, factor:0.0}, [0,1,2,3])
	; get unique filters from plan
	filter = plan.filter
	filter = filter[uniq(filter, sort(filter))]
	nfilter = n_elements(filter)
	ra_dither = 0.0 & dec_dither = 0.0
	if file_test('conf/dither.txt') then begin
		openr, 11, 'conf/dither.txt'
		readf, 11, ra_dither, dec_dither
		close, 11
	endif else begin
		message, 'Dither configure file "conf/dither.txt" is missing, default no dither.', /cont
	endelse

end