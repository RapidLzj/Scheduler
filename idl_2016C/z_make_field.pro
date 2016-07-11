pro z_make_field, outpath, step, $
  rarange=rarange, decrange=decrange, $
  glrange=glrange, gbrange=gbrange
  
  if ~keyword_set(outpath)   then outpath   = 'conf/'
  if ~keyword_set(step)      then step      = [  1.0d,   1.0d]
  if  n_elements (step) eq 1 then step      = [  step,   step]
  if ~keyword_set(rarange)   then rarange   = [  0.0d, 360.0d]
  if ~keyword_set(decrange)  then decrange  = [ -2.0d,  89.0d]
  if ~keyword_set(glrange)   then glrange   = [  0.0d, 360.0d]
  if ~keyword_set(gbrange)   then gbrange   = [-90.0d, +90.0d]
  
  file_mkdir, outpath
  openw, 11, outpath + 'field_all.txt'
  
  gbin = gbrange[0] lt gbrange[1]
  glin = glrange[0] lt glrange[1]
  plot, [0],[0], xr=[0,360],yr=[-40,90]
  
  id = 0L
  decn = ceil((decrange[1] - decrange[0]) / step[1])
  for dd = 0, decn-1 do begin
    dec = decrange[0] + dd * step[1]
    rascale = cos(dec * !dpi / 180.0d)
    ran = ceil((rarange[1] - rarange[0]) / step[0] * rascale)
    for rr = 0, ran-1 do begin
      ra = rarange[0] + rr * step[0] / rascale
      
      glactc, ra, dec, 2015, gl, gb, 1, /degree
      if glin then glok = glrange[0] le gl and gl le glrange[1] else glok = gl ge glrange[0] or glrange[1] ge gl 
      if gbin then gbok = gbrange[0] le gb and gb le gbrange[1] else gbok = gb ge gbrange[0] or gbrange[1] ge gb
      
      if glok and gbok then begin
        id ++
        printf, 11, id, ra, dec, gl, gb, lzju_hms(ra/15.0d), lzju_hms(dec), $
          format='(I6, 2(3X,F9.5), 2(3X,F7.3), 2(3X,A11))' 
        oplot,[ra], [dec], psym=4
      endif
      
    endfor
  endfor
  
  close, 11
  
  print, id, outpath + 'field_all.txt', format='(I6, " fields generated in ",A)'
  
end