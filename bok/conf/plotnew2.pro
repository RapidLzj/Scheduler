readcol, 'field.xao.txt', xid0, xra0, xdec0, xgl0, xgb0, format='l,f,f,f,f', count=n0
readcol, 'field.xao.new.txt', xid1, xra1, xdec1, xgl1, xgb1, format='l,f,f,f,f'
readcol, 'field.xao.sdss.txt', xid2, xra2, xdec2, xgl2, xgb2, format='l,f,f,f,f', count=xn2

match, xid0, xid1, xix1, xix11
match, xid0, xid2, xix2, xix22

status = intarr(n0)
status[xix1] = 1
status[xix2] = 2

forprint,text='field.xao.out.txt', xid0, xra0, xdec0, xgl0, xgb0, status, $
    format='(I-5,4(2x,F9.5),2x,I1)',comment='ID RA DEC GL GB ST'


readcol, 'field.bok.txt', bra0, bdec0, bid0, bgl0, bgb0, format='f,f,l,x,f,f', count=n0
readcol, 'field.bok.new.txt', bid1, bra1, bdec1, bgl1, bgb1, format='l,f,f,f,f', count=bn1

match, bid0, bid1, bix1, bix11
status = intarr(n0)
status[bix1] = 1

forprint,text='field.bok.out.txt', bid0, bra0, bdec0, bgl0, bgb0, status, $
    format='(I-5,4(2x,F9.5),2x,I1)',comment='ID RA DEC GL GB ST'

