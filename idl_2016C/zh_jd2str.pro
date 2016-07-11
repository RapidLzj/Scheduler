function zh_jd2str, jd, tz, mode
  if ~keyword_set(tz) then tz = 0.0d
  if ~keyword_set(mode) then mode = 0
  if jd lt 0 then return, '-'

  caldat, (jd + tz / 24.0d), mn, dy, yr, hr, mi, se
  case mode of
       1: return, string(            hr, mi, se, format='(                           I2.2,":",I2.2,":",I2.2)')
       2: return, string(            hr, mi,     format='(                           I2.2,":",I2.2         )')
    else: return, string(yr, mn, dy, hr, mi, se, format='(I4.4,"-",I2.2,"-",I2.2," ",I2.2,":",I2.2,":",I2.2)')
  endcase
end
