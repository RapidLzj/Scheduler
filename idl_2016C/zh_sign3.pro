function zh_sign3, a
	s = fix(a)
	ix = where(a gt 0, nix) & if nix gt 0 then s[ix] =  1
	ix = where(a eq 0, nix) & if nix gt 0 then s[ix] =  0
	ix = where(a lt 0, nix) & if nix gt 0 then s[ix] = -1
	return, s
end
