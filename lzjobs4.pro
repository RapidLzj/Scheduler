PRO obs4
; input the data for each survey field.
  kph=31.0+57.8/60.0            ;latitude of Kitt Peak, in degree
  kph=kph*!dtor

  mdir='uvby-users'
  fdir='data/field'
  field_file='s82.field'
  hdir=file_expand_path('')
  hp=strpos(hdir,mdir)
  fpath=''
  IF (hp LT 0)THEN BEGIN        ;not in uvby-users directory
     print,'You should use this code in a directory named '+mdir
     print,'Please input the full path to the file '+field_file
     read, fpath
     fpath=filepath(field_file,root_dir=fpath)
  ENDIF ELSE BEGIN
     hdir=strmid(hdir,0,hp)
     fpath=filepath(field_file,root_dir=hdir+mdir,subdirectory=fdir)
  ENDELSE
  rdf,fpath,nf,ras,des,id1,id2 ; 读所有field的信息，ra，dec，id1 编号，id2 不知道啥
  ras2=ras/15.0
  ids=where(ras2 LT 12.0)
  ras2[ids]=ras2[ids]+24.0 ; ras2，赤经转小时，12--36？？
  des2=des*!dtor ; des2 赤纬转弧度

  cal_file='obs_time.input'
  lh1=0
  lm1=0
  lh2=0
  lm2=0
  oyear=0
  omon=0
  oday=0
  openr,lun,cal_file,/get_lun
  readf,lun,format='(3i0)',oyear,omon,oday
  readf,lun,format='(i2,1x,i2,1x,i2,1x,i2)',lh1,lm1,lh2,lm2
  free_lun,lun
  sunt1=lh1+lm1/60.0 ; 观测时间小时表达
  sunt2=lh2+lm2/60.0
  cht,oyear,omon,oday,sunt1,lst1 ;转恒星时
  cht,oyear,omon,oday,sunt2,lst2
  IF (lst1 LT 12.0) THEN BEGIN
     lst1=lst1+24.0
  ENDIF
  sunt20=sunt2+24.0
  lst20=lst2+24.0 ;转12-36小时制

  nmon=[1,2,3,4,5,6,7,8,9,10,11,12]
  mon=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  ids=where(omon EQ nmon)
  mono=mon[ids]

;; 每一次观测的分钟数
;  dt0=16.0                      ;4 filter-expo in minutes for each field + readout time=5+5+1+1+1*4
  ;dt0=(60.0+6.0+60.0*2)/60
;  dt0=(40.0+3.0+60.0*2)/60  ;20151203 fan required 40+3
;  dt0 = (60.0+40.0)/60.0 ; 20160303 fan required 60
dt0 = (60.0 + 40.0 + 45.0 * 2) / 60  ; 20160722, simulation for both u and v

;4 filter-expo in minutes for each field + readout time=1./6+1./6+1+1+1*4
;; 大气质量和时角限制
  ;limair=1.5                    ;maximum airmass for the field can be observed
  ;limhr=3.5                     ;minimum hour angle for the field can be observed
  limair = 1.8 & limhr = 5.0  ;lzj 20160722 simulation
  bpath=filepath('block.fns',root_dir=hdir+mdir,subdirectory='data/block')
  readcol,bpath,F='X,I',FF
  maxf=max(FF)
  maxb=14*60.0/dt0/maxf         ;max 14 hours for a night
;  len0=6 ;the length of the name of block, if it is 6, the initial block name is used, if it is 7 then indicates this block has been divided into more subblock in the following survey observation.
  len0=8                        ;for the new version

  tmp=''
  bt0=0.0                      ; the time should be used between two block for observation.

  block_file='../prepare/block.new'
  block_file_origin='block.sur'
  lun=33
  openr,lun,block_file
  lun2=44
  openw,lun2,block_file_origin
  copy_lun,lun,lun2
  free_lun,lun
  free_lun,lun2
  kkk='-'+string(oyear,'(i4)')+'-'+mono+'-'+string(oday,'(i2.2)')
  block_file_finish='block_fn.fis'+kkk
  tm_file='block_tm.fis'+kkk
  air_file='simu.air'+kkk
  output_file='simu.block'+kkk
  openw,lun_finish,block_file_finish,/get_lun
  openw,lun_output,output_file,/get_lun
  openw,lun_tm,tm_file,/get_lun
  openw,lun_air,air_file,/get_lun
  endf=-1
  bnf=0                         ;the number of field observed at all night
  obsb=strarr(maxb)
  mair=fltarr(maxb)
  bestb=fltarr(maxb)
  bestr=fltarr(maxb)
  bestd=0
  bnf0=0                        ; the number of field observed at each night

