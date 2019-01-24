PRO makefappendlist, SNname, tempobsid=tempobsid

spawn, 'ls 0* > J.list'
spawn, "sed '/uvot/d' J.list > J.temp"
spawn, "sed 's/://' J.temp > J.list"
spawn, "sed '/ /d' J.list > targetids"
spawn, "gunzip -f */uvot/image/*img.gz"

dlist='targetids'

aspectfile=SNname+'_idlaspectcommands.txt'
printfile=SNname+'_idlfappendcommands.txt'
exfile=SNname+'_idlexcommands.txt'
openw, lun, printfile, /get_lun
openw, 33, aspectfile

filters=['w2','m2','w1','uu','bb','vv']
;filters=['w2','m2']

goodaspcorsumfiles=strarr(6)
for f=0,n_elements(filters)-1 do goodaspcorsumfiles[f]=SNname+"_"+filters[f]+"_goodsum.img"

for f=0,n_elements(filters)-1 do begin

	filter=filters[f]


	tempfile=SNname+"_"+filter+"_temp.img"
	tempsumfile=SNname+"_"+filter+"_tempsum.img"
	sumoutfile=SNname+"_"+filter+"_sum.img"
	h5outfile=SNname+"_"+filter+"_h5.img"
	h5sumfile=SNname+"_"+filter+"_h5sum.img"
	fulloutfile=SNname+"_"+filter+"_full.img"
	alloutfile=SNname+"_"+filter+"_all.img"
	goodaspcoroutfile=SNname+"_"+filter+"_goodaspcor.img"
	goodaspcorsumfile=SNname+"_"+filter+"_goodsum.img"


	extempfile=SNname+"_"+filter+"_extemp.img"
	extempsumfile=SNname+"_"+filter+"_extempsum.img"
	exsumoutfile=SNname+"_"+filter+"_exsum.img"
	exallsumfilename=SNname+"_"+filter+"_exsum.img"
	exh5outfile=SNname+"_"+filter+"_exh5.img"
	exh5sumfile=SNname+"_"+filter+"_exh5sum.img"
	exfulloutfile=SNname+"_"+filter+"_exfull.img"
	exalloutfile=SNname+"_"+filter+"_exall.img"
	exgoodaspcoroutfile=SNname+"_"+filter+"_exgoodaspcor.img"
	exgoodaspcorsumfile=SNname+"_"+filter+"_exgoodsum.img"

	PRINTF, lun,'rm ' + sumoutfile
	PRINTF, lun,'rm ' + tempfile
	PRINTF, lun,'rm ' + tempsumfile
	PRINTF, lun,'rm ' + h5outfile
	PRINTF, lun,'rm ' + fulloutfile
	PRINTF, lun,'rm ' + alloutfile
	PRINTF, lun,'rm ' + goodaspcoroutfile

	PRINTF, lun,'rm ' + exsumoutfile
	PRINTF, lun,'rm ' + extempfile
	PRINTF, lun,'rm ' + extempsumfile
	PRINTF, lun,'rm ' + exh5outfile
	PRINTF, lun,'rm ' + exfulloutfile
	PRINTF, lun,'rm ' + exalloutfile
	PRINTF, lun,'rm ' + exgoodaspcoroutfile

	readcol, dlist, obsids, format='a'

	nd = N_ELEMENTS(obsids)

	asp = ['']
	binx = [0]
	expose = [0.0]
	skname = ['']
	exname = ['']
	drname = ['']
	ftime = [0.0]
	tstart = [0.0D]
	exten = [0]
	windowdx = [0]

	sumstart=0

	FOR i=0, nd-1 DO BEGIN
		dir = obsids[i] + '/uvot/image/'
		skn = 'sw' + obsids[i] + 'u' + filter + '_sk.img'
		sum = 'sw' + obsids[i] + 'u' + filter + '_sk_sum.img'
		exn = 'sw' + obsids[i] + 'u' + filter + '_ex.img'
		exsum = 'sw' + obsids[i] + 'u' + filter + '_ex_sum.img'
		PRINT, dir + skn

		sumfilename=dir + sum
		exsumfilename=dir + exsum
		sumtest=file_test(sumfilename)
		if sumtest eq 1 and sumstart eq 0 then PRINTF, lun,'fextract '+ sumfilename + ' ' + sumoutfile
		if sumtest eq 1 and sumstart eq 0 then PRINTF, lun,'fextract '+ exsumfilename + ' ' + exsumoutfile
		if sumtest eq 1 and sumstart eq 0 then sumstart=1
		if sumtest eq 1 and sumstart eq 1 then PRINTF, lun,'fappend '+ sumfilename + ' ' + sumoutfile
		if sumtest eq 1 and sumstart eq 1 then PRINTF, lun,'fappend '+ exsumfilename + ' ' + exsumoutfile

