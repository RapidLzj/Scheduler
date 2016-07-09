readcol, 'field.xao.txt', xid0, xra0, xdec0, xgl0, xgb0, format='l,f,f,f,f', count=n0
readcol, 'field.xao.new.txt', xid1, xra1, xdec1, xgl1, xgb1, format='l,f,f,f,f'
readcol, 'field.xao.sdss.txt', xid2, xra2, xdec2, xgl2, xgb2, format='l,f,f,f,f'

match, xid0, xid1, xix1, xix11
match, xid0, xid2, xix2, xix22
status = intarr(n0)
status[xix1] = 1
status[xix2] = 2
xix0 = where(status eq 0)
xix1 = where(status eq 1)

set_plot, 'ps'
loadct, 39
device, file='field.xao.A.eps',  /encapsulated, /color, xsize=30, ysize=18
map_set, /moll, /grid, /noborder, limit=[-20,0,90,360], reverse=1
oplot, xra0[xix0], xdec0[xix0], psym=6, symsize=0.5, color=50
oplot, xra0[xix1], xdec0[xix1], psym=6, symsize=0.5, color=250
oplot, xra0[xix2], xdec0[xix2], psym=6, symsize=0.5, color=150
device, /close

device, file='field.xao.B.eps',  /encapsulated, /color, xsize=30, ysize=18
map_set, /moll, /grid, /noborder, limit=[-20,0,90,360], reverse=1
oplot, xra0[xix0]-180, xdec0[xix0], psym=6, symsize=0.5, color=50
oplot, xra0[xix1]-180, xdec0[xix1], psym=6, symsize=0.5, color=250
oplot, xra0[xix2]-180, xdec0[xix2], psym=6, symsize=0.5, color=150
device, /close

device, file='field.xao.G.eps',  /encapsulated, /color, xsize=30, ysize=18
map_set, /moll, /grid, /noborder, reverse=1
oplot, xgl0[xix0], xgb0[xix0], psym=6, symsize=0.5, color=50
oplot, xgl0[xix1], xgb0[xix1], psym=6, symsize=0.5, color=250
oplot, xgl0[xix2], xgb0[xix2], psym=6, symsize=0.5, color=150
device, /close

readcol, 'field.bok.txt', bra0, bdec0, bid0, bgl0, bgb0, format='f,f,l,x,f,f', count=n0
readcol, 'field.bok.new.txt', bid1, bra1, bdec1, bgl1, bgb1, format='l,f,f,f,f'

match, bid0, bid1, bix1, bix11
status = intarr(n0)
status[bix1] = 1
bix0 = where(status eq 0)

set_plot, 'ps'
loadct, 39
device, file='field.bok.A.eps',  /encapsulated, /color, xsize=30, ysize=18
map_set, /moll, /grid, /noborder, limit=[-5,0,90,360], reverse=1
oplot, bra0[bix0], bdec0[bix0], psym=6, symsize=0.5, color=50
oplot, bra0[bix1], bdec0[bix1], psym=6, symsize=0.5, color=150
device, /close

device, file='field.bok.B.eps',  /encapsulated, /color, xsize=30, ysize=18
map_set, /moll, /grid, /noborder, limit=[-5,0,90,360], reverse=1
oplot, bra0[bix0]-180, bdec0[bix0], psym=6, symsize=0.5, color=50
oplot, bra0[bix1]-180, bdec0[bix1], psym=6, symsize=0.5, color=150
device, /close

device, file='field.bok.G.eps',  /encapsulated, /color, xsize=30, ysize=18
map_set, /moll, /grid, /noborder, reverse=1
oplot, bgl0[bix0], bgb0[bix0], psym=6, symsize=0.5, color=50
oplot, bgl0[bix1], bgb0[bix1], psym=6, symsize=0.5, color=150
device, /close
