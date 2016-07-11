pro zh_sunalt, jd, lat, lon, ele, ra, dec, alt, az, basealt=basealt, moon=moon
  if ~keyword_set(basealt) then basealt = 0.0d
  if keyword_set(moon) then moonpos, jd, ra, dec else sunpos, jd, ra, dec
  eq2hor, ra, dec, jd, alt, az, lat=lat, lon=lon, alt=ele
  alt -= basealt
end
