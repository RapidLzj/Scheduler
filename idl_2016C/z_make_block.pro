pro z_make_block, outpath, blocksize

  if ~keyword_set(outpath)   then outpath   = 'conf/'
  if ~keyword_set(blocksize) then blocksize = 5
  
  readcol, outpath + 'field_all.txt', fid, fra, fdec, format='I,F,F', count=fdn
  fid = [fid, 0] & fra = [fra, -1] & fdec = [fdec, 100]
  
  openw, 11, outpath + 'block_all.txt'
  plot, [0],[0], xr=[0,360],yr=[-40,90]
  
  ix = lonarr(blocksize) - 1
  ; init block
  bid = 0L
  ix[0] = 0
  lastix = 0
  bsize = 1
  rascale = cos(fdec[lastix] * !dpi / 180.0d)
  
  fmt = '(I5, 2(3X,F9.5), (3X,I2,1X), '+strn(blocksize)+'(2X,I6))' 
  for ff = 1, fdn do begin ; last field is virtual
    if bsize ge blocksize or $
        fdec[ff] - fdec[lastix] gt 0.1 or fra[ff] - fra[lastix] gt 5.0 / rascale then begin
      ; out a block
      bid ++
      bra  = median(fra [ix[0:bsize-1]])
      bdec = median(fdec[ix[0:bsize-1]])
      printf, 11, bid, bra, bdec, bsize, fid[ix], format=fmt
      oplot,[bra], [bdec], psym=2
      ; begin new block
      ix[*] = fdn
      bsize = 0
      rascale = cos(fdec[ff] * !dpi / 180.0d)
    endif
    ; put field into current block
    ix[bsize] = ff
    bsize ++
    lastix = ff    
  endfor
  
  close, 11
  print, bid, outpath + 'block_all.txt', format='(I6, " blocks generated in ",A)'
end