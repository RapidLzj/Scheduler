pro z_Collect, runcode
  ;1. Find file list for this run
  ;2. Load exp plan and factor data
  ;3. Read list info, put into correct list
  ;4. For each exposure, if depth not enough, then mark as fail
  ;5. Collect all ok image info, generate a list
  ;6. Backup the original finished list if exists, save new list

  ;1.
  filelst = file_search('obsed/'+runcode, 'check.*.lst', count=nl)
  runlst = 'obsed/'+runcode+'/obsed.lst'

  ;2.
  readcol, 'conf/exp_plan.txt', p_code, p_filter, p_expt, p_repeat, p_factor, p_dither, p_name, $
  	format='i,a,f,i,f,i,a', count=np, /silent
  readcol, 'conf/exp_factor.txt', f_filter, f_expt, f_code, f_factor, format='a,f,i,f', /silent

  ;3.
  na = 0
  for ll = 0, nl-1 do begin
    readcol, filelst[ll], fn1, sn1, object1, filter1, expt1, fr1, $
      format='a,i,a,a,f,i', count=nf, /silent
    print, nf, filelst[ll], format='("Load ",I3," files from ",A)'
    if nf gt 0 then begin
      if na eq 0 then begin
        fn     = fn1
        sn     = sn1
        object = object1
        filter = filter1
        expt   = expt1
        fr     = fr1
      endif else begin
        fn     = [fn    , fn1]
        sn     = [sn    , sn1]
        object = [object, object1]
        filter = [filter, filter1]
        expt   = [expt  , expt1]
        fr     = [fr    , fr1]
      endelse
      na += nf
    endif
  endfor

  ;4.
  ix = where(fr gt 0, na)
  fn     = fn    [ix]
  sn     = sn    [ix]
  object = object[ix]
  filter = filter[ix]
  expt   = expt  [ix]
  fr     = fr    [ix]
  ; remove dither mark (x as postfix), take as the same
  for ff = 0, na-1 do $
    if strmid(object[ff], 0, 1, /reverse) eq 'x' then $
      object[ff] = strmid(object[ff], 0, strlen(object[ff])-1)

  uobj = object[uniq(object, sort(object))]
  nuobj = n_elements(uobj)

  ;5.
  obsed = fltarr(nuobj, np)
  for ff = 0, na-1 do begin
    c_ix = where(f_filter eq filter[ff] and f_expt eq expt[ff])
    o_ix = where(uobj eq object[ff])
    if c_ix[0] ne -1 and o_ix[0] ne -1 then $
    	obsed[o_ix, f_code[c_ix]] += f_factor[c_ix]
  endfor

  ;6.
  bd = bin_date(systime())
  nows = string(bd[0:5], format='(I4.4,I2.2,I2.2,I2.2,I2.2,I2.2)')
  if file_test(runlst) then begin
    print, 'Old version backup as ', '/obsed.'+nows+'.bak'
    file_move, runlst, 'obsed/'+runcode+'/obsed.'+nows+'.bak'
  endif

  openw, 1, runlst
  printf, 1, p_name, format='("# Object  ",'+strn(np)+'(A10))'
  for ff = 0, nuobj-1 do begin
    printf, 1, uobj[ff], obsed[ff, *], format='(A-10, 4(F10.1))'
  endfor
  close, 1
  print, runcode, nuobj, format='("New obsed list of ",A," generated, ",I5," objects")'
end
