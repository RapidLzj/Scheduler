openr, 1, '/data/dr12/radec.txt'

sdssmap = bytarr(3600,1000) ; 360*10(0~359.9),100*10(-10~90)

line = ''
c = 0ll
while not eof(1) do begin & $
    readf, 1, line & $
    p = strsplit(line, ',', /ex) & $
    r = fix(p[1] * 10) & d = fix((p[2] + 10) * 10) & $
    if r ge 0 and r lt 3600 and d ge 0 and d lt 1000 then $
        sdssmap[r, d] = 1 & $
    c ++ & $
    if c mod 1000 eq 0 then print, c, total(sdssmap) & $
endwhile

close, 1

print, c, total(sdssmap)

openw, 1, 'sdss_map.txt'
for r = 0, 3600-1 do $
    for d = 0, 1000-1 do $
        printf, 1, r/10.0, d/10.0-10.0, sdssmap[r,d], format='(f5.1,2x,f5.1,2x,i1)'
close, 1


