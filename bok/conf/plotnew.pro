readcol, 'field.xao.txt', xid0, xra0, xdec0, xgl0, xgb0, format='l,f,f,f,f', count=n0
readcol, 'field.xao.new.txt', xid1, xra1, xdec1, xgl1, xgb1, format='l,f,f,f,f'
readcol, 'field.xao.sdss.txt', xid2, xra2, xdec2, xgl2, xgb2, format='l,f,f,f,f', count=xn2

match, xid0, xid1, xix1, xix11
match, xid0, xid2, xix2, xix22
status = intarr(n0)
status[xix1] = 1
status[xix2] = 2
xix0 = where(status eq 0, xn0)
xix1 = where(status eq 1, xn1)

set_plot, 'ps'
loadct, 39
device, file='field.xao.A.eps',  /encapsulated, /color, xsize=30, ysize=18
map_set, /moll, /grid, /noborder, limit=[-30,0,90,360], reverse=1, title='XAO Obs Fields'
oplot, xra0[xix0], xdec0[xix0], psym=6, symsize=0.5, color=50
oplot, xra0[xix1], xdec0[xix1], psym=6, symsize=0.5, color=250
oplot, xra0[xix2], xdec0[xix2], psym=6, symsize=0.5, color=150
xyouts, 120, -25, string(xn0, format='("Abondoned: ",I5)'), color=50
xyouts,  30, -25, string(xn1, format='("SDSS: ",I5)'), color=250
xyouts, -30, -25, string(xn2, format='("New plan: ",I5)'), color=150
device, /close

device, file='field.xao.B.eps',  /encapsulated, /color, xsize=30, ysize=18
map_set, /moll, /grid, /noborder, limit=[-30,0,90,360], reverse=1
oplot, xra0[xix0]-180, xdec0[xix0], psym=6, symsize=0.5, color=50
oplot, xra0[xix1]-180, xdec0[xix1], psym=6, symsize=0.5, color=250
oplot, xra0[xix2]-180, xdec0[xix2], psym=6, symsize=0.5, color=150
xyouts, 120, -25, string(xn0, format='("Abondoned: ",I5)'), color=50
xyouts,  30, -25, string(xn1, format='("SDSS: ",I5)'), color=250
xyouts, -30, -25, string(xn2, format='("New plan: ",I5)'), color=150
device, /close

device, file='field.xao.G.eps',  /encapsulated, /color, xsize=30, ysize=18
map_set, /moll, /grid, /noborder, reverse=1
oplot, xgl0[xix0], xgb0[xix0], psym=6, symsize=0.5, color=50
oplot, xgl0[xix1], xgb0[xix1], psym=6, symsize=0.5, color=250
oplot, xgl0[xix2], xgb0[xix2], psym=6, symsize=0.5, color=150
xyouts, 120, -5, string(xn0, format='("Abondoned: ",I5)'), color=50
xyouts,  30, -5, string(xn1, format='("SDSS: ",I5)'), color=250
xyouts, -30, -5, string(xn2, format='("New plan: ",I5)'), color=150
device, /close

readcol, 'field.bok.txt', bra0, bdec0, bid0, bgl0, bgb0, format='f,f,l,x,f,f', count=n0
readcol, 'field.bok.new.txt', bid1, bra1, bdec1, bgl1, bgb1, format='l,f,f,f,f', count=bn1

match, bid0, bid1, bix1, bix11
status = intarr(n0)
status[bix1] = 1
bix0 = where(status eq 0, bn0)

set_plot, 'ps'
loadct, 39
device, file='field.bok.A.eps',  /encapsulated, /color, xsize=30, ysize=18
map_set, /moll, /grid, /noborder, limit=[-10,0,90,360], reverse=1, title='Bok Obs Fields'
oplot, bra0[bix0], bdec0[bix0], psym=6, symsize=0.5, color=50
oplot, bra0[bix1], bdec0[bix1], psym=6, symsize=0.5, color=150
xyouts,  90, -5, string(bn0, format='("Abondoned: ",I5)'), color=50
xyouts, -30, -5, string(bn0, format='("New plan: ",I5)'), color=150
device, /close

