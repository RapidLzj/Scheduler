readcol, 'sdss_map.txt', r, d, t, format='f,f,i'

readcol, 'nowt_field.txt', fid, fr, fd, fb, fl, format='i,f,f,f,f', count=nf

tt = bytarr(nf)

openw, 1, 'nowt_field_tag.txt'

for f = 0, nf-1 do begin $
    scl = cos(fd[f] / 180.0 * !pi) & $
    ix = where(r ge fr[f] - 0.6/scl and r le fr[f] + 0.6/scl and d ge fd[f] - 0.6 and d le fd[f] + 0.6) & $
    if ix[0] ge 0 then tt[f] = (total(t[ix]) gt 0) else tt[f] = 0 & $
    printf, 1, fid[f], fr[f], fd[f], fb[f], fl[f], tt[f], $
        format='(I5,2x,F8.4,2x,F8.4,2x,F8.4,2x,F8.4,2x,I1)' & $
endfor

close, 1

ix1 = where(tt eq 1)
ix0 = where(tt eq 0)

map_set, /moll, /grid, reverse=1
oplot, fr[ix1], fd[ix1], psym=3, color='0000ff'xl
oplot, fr[ix0], fd[ix0], psym=3, color='00ff00'xl

map_set, /moll, /grid, reverse=1
oplot, fb[ix1], fl[ix1], psym=3, color='0000ff'xl
oplot, fb[ix0], fl[ix0], psym=3, color='00ff00'xl

mr = [0.0] ; map ra
md = [0.0] ; map dec
mt = [0]   ; map tag
for ad = -89.5, 89.5, 0.5 do begin $
    scl = cos(ad / 180 * !pi) & $
    linecnt = fix(720 * scl) & $
    mrline = findgen(linecnt) * 0.5 / scl & $
    mdline = fltarr(linecnt) + ad & $
    mtline = intarr(linecnt) & $
    mr = [mr, mrline] & md = [md, mdline] & $
    for ar = 0, linecnt-1 do begin $
        ix = where(r ge mrline[ar] - 0.3/scl and r le mrline[ar] + 0.3/scl and d ge ad - 0.3 and d le ad + 0.3) & $
        if ix[0] ge 0 then mtline[ar] = (total(t[ix]) gt 0) else mtline[ar] = 0 & $
    endfor & $
    mt = [mt, mtline] & $
    print, '.', format='(a,$)' & $
endfor
print, ''

n_m = n_elements(mt)

openw, 1, 'map_tag.txt'
for f = 1, n_m-1 do printf, 1, mr[f], md[f], mt[f], format='(F8.4,2x,F8.4,2x,I1)'
close, 1

;;;;;;;;;;;;

readcol,'nowt_field_tag.txt',f_id,f_ra,f_dec,f_gb, f_gl, f_tag, format='i,f,f,f,f,i', count=nf

ixf1 = where(f_tag eq 1, n_f1)
ixf0 = where(f_tag eq 0, n_f0)

cl_sdss = '0000ff'xl
cl_our  = 'ffff00'xl
gl=findgen(37)*10
gb=fltarr(37)
glactc, xra,xdec,2000,gl,gb,2,/deg

map_set, /moll, /grid, reverse=1,limit=[-10,0,90,360];,title='NOWT Fields', label=3,lonlab=-8,latlab=90
oplot, f_ra[ixf1]-180, f_dec[ixf1], psym=6, symsize=0.5, color=cl_sdss
oplot, f_ra[ixf0]-180, f_dec[ixf0], psym=6, symsize=0.5, color=cl_our
oplot,xra-180,xdec
oplot,[135,180]-180,[65,65],color='00ffff'xl,thick=2
oplot, 135-findgen(12)-180,65-findgen(12)*5,color='00ffff'xl,thick=2

oplot, [85], [-5], psym=6, color=cl_sdss & xyouts, 80, -5, string(n_f1, format='("SDSS: ",I5," blocks")'), color=cl_sdss
oplot, [10], [-5], psym=6, color=cl_our  & xyouts,  5, -5, string(n_f0, format='("Our: ",I5," blocks")'), color=cl_our

ixk1 = where(f_tag eq 0 and (f_gl lt 0 or f_ra lt 180))
