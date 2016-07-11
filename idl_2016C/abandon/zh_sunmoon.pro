pro zh_sunmoon, yr, mn, dy, lat, lon, ele=ele, $
  jdsunset, jdsunris, jdsettwi, jdristwi, jdmoonris, jdmoonset, moonphase
  
  if ~keyword_set(ele) then ele = 1500.0

  ; local midnight julian day
  jd0 = julday(mn, dy, yr, 24 - lon / 15.0d, 0, 0)
  
  jdsunset = zh_sun_findalt(jd0 - 0.4, jd0 - 0.0, lat, lon, ele)
  jdsunris = zh_sun_findalt(jd0 + 0.0, jd0 + 0.4, lat, lon, ele)
  jdsettwi = zh_sun_findalt(jd0 - 0.4, jd0 - 0.0, lat, lon, ele, base=-15.0)
  jdristwi = zh_sun_findalt(jd0 + 0.0, jd0 + 0.4, lat, lon, ele, base=-15.0)
  jdmoon0 = zh_sun_findalt(jd0 - 0.4, jd0 - 0.0, lat, lon, ele, dir0, /moon)
  jdmoon1 = zh_sun_findalt(jd0 + 0.0, jd0 + 0.4, lat, lon, ele, dir1, /moon)
  jdmoonris = -1 & jdmoonset = -1
  if dir0 eq 1 and jdmoon0 gt 0 then jdmoonris = jdmoon0 else jdmoonset = jdmoon0
  if dir1 eq 1 and jdmoon1 gt 0 then jdmoonris = jdmoon1 else jdmoonset = jdmoon1
  
  mphase, jd0, moonphase
end