;  lun=33
;  openr,lun,block_file_origin
;  lun2=44
;  openw,lun2,block_file_origin+'-backup'
;  copy_lun,lun,lun2
;  free_lun,lun
;  free_lun,lun2

  print,'         **************************************'
  print,format='(a,i4,3a,i2.2,a)','       ***  observation plan for ',oyear,'-',mono,'-',oday,'  ***'
  print,'         **************************************'
  f0=-1                         ; the number of block observed at each night
  t10=lst1*60.0                 ;the begining time for one night,in min of LST
  t20=lst20*60.0                ;the finish time for one night,in min of LST

  REPEAT BEGIN
     rdb,block_file_origin,maxf,nb,idb,nnb,fnb ;read block.sur
                                ;idb=block name  ;nnb=field number of
                                ;the block   ;fnb= field names array
                                ;of this file

     IF (nb EQ 0) THEN BEGIN    ;no fields in block.sur
        endf=endf+1
     ENDIF
     IF (f0 EQ -1 AND endf LT 1) THEN BEGIN
        printf,lun_tm,format='(a,i4,3a,i2.2)','#  ',oyear,'-',mono,'-',oday
        print,"year=",oyear
        print,format='(a)',"For this night, we've found"
     ENDIF
;input the block data from a file which include all blocks that don't observed before.
; nb=number of blocks can be observed
; idb=name of each block
; nnb=number of fields in each block
; fnb=name of each field in each block
        ;; 开始选天区
     IF (nb GT 0) THEN BEGIN    ;There are observable blocks
        nnb2=intarr(nb)
        fnb2=intarr(maxf,nb) 每个区块每个视场的编号
        airx=fltarr(maxf,nb) 每个区块每个视场的大气质量
        xm=fltarr(nb)
        rasb=fltarr(nb)
        desb=fltarr(nb)
        t2x=fltarr(nb)
        FOR j=0,nb-1 DO BEGIN   ;for each block
           nnb0=nnb[j]          ;number of field 本区块的视场数
           t1x1=t10+findgen(nnb0)*dt0 ;time of each field  假设在当前时间t10下，观测这个区块的每个视场的时间
           idt=where(t1x1 LE t20,count) ;field name before the finishing time 选择能够完成的部分（最后一个区块往往来不及完成）
           fnb0=fnb[idt,j]              ;save in an array 该区块的视场编号
           nnb0=count                   ;number of usable field
           ras0=fltarr(nnb0)
           des0=fltarr(nnb0)
           t1x=fltarr(nnb0) ;可观测视场的坐标和假设时间
           FOR k=0,nnb0-1 DO BEGIN ;for each usable field
              ids=where(fnb0[k] EQ id1) ;
              ras0[k]=ras2[ids]         ;ra of the field
              des0[k]=des2[ids]         ;dec of the field
              t1x[k]=t10+k*dt0  ;planing observing time (in LST) of the field
           ENDFOR
           desb[j]=des0[0]      ; the declination of each block. 每个区块的赤纬，以第一个视场的为准
           IF (nnb0 GT 0) THEN BEGIN ;there are obsevable fields 每个区块的赤经，均值
              rasb[j]=mean(ras0)     ;mean ra of the block
           ENDIF ELSE BEGIN
              rasb[j]=ras0[0]
           ENDELSE
           x1=sin(kph)*sin(des0)
           x2=cos(kph)*cos(des0) ; 计算大气质量（不知道公式出处），计算每个视场的大气质量
           hr=t1x/60.0-ras0     ; calcualte the hour angle at the given observation time
                                ; for the corresponding field, ( the sequence of field assumed is same as the time)
           x=1.0/(x1+x2*cos(hr*15.0*!dtor)) ; calculate the airmass for the field at the observation time.
           idx=where(x GT 0 AND x LE limair,count)
           IF (count GT 0)THEN BEGIN ;there are obsevable field with airmass
              nnb2[j]=count          ;number of obsevable field with airmass
              airx[idx,j]=x[idx]     ;airmass array
              xm[j]=median(x[idx])   ;mean airmass 计算出该视场的平均大气质量
              fnb2[idx,j]=fnb0[idx] ;block name of obsevable field with airmass
              t2x[j]=t1x[count-1]   ;latest observing time of the block 本区块的观测结束时间
           ENDIF ELSE BEGIN
              nnb2[j]=0
              xm[j]=20
           ENDELSE
        ENDFOR ; 在当前时间，每个可用区块都假设观测一次，求观测的各种参数

        ids=where(nnb2 GT 0 AND airx[0,*] GT 0,nids) 可用区块
        IF (nids LT 1) THEN BEGIN
           IF (f0 EQ -1) THEN BEGIN
              print,'Improper begining time, because no field can be observed at this time!!'
           ENDIF ELSE BEGIN
              print,'no field can be observe before this night finish!'
           ENDELSE
           t10=t20+2.0
        ENDIF ELSE BEGIN  ;开始从可用区块中选择合适的区块
           minde=min(desb[ids]) ; lowest dec block
           ids2=where(abs(desb[ids]-minde) LT 4.0*!dtor,nids)  ;4 deg range dec variation 限制在最低可用的dec之上4度
           irasb=sort(rasb[ids[ids2]])                         ;sorted mean ra
           idesb=sort(desb[ids[ids2]])                         ;sorted dec
           ixm=sort(xm[ids[ids2]])                             ;sorted airmass
           wt=fltarr(nids)
           FOR k=0,nids-1 DO BEGIN
              wt[k]=k           ;number
              idsir=where(irasb EQ ixm[k]) ;找出大气质量第k小的天区的赤经的编号
              wt[k]=wt[k]+idsir            ;smallest ra  大气质量排名+对应赤经排名+对应赤纬排名
              idsid=where(idesb EQ ixm[k]) ;
              wt[k]=wt[k]+idsid            ;smallest dec
           ENDFOR

           minw=min(wt)         ;both smallest ra and smallest dec 赤经排名+赤纬排名+大气质量排名，最小的
           ids3=where(wt EQ minw) ;best block
           minx=min(xm[ids[ids2[ixm[ids3]]]]) ;smallest airmass 最佳区块的大气质量
           ids4=where(xm[ids[ids2[ixm[ids3]]]] EQ minx,nmm) ;
           obidb=ids[ids2[ixm[ids3[ids4[0]]]]]最佳区块的最原始列表下标
