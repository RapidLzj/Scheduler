pro zh_plotairmass, file, ra, dec, airm, ix
	;set_plot, 'ps'
	;loadct, 39
	device, file=file, $
		/color,bits_per_pixel=16,xsize=24,ysize=12, $
		/encapsulated,yoffset=0,xoffset=0,/TT_FONT,/helvetica,/bold,font_size=10
    !p.multi = 2

	map_set, /grid, /mollweide, limit=[-10,-180,90,180], $
		/noborder, /label, latlab=-180, lonlab=-8, londel=30, latdel=10, reverse=1, $
		position=[0.03,0.03, 0.95, 0.95], $
		title='Estimated Airmass'

	n = n_elements(airm)
	for k = 0, n-1 do begin
	    if finite(airm[k]) then $
    	    polyfill, ra[k] + 3.0 * [0, 1, 1, 0, 0], dec[k] + 0.7 * [0, 0, 1, 1, 0], $
	            color=fix((airm[k]-1.0)*100)<254 $
	    else $
	        oplot, [ra[k]], [dec[k]], psym=1
	endfor
	oplot, ra[ix] + 3.0 * [0, 1, 1, 0, 0], dec[ix] + 0.9 * [0, 0, 1, 1, 0], $
	    color=254, thick=3

	plot, [0],[0], xr=[0,5], yr=[0,255], xs=1+4, ys=1+4, position=[0.9,0.75, 0.93, 0.95]
	for k = 0, 254 do polyfill, [0, 5, 5, 0, 0], k+[0, 0, 1, 1, 0], color=k
	for k = 1.0, 3.5, 0.5 do xyouts, 5, (k-1)*100, string(k, format='(F3.1)')

	device, /close

	!p.multi = 0
	;set_plot, 'x'
end