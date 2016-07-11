pro z_HeaderInfo, file, sn, object, filter, expt, ra, dec
; Extract header info from fits file
; Alter this procedure for different telescope
    sn     = 0
    object = ''
    filter = ''
    expt   = 0.0
    ra     = 0.0
    dec    = 0.0

    if file_test(file) then begin
        hdr = headfits(file)
        it = strtrim(sxpar(hdr, 'IMAGETYP'), 2)
        if it eq 'object' then begin
            sn     = strmid(file, 8, 4, /reverse) ;sxpar(hdr, 'OBSNUM')
            object = strtrim(sxpar(hdr, 'OBJECT'), 2)
            object = strjoin(strsplit(object, '''', /ext), '')
            filter = strtrim(sxpar(hdr, 'FILTER'), 2)
            expt   = sxpar(hdr, 'EXPTIME')  * 1.0
            ra     = sxpar(hdr, 'OBJCTRA')  * 1.0
            dec    = sxpar(hdr, 'OBJCTDEC') * 1.0
        endif
    endif
end