;           print,'bestd=',bestd
           ids2=where(desb[obidb] EQ bestb[0:bestd],nmb)
           IF (nmb GT 0) THEN BEGIN
              maxbr=max(bestr[ids2])
              maxbd=desb[obidb]
              IF (rasb[obidb] LT maxbr) THEN BEGIN
                 ids2=where(desb[ids] NE maxbd,nids)
                 IF (nids GT 0) THEN BEGIN
                    irasb=sort(rasb[ids[ids2]])
                    idesb=sort(desb[ids[ids2]])
                    ixm=sort(xm[ids[ids2]])
                    wt=fltarr(nids)
                    FOR k=0,nids-1 DO BEGIN
                       wt[k]=k
                       idsir=where(irasb EQ ixm[k])
                       wt[k]=wt[k]+idsir
                       idsid=where(idesb EQ ixm[k])
                       wt[k]=wt[k]+idsid
                    ENDFOR
                    minw=min(wt)
                    ids3=where(wt EQ minw)
                    minx=min(xm[ids[ids2[ixm[ids3]]]])
                    ids4=where(xm[ids[ids2[ixm[ids3]]]] EQ minx)
                    obidb=ids[ids2[ixm[ids3[ids4[0]]]]]
                 ENDIF
              ENDIF
           ENDIF
           bestb[bestd]=desb[obidb]
           bestr[bestd]=rasb[obidb]
           bestd=bestd+1
           print,format='(a,i3,a)'," the ",bestd,"th block ..."
           if bestd ge maxb-2 then break

           IF (nnb2[obidb] EQ nnb[obidb])THEN BEGIN
; the whole origin block can be observed
              lun=77
              openw,lun,block_file_origin
              FOR j=0,nb-1 DO BEGIN
                 IF (j NE obidb) THEN BEGIN
                    printf,lun,format='(a'+string(len0+1,'(i1)')+',i3,a3,'+string(nnb[j])+'i6)',idb[j],nnb[j],'**',fnb[0:nnb[j]-1,j]
;                    print,j,' ',idb[j]
                 ENDIF
              ENDFOR
              free_lun,lun

              j=obidb
              printf,lun_finish,format='(a'+string(len0+1,'(i1)')+',i3,a3,'+string(nnb[j])+'i6)',idb[j],nnb[j],'**',fnb[0:nnb[j]-1,j]
              printf,lun_tm,format='(a'+string(len0+1,'(i1)')+',i3,a3,2f8.2,'+string(nnb[j])+'f6.2)', idb[j],nnb[j],'**', $
                     t10,t2x[j],airx[0:nnb[j]-1,j]
              bnf0=bnf0+nnb[j]
              f0=f0+1
              obsb[f0]=idb[j]
              mair[f0]=mean(airx[0:nnb[j]-1,j])
           ENDIF ELSE BEGIN
