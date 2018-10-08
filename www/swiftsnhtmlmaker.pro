pro printsnline, lun, SNnamen, PSNn, SNname2n, galaxyn, redshiftn, typen, n, q
 
	datafilenamesousa='../data/'+SNnamen+'_uvotB15.1.dat'
	imagefilename='../images/'+SNnamen+'_uvot.png'
	lcfilename='../lcplots/'+SNnamen+'_lightcurve.jpg'

printf, lun, '<tr>'
printf, lun, '<td align="center" valign="top">', q , '<br></td>'
printf, lun, '<td align="center" valign="top"><b>', SNnamen, '</b><br> &nbsp;', PSNn,' ', SNname2n, '<br> </td>'
printf, lun, '<td align="center" valign="top"><a'
printf, lun, 'href="http://ned.ipac.caltech.edu/forms/byname.html"> ', galaxyn, ' </a><br> </td>'
printf, lun, '<td align="center" valign="top"> ', redshiftn, ' <br> </td>'
printf, lun, '<td align="center" valign="top"><a href="http://www.cbat.eps.harvard.edu/cbet/RecentCBETs.html"> ', typen, ' </a><br> </td>'
printf, lun, '<td align="center" valign="top"><a'
	if file_test(imagefilename) eq 1 then printf, lun, 'href="https://github.com/pbrown801/SOUSA/images/', SNnamen, '_uvot.png"><img'
	if file_test(imagefilename) eq 1 then printf, lun, 'src="pic.jpg" alt="Swift image" style="border: 0px solid; border: 0px solid; width: 52px; height: 55px;" '


printf, lun, 'border="0" height="55" width="52"></a><a'
if file_test(lcfilename) eq 1 then printf, lun, 'href="https://github.com/pbrown801/SOUSA/lcplots/', SNnamen, '_lightcurve.jpg"><img'
if file_test(lcfilename) eq 1 then printf, lun, 'src="light.jpg" alt="Swift UVOT lightcurve"'

printf, lun, 'style="border: 0px solid; border: 0px solid; width:'
printf, lun, '52px; height: 55px;" border="0" height="55" width="52"></a><a'
	if file_test(datafilenamesousa) eq 1 then printf, lun, 'href="https://github.com/pbrown801/SOUSA/images/data/', SNnamen, '_uvotB15.1.dat"><img'
	if file_test(datafilenamesousa) eq 1 then printf, lun, 'src="sousa_galaxy_small.png" alt="Swift UVOT data"'

printf, lun, 'style="border: 0px solid; border: 0px solid; width:'
printf, lun, '52px; height: 89px;" border="0" height="89" width="52"></a></td>'
printf, lun, '<td align="center" valign="top"><br> </td>'


end



pro swiftsnhtmlmaker

;revised to read in using other code

restore, 'host.sav'


SNname=host.SNname_array
PSN=host.PSNname_array
SNname2=host.SNname2_array
galaxy=host.hostname_array
redshift=host.redshift_array
type=host.SNtype_array
SNtypes=host.SNtype_array

nSNe=n_elements(SNname)

close=sort(host.redshift_array)

ia=where(host.SNtype_array eq 'Ia')

ii=where(strmatch(SNtypes, '*II*') eq 1)
ibc=where(SNTypes eq 'Ib' or SNTypes eq 'Ic' or SNTypes eq 'Ic-BL' or SNTypes eq 'Ib/c' or SNTypes eq 'Ibc' or SNTypes eq 'Ibn' or SNTypes eq 'Ic-PI?' or SNTypes eq 'Ic/GRB' or  SNTypes eq 'Ib/cpec'  or  SNTypes eq 'CC' or SNTypes eq 'Ib-IIb' or SNTypes eq 'SLSNIc' or SNTypes eq 'Ic-bl' or SNTypes eq 'SLSN-Ic'  )

slsne=where(strmatch(SNtypes, '*SLSN*') eq 1)

closeia=sort(host.redshift_array[ia])
closeibc=sort(host.redshift_array[ibc])
closeii=sort(host.redshift_array[ii])

goodia=reverse(sort(host.Nobs_array[ia]))
goodibc=reverse(sort(host.Nobs_array[ibc]))
goodii=reverse(sort(host.Nobs_array[ii]))

;for i=0,n_elements(SNname)-1 do print, SNname[close[i]], redshift[close[i]], host.nobs_array[close[i]]


;for i=0,n_elements(ia)-1 do print, SNname[ia[goodia[i]]], redshift[ia[goodia[i]]], host.nobs_array[ia[goodia[i]]]

;for i=0,n_elements(ibc)-1 do print, SNname[ibc[goodibc[i]]], redshift[ibc[goodibc[i]]], host.nobs_array[ibc[goodibc[i]]]

;for i=0,n_elements(ii)-1 do print, SNname[ii[goodii[i]]], redshift[ii[goodii[i]]], host.nobs_array[ii[goodii[i]]]


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

htmlfile='swift_sn_middle.txt'
openw,lun,htmlfile,/get_lun

for n=0,nSNe-1 do begin
	q=nSNe-n

	printsnline, lun, SNname[n], PSN[n], SNname2[n], galaxy[n], redshift[n], type[n], n, q
endfor
Free_lun,lun
close,lun
close,/all


