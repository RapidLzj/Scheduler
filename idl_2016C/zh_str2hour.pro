function zh_str2hour, str, hr0, mi0
	if ~ keyword_set(hr0) then hr0 = 24
	if ~ keyword_set(mi0) then mi0 = 00
	sp = strsplit(str, ':', /ext, /preserve)
	hrs = sp[0]
	if n_elements(sp) ge 2 then mis = sp[1] else mi = '0'
	if ~ strnumber(hrs, hr) then hr = hr0
	if ~ strnumber(mis, mi) then mi = mi0
	if hr lt 12 then hr += 24
	return, hr + mi / 60.0
end