readcol,'field.txt',id,ra,de,gl,gb,bk,format='i,f,f,f,f,a'
ubk = bk[uniq(bk,sort(bk))]
nu = n_elements(ubk)
cl=['0000ff'xl,'00ff00'xl,'ff0000'xl,'00ffff'xl,'ff00ff'xl,'ffff00'xl]

map_set, /moll,/grid
for i=0,nu-1 do begin $
ix=where(bk eq ubk[i]) & $
oplot,180-ra[ix],de[ix],psym=6,color=cl[i mod 6] &$
end
