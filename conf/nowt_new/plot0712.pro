;readcol,'nowt_field_tag.txt',fid, fra,fdec,fgl,fgb,ftag,format='l,f,f,f,f,i',count=nf

ix1 = where(ftag eq 1)
ix0 = where(ftag eq 0)
ixm = where( (fgb gt 0 and fra lt 185 and (fra lt 135 or fdec ge 65)) $
          or (fgb lt 0 and (fdec gt 30 or (fra le 330 and fra ge 30))) )
ixp = where( ( (fgb gt 0 and fra lt 185 and (fra lt 135 or fdec ge 65)) $
             or(fgb lt 0 and (fdec gt 30 or (fra le 330 and fra ge 30))) ) and ftag eq 1 )

window, xsize=1000, ysize=700
map_set, /grid, /moll, rev=1, limit=[-10,0,90,360], /noborder
oplot, fra[ix0]-180, fdec[ix0], psym=1,color='00ffff'xl
oplot, fra[ix1]-180, fdec[ix1], psym=1,color='0000ff'xl
oplot, fra[ixm]-180, fdec[ixm], psym=1,color='ff0000'xl
oplot, fra[ixp]-180, fdec[ixp], psym=1,color='00ff00'xl
for h = 0,24,3 do xyouts, h * 15 - 180, -5, strn(h) + 'H'
xyouts, 105,  0, '0'
xyouts, 110, 10, '10'
xyouts, 115, 20, '20'
xyouts, 120, 30, '30'
xyouts, 130, 40, '40'
xyouts, 145, 50, '50'
xyouts, 170, 60, '60'
