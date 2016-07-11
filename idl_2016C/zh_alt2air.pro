function zh_alt2air, alt
    air = fltarr(n_elements(alt)) + 'nan'
    ix = where(alt gt 0, nix)
    if nix gt 0 then air[ix] = 1.0 / sin(( alt[ix] + 244.0 /(165.0 + 47.0 * alt[ix] ^ 1.1) ) * !pi / 180.d)
    return, air
end