device, file='field.bok.B.eps',  /encapsulated, /color, xsize=30, ysize=18
map_set, /moll, /grid, /noborder, limit=[-10,0,90,360], reverse=1, title='Bok Obs Fields'
oplot, bra0[bix0]-180, bdec0[bix0], psym=6, symsize=0.5, color=50
oplot, bra0[bix1]-180, bdec0[bix1], psym=6, symsize=0.5, color=150
xyouts,  90, -5, string(bn0, format='("Abondoned: ",I5)'), color=50
xyouts, -30, -5, string(bn0, format='("New plan: ",I5)'), color=150
device, /close

device, file='field.bok.G.eps',  /encapsulated, /color, xsize=30, ysize=18
map_set, /moll, /grid, /noborder, reverse=1, title='Bok Obs Fields'
oplot, bgl0[bix0], bgb0[bix0], psym=6, symsize=0.5, color=50
oplot, bgl0[bix1], bgb0[bix1], psym=6, symsize=0.5, color=150
xyouts,  90, -5, string(bn0, format='("Abondoned: ",I5)'), color=50
xyouts, -30, -5, string(bn0, format='("New plan: ",I5)'), color=150
device, /close


readcol,'nowt_field_tag.txt',f_id,f_ra,f_dec,f_gb, f_gl, f_tag, format='i,f,f,f,f,i', count=nf

ixf1 = where(f_tag eq 1, n_f1)
ixf0 = where(f_tag eq 0, n_f0)

gl=findgen(37)*10
gb=fltarr(37)
glactc, gra,gdec,2000,gl,gb,2,/deg

device, file='field.xao.S.eps',  /encapsulated, /color, xsize=30, ysize=18
map_set, /moll, /grid, reverse=1,limit=[-5,0,90,360],title='NOWT Fields', label=3,lonlab=-8,latlab=90
oplot, f_ra[ixf1]-180, f_dec[ixf1], psym=6, symsize=0.5, color=250
oplot, f_ra[ixf0]-180, f_dec[ixf0], psym=6, symsize=0.5, color=150
oplot, gra-180, gdec
ln = 185-135+1 & lra = 135+findgen(ln)-180 & ldec = 65+fltarr(ln)
oplot, lra, ldec, color=0,thick=3
ln = 65+1+1 & lra = 135-fltarr(ln)-180 & ldec = 65-findgen(ln)
oplot, lra, ldec, color=0,thick=3
ln = 90+1+1 & lra = 185-fltarr(ln)-180 & ldec = 90-findgen(ln)
oplot, lra, ldec, color=0,thick=3

ln = 30-0+1 & lra = 0+findgen(ln)-180 & ldec = 30+fltarr(ln)
oplot, lra, ldec, color=0,thick=3
ln = 30+1+1 & lra = 30-fltarr(ln)-180 & ldec = 30-findgen(ln)
oplot, lra, ldec, color=0,thick=3

ln = 359-330+1 & lra = 359-findgen(ln)-180 & ldec = 30+fltarr(ln)
oplot, lra, ldec, color=0,thick=3
ln = 30+1+1 & lra = 330-fltarr(ln)-180 & ldec = 30-findgen(ln)
oplot, lra, ldec, color=0,thick=3

device, /close


;图片说明：

;南山原计划共有23384天区（视场），每个天区按照1＊1度规划。
;扣除春夏季，以及赤纬－1度以下部分，还剩10969天区。
;扣除SDSS已经观测过的天区，还剩6654天区需要观测。
;扣除SDSS天区时，并非直接扣除已观测部分，而是给定了一个范围，实际计划观测天区与SDSS已观测部分有重叠。
;指定的扣除范围为：北部扣除 135 < RA < 180 AND DEC < 65 部分，南部扣除 330 < RA < 30 AND DEC < 30 。
;在图中黑线框起来的部分。

;南山图图例：蓝色：扣除的春夏季和南天部分；红色：SDSS部分；绿色：计划观测。

;BOK望远镜计划共有27399天区，每天区按照0.8*0.8度规划。
;扣除春夏季，还剩17125天区。

;Bok图例：蓝色：扣除的春夏季天区；绿色：计划观测。