; need to check if tempobsid exists first		checktemp=intarr(n_elements(tempobsid))
;		for c=0,n_elements(tempobsid)-1 do	checktemp[c]=strmatch(obsids,tempobsid[c])


		filename=dir + skn
		test=file_test(filename)

		if test eq 1 then begin
			x = MRDFITS(dir + skn,1,h)
			n = N_ELEMENTS(x)

			s = SIZE(FXPAR(h,'ASPCORR'))
			IF s[1] EQ 7 THEN asp = [asp,FXPAR(h,'ASPCORR')] ELSE $
				asp = [asp,STRING(FXPAR(h,'ASPCORR'))]
			binx = [binx,FIX(FXPAR(h,'BINX'))]
			expose = [expose,FLOAT(FXPAR(h,'EXPOSURE'))]
			tstart = [tstart,FLOAT(FXPAR(h,'TSTART'))]
			ftime = [ftime,FXPAR(h,'FRAMTIME')*1000.]
			exten = [exten,1]
			skname = [skname,skn]
			exname = [exname,exn]
			drname = [drname,dir]
			windowdx = [windowdx,FXPAR(h,'WINDOWDX')]
 
			k = 2

			WHILE n GT 1 DO BEGIN
				x = MRDFITS(dir + skn,k,h)
				n = N_ELEMENTS(x)

				IF n GT 1 THEN BEGIN
					s = SIZE(FXPAR(h,'ASPCORR'))
					IF s[1] EQ 7 THEN asp = [asp,FXPAR(h,'ASPCORR')] ELSE $
						asp = [asp,STRING(FXPAR(h,'ASPCORR'))]
					binx = [binx,FIX(FXPAR(h,'BINX'))]
					expose = [expose,FLOAT(FXPAR(h,'EXPOSURE'))]
					ftime = [ftime,FXPAR(h,'FRAMTIME')*1000.]
					tstart = [tstart,FLOAT(FXPAR(h,'TSTART'))]
					exten = [exten,k]
					skname = [skname,skn]
					exname = [exname,exn]
					drname = [drname,dir]
					windowdx = [windowdx,FXPAR(h,'WINDOWDX')]
				ENDIF
			k = k+1
			ENDWHILE
   		endif
	ENDFOR

	narr = N_ELEMENTS(asp)


		PRINT
		PRINT, 'Exposure: ', TOTAL(expose)
		;w = WHERE((asp EQ 'DIRECT  ' OR asp EQ 'UNICORR ') AND binx LE blim, nw)

		h5 = WHERE(ftime lt 4.0 and ftime gt 3.0, nh5)
		full = WHERE(expose gt 8.0 and windowdx eq 2048 and ftime gt 9.9, nfull)
		all = WHERE(expose gt 8.0, nall)
		noaspcor = WHERE(strmatch(asp,'NONE*') eq 1, nnoaspcor)
		goodaspcor = WHERE(strmatch(asp,'NONE*') eq 0  and windowdx eq 2048 and ftime gt 9.9, ngoodaspcor)
;		h5full=h5-1
;		h5all=[h5,h5full]

		if (h5[0] ne -1) then  PRINTF, lun,'fextract '+ drname[h5[0]] + skname[h5[0]] + '+' + STRCOMPRESS(STRING(exten[h5[0]]),/REMOVE_ALL) + ' ' + h5outfile
		if (nh5 ge 2)    then  FOR i=1, nh5-1 DO  PRINTF, lun,'fappend  '+ drname[h5[i]] + skname[h5[i]] + '+' +  STRCOMPRESS(STRING(exten[h5[i]]),/REMOVE_ALL) + ' ' + h5outfile
		if (nh5 ge 2)    then    PRINTF, lun,'uvotimsum '+h5outfile+'  outfile='+h5sumfile+' exclude=none clobber=yes'

		if (full[0] ne -1)  then  PRINTF, lun,'fextract '+ drname[full[0]] + skname[full[0]] + '+' + STRCOMPRESS(STRING(exten[full[0]]),/REMOVE_ALL) + ' ' + fulloutfile
		if (nfull ge 2)     then  FOR i=1, nfull-1 DO  PRINTF, lun,'fappend  '+ drname[full[i]] + skname[full[i]] + '+' +  STRCOMPRESS(STRING(exten[full[i]]),/REMOVE_ALL) + ' ' + fulloutfile

		if (all[0] ne -1)  then  PRINTF, lun,'fextract '+ drname[all[0]] + skname[all[0]] + '+' + STRCOMPRESS(STRING(exten[all[0]]),/REMOVE_ALL) + ' ' + alloutfile
		if (nall ge 2)    then  FOR i=1, nall-1 DO  PRINTF, lun,'fappend  '+ drname[all[i]] + skname[all[i]] + '+' +  STRCOMPRESS(STRING(exten[all[i]]),/REMOVE_ALL) + ' ' + alloutfile