spawn, 'cp swift_sn_top.txt swift_sn_html.txt'
spawn, 'cat swift_sn_middle.txt >> swift_sn_html.txt'
spawn, 'cat swift_sn_bottom.txt >> swift_sn_html.txt'
spawn, 'cp swift_sn_html.txt swift_sn.html'


;;;;;;;;;;;;;;;;


htmlfile='swift_sn_close.txt'
openw,lun,htmlfile,/get_lun

for r=0,nSNe-1 do begin
	n=close[r]
	q=r+1
	printsnline, lun, SNname[n], PSN[n], SNname2[n], galaxy[n], redshift[n], type[n], n, q

endfor
Free_lun,lun
close,lun
close,/all

spawn, 'cp swift_sn_top.txt swift_sn_close_html.txt'
spawn, 'cat swift_sn_close.txt >> swift_sn_close_html.txt'
spawn, 'cat swift_sn_bottom.txt >> swift_sn_close_html.txt'
spawn, 'cp swift_sn_close_html.txt swift_sn_close.html'
;;;;;;;;;;;;;;;;


htmlfile='swift_sn_close_ia.txt'
openw,lun,htmlfile,/get_lun

for r=0,n_elements(ia)-1 do begin
	n=ia[closeia[r]]
	q=r+1
	printsnline, lun, SNname[n], PSN[n], SNname2[n], galaxy[n], redshift[n], type[n], n, q

endfor
Free_lun,lun
close,lun
close,/all

spawn, 'cp swift_sn_top.txt swift_sn_close_ia_html.txt'
spawn, 'cat swift_sn_close_ia.txt >> swift_sn_close_ia_html.txt'
spawn, 'cat swift_sn_bottom.txt >> swift_sn_close_ia_html.txt'
spawn, 'cp swift_sn_close_ia_html.txt swift_sn_close_ia.html'


;;;;;;;;;;;;;;;;;;;

htmlfile='swift_sn_good_ia.txt'
openw,lun,htmlfile,/get_lun

for r=0,n_elements(goodia)-1 do begin
	n=ia[goodia[r]]
	q=r+1

	printsnline, lun, SNname[n], PSN[n], SNname2[n], galaxy[n], redshift[n], type[n], n, q
endfor
Free_lun,lun
close,lun
close,/all



spawn, 'cp swift_sn_top.txt swift_sn_good_ia_html.txt'
spawn, 'cat swift_sn_good_ia.txt >> swift_sn_good_ia_html.txt'
spawn, 'cat swift_sn_bottom.txt >> swift_sn_good_ia_html.txt'
spawn, 'cp swift_sn_good_ia_html.txt swift_sn_good_ia.html'
;;;;;;;;;;;;;;;;;;;;;;;;;;;

htmlfile='swift_sn_good_ibc.txt'
openw,lun,htmlfile,/get_lun

for r=0,n_elements(goodibc)-1 do begin
	n=ibc[goodibc[r]]
	q=r+1

	printsnline, lun, SNname[n], PSN[n], SNname2[n], galaxy[n], redshift[n], type[n], n, q
endfor
Free_lun,lun
close,lun
close,/all


spawn, 'cp swift_sn_top.txt swift_sn_good_ibc_html.txt'
spawn, 'cat swift_sn_good_ibc.txt >> swift_sn_good_ibc_html.txt'
spawn, 'cat swift_sn_bottom.txt >> swift_sn_good_ibc_html.txt'
spawn, 'cp swift_sn_good_ibc_html.txt swift_sn_good_ibc.html'
;;;;;;;;;;;;;;;;;;;;;;;;;;;

htmlfile='swift_sn_good_ii.txt'
openw,lun,htmlfile,/get_lun

for r=0,n_elements(goodii)-1 do begin

	n=ii[goodii[r]]
	q=r+1

	printsnline, lun, SNname[n], PSN[n], SNname2[n], galaxy[n], redshift[n], type[n], n, q

endfor
Free_lun,lun
close,lun
close,/all

spawn, 'cp swift_sn_top.txt swift_sn_good_ii_html.txt'
spawn, 'cat swift_sn_good_ii.txt >> swift_sn_good_ii_html.txt'
spawn, 'cat swift_sn_bottom.txt >> swift_sn_good_ii_html.txt'
spawn, 'cp swift_sn_good_ii_html.txt swift_sn_good_ii.html'
;;;;;;;;;;;;;;;;;;;;;;;;;;;


htmlfile='swift_sn_slsne.txt'
openw,lun,htmlfile,/get_lun

for r=0,n_elements(slsne)-1 do begin

	n=slsne[r]
	q=r+1

	printsnline, lun, SNname[n], PSN[n], SNname2[n], galaxy[n], redshift[n], type[n], n, q

endfor
Free_lun,lun
close,lun
close,/all

spawn, 'cp swift_sn_top.txt swift_sn_slsne_html.txt'
spawn, 'cat swift_sn_slsne.txt >> swift_sn_slsne_html.txt'
spawn, 'cat swift_sn_bottom.txt >> swift_sn_slsne_html.txt'
spawn, 'cp swift_sn_slsne_html.txt swift_sn_slsne.html'
;;;;;;;;;;;;;;;;;;;;;;;;;;;



print, 'final stop'
stop 
end
