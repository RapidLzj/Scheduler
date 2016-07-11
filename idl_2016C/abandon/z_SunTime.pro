pro z_SunTime, jd, site_lon, site_lat, sunset, sunris, limit=limit
  step = [7200.0d, 720.0d, 72.0d, 7.2d, 0.72d] / 3600.0 / 24.0  ; seconds to days
  scnt = [6, 11, 11, 11, 11]
  
  ; start grid point of 
  sunset = jd
  sunris = jd
  for ss = 0, 4 do begin ; 5 levels
    ; grid of test
    grid = findgen(scnt[ss]) * step[ss]
    setgrid = sunset - grid
    risgrid = sunris + grid
    ; sun alt of each grid point
    sunpos, setgrid, setra, setdec
    sunpos, risgrid, risra, risdec
    eq2hor, setra, setdec, setgrid, setalt, setaz, lat=site_lat, lon=site_lon, alt=0
    eq2hor, risra, risdec, risgrid, risalt, risaz, lat=site_lat, lon=site_lon, alt=0
    ; find the max alt of underground, this is the limit point of sunset and sunrise
    sunset = (setgrid[where(setalt eq max(setalt[where(setalt le limit)]))])[0]
    sunris = (risgrid[where(risalt eq max(risalt[where(risalt le limit)]))])[0]
    print, z_jd2str(sunset, round(site_lon/15), 3), z_jd2str(sunris, round(site_lon/15), 3) $
      ,format='(A,4x,A)'
  endfor
end