; part of the origin block can be observed
              idb0=idb[obidb]
              ss=strcompress(idb0,/remove_all)
              len=strlen(ss)
              IF (len EQ len0)THEN BEGIN
                 idb01=ss+string(1,'(i1)')
                 printf,lun_finish,format='(a'+string(len0+1,'(i1)')+',i3,a3,'+string(nnb2[obidb])+'i6)',idb01,nnb2[obidb],'**', $
                        fnb2[0:nnb2[obidb]-1,obidb]
                 printf,lun_tm,format='(a'+string(len0+1,'(i1)')+',i3,a3,2f8.2,'+string(nnb2[obidb])+'f6.2)', $
                        idb01,nnb2[obidb],'**',t10,t2x[obidb],airx[0:nnb2[obidb]-1,obidb]
                 f0=f0+1
                 obsb[f0]=idb01
                 mair[f0]=mean(airx[0:nnb2[obidb]-1,obidb])
                 bnf0=bnf0+nnb2[obidb]
                 idb02=ss+string(2,'(i1)')
                 ids=where(airx[0:nnb[obidb]-1,obidb] EQ 0)
                 fnb0=fnb[ids,obidb]
                 n0=n_elements(ids)
                 lun=88

                 openw,lun,block_file_origin
                 FOR j=0,nb-1 DO BEGIN
                    IF (j NE obidb) THEN BEGIN
                       printf,lun,format='(a'+string(len0+1,'(i1)')+',i3,a3,'+string(nnb[j])+'i6)',idb[j],nnb[j],'**',fnb[0:nnb[j]-1,j]
;                       print,j,' ',idb[j]
                    ENDIF ELSE BEGIN
                       printf,lun,format='(a'+string(len0+1,'(i1)')+',i3,a3,'+string(n0)+'i6)',idb02,n0,'**',fnb0
                    ENDELSE
                 ENDFOR
                 free_lun,lun
              ENDIF ELSE BEGIN
                 bl0=0
                 idb01=idb0
                 printf,lun_finish,format='(a'+string(len0+1,'(i1)')+',i3,a3,'+string(nnb2[obidb])+'i6)',idb01,nnb2[obidb],'**', $
                        fnb2[0:nnb2[obidb]-1,obidb]
                 printf,lun_tm,format='(a'+string(len0+1,'(i1)')+',i3,a3,2f8.2,'+string(nnb2[obidb])+'f6.2)', $
                        idb01,nnb2[obidb],'**',t10,t2x[obidb],airx[0:nnb2[obidb]-1,obidb]
                 f0=f0+1
                 obsb[f0]=idb01
                 mair[f0]=mean(airx[0:nnb2[obidb]-1,obidb])
                 bnf0=bnf0+nnb2[obidb]
                 reads,idb0,format='('+string(len0)+'x,i1)',bl0
                 idb02=strmid(ss,0,len0)+string(bl0+1,'(i1)')
                 ids=where(airx[0:nnb[obidb]-1,obidb] EQ 0)
                 fnb0=fnb[ids,obidb]
                 n0=n_elements(ids)
                 lun=88
                 openw,lun,block_file_origin
                 FOR j=0,nb-1 DO BEGIN
                    IF (j NE obidb) THEN BEGIN
                       printf,lun,format='(a'+string(len0+1,'(i1)')+',i3,a3,'+string(nnb[j])+'i6)',idb[j],nnb[j],'**',fnb[0:nnb[j]-1,j]
                    ENDIF ELSE BEGIN
                       printf,lun,format='(a'+string(len0+1,'(i1)')+',i3,a3,'+string(n0)+'i6)',idb02,n0,'**',fnb0
                    ENDELSE
                 ENDFOR
                 free_lun,lun
              ENDELSE

           ENDELSE
           t10=bt0+dt0+t2x[obidb]
        ENDELSE
     ENDIF ELSE BEGIN
        print,'There is no any field in the input file!'
        t10=t20+2.0
     ENDELSE
  ENDREP UNTIL (t10 GT t20)
  IF (endf LT 1)THEN BEGIN
     IF (f0+1 GT 0) THEN BEGIN
        printf,lun_output,format='(i4,3a,i2.2,2i5,x,'+string(f0+1)+'a9)',oyear,'-',mono,'-',oday,f0+1,bnf0,obsb[0:f0]
;        print,bnf0,obsb[0:f0]
        printf,lun_air,format='(i4,3a,i2.2,2i5,'+string(f0+1)+'f6.2)',oyear,'-',mono,'-',oday,f0+1,bnf0,mair[0:f0]
        bnf=bnf+bnf0
     ENDIF ELSE BEGIN
        printf,lun_output,format='(i4,3a,i2.2,i5)',oyear,'-',mono,'-',oday,f0+1
     ENDELSE
  ENDIF
  free_lun,lun_finish
  free_lun,lun_output
  free_lun,lun_tm
  free_lun,lun_air
  print,format='(a,i5)','the total number of observed fields for this night is',bnf
END
