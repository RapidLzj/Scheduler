pro z_schedule, outfile, yr, mn, lat, lon, ele, site, timezone
  if ~keyword_set(ele) then ele = 1500
  if ~keyword_set(site) then site = zh_hms(lon, len=9) + ' ' + zh_hms(lat, len=9)
  if ~keyword_set(timezone) then timezone = round(lon / 15.0)
  
  case mn of
    2:    nday = yr mod 4 eq 0 ? 29 : 28
    4:    nday = 30
    6:    nday = 30
    9:    nday = 30
    11:   nday = 30
    else: nday = 31
  endcase
  
  jdsunset = dblarr(nday)
  jdsunris = dblarr(nday)
  jdsettwi = dblarr(nday)
  jdristwi = dblarr(nday)
  jdmoonris = dblarr(nday)
  jdmoonset = dblarr(nday)
  moonphase = dblarr(nday)
  
  for d = 0, nday-1 do begin
    zh_sunmoon, yr, mn, d+1, lat, lon, ele=ele, $
      jdsunset1, jdsunris1, jdsettwi1, jdristwi1, jdmoonris1, jdmoonset1, moonphase1
    
    jdsunset [d] = jdsunset1
    jdsunris [d] = jdsunris1
    jdsettwi [d] = jdsettwi1
    jdristwi [d] = jdristwi1
    jdmoonris[d] = jdmoonris1
    jdmoonset[d] = jdmoonset1
    moonphase[d] = moonphase1
  endfor
  
  openw, 11, outfile
  
  printf, 11, site, yr, mn, format='("Observation Schedule of ",A, "  ( ",I4.4,"-",I2.2," )")'
  printf, 11, zh_hms(lon, len=12), zh_hms(lat, len=12), format='("Site LON&LAT: ", A, 1X,A)'
  printf, 11, ''
  printf, 11, 'Date', 'Moon%', 'SunSet', 'Twilight', 'Twilight', 'SunRise', 'MoonRise', 'MoonSet', $
    format='(A10, 2X, A5, 6(2X,A8))'
  for d = 0, nday-1 do begin
    printf, 11, yr, mn, d+1, moonphase[d]*100.0, $
      zh_jd2str(jdsunset[d], timezone, 1), $
      zh_jd2str(jdsettwi[d], timezone, 1), $
      zh_jd2str(jdristwi[d], timezone, 1), $
      zh_jd2str(jdsunris[d], timezone, 1), $
      zh_jd2str(jdmoonris[d], timezone, 1), $
      zh_jd2str(jdmoonset[d], timezone, 1), $
      format='(I4.4,"-",I2.2,"-",I2.2, 2X, F5.1, 6(2X,A8))'
  endfor
  
  close, 11
end