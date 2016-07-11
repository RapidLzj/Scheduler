function zh_hms, value, DEG=deg, HMS=hms, LEN=len
  mode = 'n' ;12 34 56.789
  if keyword_set(deg) then mode = 'd' ; 12d34m56s789
  if keyword_set(hms) then mode = 'h' ; 12h34m56s789
  if ~ keyword_set(len) then len=13

  ;r = dec2hms(value)
  eps = (machar(double=double)).eps ; machine precision

  hhh = replicate({neg:'+', h:0, m:0, s:0, ss:0}, n_elements(value))
  
  angle = double(value)

  ix = where(angle lt 0.0d)
  if ix[0] ne -1 then hhh[ix].neg = '-'
  angle = abs(angle)

  hhh.h = floor(angle+eps)
  angle = (angle-hhh.h)*60.0d
  
  hhh.m = floor(angle+eps*60)
  angle = (angle-hhh.m)*60.0d
  
  hhh.s = floor(angle+eps*3600)
  angle = (angle-hhh.s)*1000.0d
  
  hhh.ss = floor(angle+eps*3600000)
  
  if mode eq 'd' then begin
    fmt = '(A1,I2.2,"!Eo!N",I2.2,"''",I2.2,''"'',I3.3)'
  endif else if mode eq 'h' then begin
    fmt = '(A1,I2.2,"h",I2.2,"m",I2.2,"s",I3.3)'
  endif else begin
    fmt = '(A1,I2.2,":",I2.2,":",I2.2,".",I3.3)'
  endelse
  
  shms=string(hhh, format=fmt)

  if mode eq 'd' && len gt 3 then len += 4
  shms = strmid(shms, 0, len)

  return, shms
end