;;
		if (h5[0] ne -1) then  PRINT,'fextract '+ drname[h5[0]] + skname[h5[0]] + '+' + STRCOMPRESS(STRING(exten[h5[0]]),/REMOVE_ALL) + ' ' + h5outfile
		if (nh5 ge 2)    then  FOR i=1, nh5-1 DO  PRINT,'fappend  '+ drname[h5[i]] + skname[h5[i]] + '+' +  STRCOMPRESS(STRING(exten[h5[i]]),/REMOVE_ALL) + ' ' + h5outfile

		if (full[0] ne -1)  then  PRINT, 'fextract '+ drname[full[0]] + skname[full[0]] + '+' + STRCOMPRESS(STRING(exten[full[0]]),/REMOVE_ALL) + ' ' + fulloutfile
		if (nfull ge 2)     then  FOR i=1, nfull-1 DO  PRINT,'fappend  '+ drname[full[i]] + skname[full[i]] + '+' +  STRCOMPRESS(STRING(exten[full[i]]),/REMOVE_ALL) + ' ' + fulloutfile

		if (all[0] ne -1)  then  PRINT,'fextract '+ drname[all[0]] + skname[all[0]] + '+' + STRCOMPRESS(STRING(exten[all[0]]),/REMOVE_ALL) + ' ' + alloutfile
		if (nall ge 2)    then  FOR i=1, nall-1 DO  PRINT,'fappend  '+ drname[all[i]] + skname[all[i]] + '+' +  STRCOMPRESS(STRING(exten[all[i]]),/REMOVE_ALL) + ' ' + alloutfile

		if (ngoodaspcor ge 2)  then  PRINTF, lun,'fextract '+ drname[goodaspcor[1]] + skname[goodaspcor[1]] + '+' + STRCOMPRESS(STRING(exten[goodaspcor[1]]),/REMOVE_ALL) + ' ' + goodaspcoroutfile
		if (ngoodaspcor ge 2)    then  FOR i=2, ngoodaspcor-1 DO  PRINTF, lun,'fappend  '+ drname[goodaspcor[i]] + skname[goodaspcor[i]] + '+' +  STRCOMPRESS(STRING(exten[goodaspcor[i]]),/REMOVE_ALL) + ' ' + goodaspcoroutfile

		if (nnoaspcor ge 2)    then  FOR i=1, nnoaspcor-1 DO  if (skname[noaspcor[i]] ne skname[noaspcor[i-1]])    then  PRINTF, 33, 'perl $SNSCRIPTS/uaspectex.pl  '+ drname[noaspcor[i]] + skname[noaspcor[i]] +  ' coo.reg '  + drname[noaspcor[i]] + exname[noaspcor[i]]

		if (ngoodaspcor ge 2)  then  PRINTF, lun,'uvotimsum '+goodaspcoroutfile+'  outfile='+goodaspcorsumfile+' exclude=none clobber=yes'
		if (ngoodaspcor ge 2)  then  PRINTF, lun,'rm '+goodaspcoroutfile

