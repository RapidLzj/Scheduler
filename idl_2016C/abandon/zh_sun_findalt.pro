function zh_sun_findalt, jd0, jd1, lat, lon, ele, direction, $
  basealt=basealt, maxn=maxn, prec=prec, moon=moon
  
  if ~keyword_set(maxn) then maxn = 10
  if ~keyword_set(prec) then prec = 1d-3
  if ~keyword_set(basealt) then basealt = 0.0d
  
  zh_sunalt, jd0, lat, lon, ele, sra0, sdec0, salt0, saz0, basealt=basealt, moon=moon
  zh_sunalt, jd1, lat, lon, ele, sra1, sdec1, salt1, saz1, basealt=basealt, moon=moon

  ; if no rise or set between jd0 and jd1, return -1
  ; jd0 to jd1 is shorter than half day, will not include both rise and set
  ; direction: 1 rise or always in sky, -1 set or always under ground
  if salt0 lt 0 and salt1 lt 0 then begin direction = -1 & return, -1 & endif 
  if salt0 gt 0 and salt1 gt 0 then begin direction = +1 & return, -1 & endif
  if salt0 lt salt1 then direction = 1 else direction = -1
  
  nn = 0
  repeat begin 
    jdm = (jd1 * salt0 - jd0 * salt1) / (salt0 - salt1)
    zh_sunalt, jdm, lat, lon, ele, sram, sdecm, saltm, sazm, basealt=basealt, moon=moon
    
    ;caldat, jd0, mn0, dy0, yr0, hr0, mi0, se0
    ;caldat, jd1, mn1, dy1, yr1, hr1, mi1, se1
    ;caldat, jdm, mnm, dym, yrm, hrm, mim, sem
    ;print, hr0,mi0,se0,salt0, hr1,mi1,se1,salt1, hrm,mim,sem,saltm, format='(3(I2.2,":",I2.2,":",I2.2, "=",F6.2,3X))'

    if zh_sign3(saltm) eq zh_sign3(salt0) then begin
      jd0 = jdm
      salt0 = saltm
    endif else begin
      jd1 = jdm
      salt1 = saltm
    endelse
    nn ++
  endrep until abs(saltm) lt prec or jd1-jd0 lt prec or nn ge maxn

  return, jdm
end