;;;;;;;;;;;;; exposure maps

		if (h5[0] ne -1) then  PRINTF, lun,'fextract '+ drname[h5[0]] + exname[h5[0]] + '+' + STRCOMPRESS(STRING(exten[h5[0]]),/REMOVE_ALL) + ' ' + exh5outfile
		if (nh5 ge 2)    then  FOR i=1, nh5-1 DO  PRINTF, lun,'fappend  '+ drname[h5[i]] + exname[h5[i]] + '+' +  STRCOMPRESS(STRING(exten[h5[i]]),/REMOVE_ALL) + ' ' + exh5outfile
		if (nh5 ge 2)    then    PRINTF, lun,'uvotimsum '+exh5outfile+'  outfile='+exh5sumfile+' exclude=none clobber=yes'

		if (full[0] ne -1)  then  PRINTF, lun,'fextract '+ drname[full[0]] + exname[full[0]] + '+' + STRCOMPRESS(STRING(exten[full[0]]),/REMOVE_ALL) + ' ' + exfulloutfile
		if (nfull ge 2)     then  FOR i=1, nfull-1 DO  PRINTF, lun,'fappend  '+ drname[full[i]] + exname[full[i]] + '+' +  STRCOMPRESS(STRING(exten[full[i]]),/REMOVE_ALL) + ' ' + exfulloutfile

		if (all[0] ne -1)  then  PRINTF, lun,'fextract '+ drname[all[0]] + exname[all[0]] + '+' + STRCOMPRESS(STRING(exten[all[0]]),/REMOVE_ALL) + ' ' + exalloutfile
		if (nall ge 2)    then  FOR i=1, nall-1 DO  PRINTF, lun,'fappend  '+ drname[all[i]] + exname[all[i]] + '+' +  STRCOMPRESS(STRING(exten[all[i]]),/REMOVE_ALL) + ' ' + exalloutfile
;;
		if (h5[0] ne -1) then  PRINT,'fextract '+ drname[h5[0]] + exname[h5[0]] + '+' + STRCOMPRESS(STRING(exten[h5[0]]),/REMOVE_ALL) + ' ' + exh5outfile
		if (nh5 ge 2)    then  FOR i=1, nh5-1 DO  PRINT,'fappend  '+ drname[h5[i]] + exname[h5[i]] + '+' +  STRCOMPRESS(STRING(exten[h5[i]]),/REMOVE_ALL) + ' ' + exh5outfile

		if (full[0] ne -1)  then  PRINT, 'fextract '+ drname[full[0]] + exname[full[0]] + '+' + STRCOMPRESS(STRING(exten[full[0]]),/REMOVE_ALL) + ' ' + exfulloutfile
		if (nfull ge 2)     then  FOR i=1, nfull-1 DO  PRINT,'fappend  '+ drname[full[i]] + exname[full[i]] + '+' +  STRCOMPRESS(STRING(exten[full[i]]),/REMOVE_ALL) + ' ' + exfulloutfile

		if (all[0] ne -1)  then  PRINT,'fextract '+ drname[all[0]] + exname[all[0]] + '+' + STRCOMPRESS(STRING(exten[all[0]]),/REMOVE_ALL) + ' ' + exalloutfile
		if (nall ge 2)    then  FOR i=1, nall-1 DO  PRINT,'fappend  '+ drname[all[i]] + exname[all[i]] + '+' +  STRCOMPRESS(STRING(exten[all[i]]),/REMOVE_ALL) + ' ' + exalloutfile

		if (ngoodaspcor ge 2)  then  PRINTF, lun,'fextract '+ drname[goodaspcor[1]] + exname[goodaspcor[1]] + '+' + STRCOMPRESS(STRING(exten[goodaspcor[1]]),/REMOVE_ALL) + ' ' + exgoodaspcoroutfile
		if (ngoodaspcor ge 2)    then  FOR i=2, ngoodaspcor-1 DO  PRINTF, lun,'fappend  '+ drname[goodaspcor[i]] + exname[goodaspcor[i]] + '+' +  STRCOMPRESS(STRING(exten[goodaspcor[i]]),/REMOVE_ALL) + ' ' + exgoodaspcoroutfile

		if (ngoodaspcor ge 2)  then  PRINTF, lun,'uvotimsum '+exgoodaspcoroutfile+'  outfile='+exgoodaspcorsumfile+' exclude=none clobber=yes'
		if (ngoodaspcor ge 2)  then  PRINTF, lun,'rm '+exgoodaspcoroutfile

;;;;;;;;;;;;; end exposure maps

endfor

if (ngoodaspcor ge 2)  then  PRINTF, lun,'ds9 -rgb -red '+goodaspcorsumfiles[5]+' -green '+goodaspcorsumfiles[3]+' -blue '+goodaspcorsumfiles[1]+' -height 600 -width 800 & '
if (ngoodaspcor ge 2)  then  PRINTF, lun,'ds9 -rgb -red '+goodaspcorsumfiles[5]+' -green '+goodaspcorsumfiles[2]+' -blue '+goodaspcorsumfiles[1]+' -height 600 -width 800 & '

close, lun
free_lun, lun

close, 33
free_lun, 33

print, 'all done'
stop
END
