pro readSN2016list

savename='host2016.sav'

; this only works on computer to which it has been downloaded
;spawn, "  cp ~/Downloads/SwiftSNweblist\ -\ FullSNList.csv SwiftSNweblist.csv"
;spawn, "  sed 's/,,/, ,/g' SwiftSNweblist2016.csv > Swiftnew.csv"
;spawn, "  sed 's/,,/, ,/g' Swiftnew.csv > SwiftSNweblist2016.csv"

; messy, with duplicated columns

; the last column needs something in it because it is harder to insert spaces

readcol, 'SwiftSNweblist2016.csv', SNnames, HostNames, PSNnames, SNtypes,  Redshifts, SNnames2, Nobs, TargetIDs, SNra, SNdec, AV, AVerr, AVsource,  RAhost, DEChost, gal_lat_host, gal_long_host, redshift, Host_morphology, host_vel, host_vel_err, host_vel_corr, host_vel_corr_err, discoverydate,lastnondection, template_status, max_exptime, filters, notes, explosiondate, expreference, referencelink, explosionmethod,sibling_SNe, distance_best, distance_err, method_best, refer_best, hubble_dm, hubble_dm_err, uvm2points, dm_cepheid, dm_cepheid_err, dm_cepheid_ref, dm_SBF, dm_sbf_err, dm_sbf_ref, endcolumn, delimiter=',', format='A,A,A,A,A,A,A,A,A,A,A,A,A,A,A, A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A,A', /nan, comment='#'


; after template status  mast_status, 
nobs=uint(Nobs)
nSNe=n_elements(SNnames)


; for mast
; for i=0, nSNe-1 do print, SNnames[i], ' ', SNTypes[i], ' ', HostNames[i], ' ', Redshifts[i], dm_sbf_ref[i]


; for i=0, nSNe-1 do print, SNnames[i], ' ', editor[i]



host = CREATE_STRUCT( $
'SNname_array', make_array(nSNe,/string, value=' '), $
'hostname_array', make_array(nSNe,/string, value=' '), $
'PSNname_array', make_array(nSNe,/string, value=' '), $
'SNname2_array', make_array(nSNe,/string, value=' '), $
'redshift_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'redshift_err_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'redshifttext_array', make_array(nSNe,/string, value=' '), $
'SNtype_array', make_array(nSNe,/string, value=' '), $
'SNtype2_array', make_array(nSNe,/string, value=' '), $
'Nobs_array', make_array(nSNe,/INT, value=!values.f_nan), $
'TargetIDs_array', make_array(nSNe,/string, value=' '), $
'SNra_array', make_array(nSNe,/string, value=' '), $
'SNdec_array', make_array(nSNe,/string, value=' '), $
'template_status_array', make_array(nSNe,/string, value=' '), $
'mast_status_array', make_array(nSNe,/string, value=' '), $
'max_exptime_array', make_array(nSNe,/string, value=' '), $
'filters_array', make_array(nSNe,/string, value=' '), $
'notes_array', make_array(nSNe,/string, value=' '), $
'sibling_SNe_array', make_array(nSNe,/string, value=' '), $
'RAhost_array', make_array(nSNe,/string, value=' '), $
'DEChost_array', make_array(nSNe,/string, value=' '), $
'gal_lat_host_array', make_array(nSNe,/string, value=!values.f_nan), $
'gal_long_host_array', make_array(nSNe,/string, value=!values.f_nan), $
'av_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'redshift_ref_array', make_array(nSNe,/string, value=' '), $
'velocity_array', make_array(nSNe,4,/FLOAT, value=!values.f_nan), $
;'velocityarray', make_array(nSNe,/FLOAT, value=!values.f_nan), $
;'velocityerrarray', make_array(nSNe,/FLOAT, value=!values.f_nan), $
;'velocitycorrarray', make_array(nSNe,/FLOAT, value=!values.f_nan), $
;'velocitycorrerrarray', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'dm_array', make_array(nSNe,5,/FLOAT, value=!values.f_nan), $
'dm_err_array', make_array(nSNe,5,/FLOAT, value=!values.f_nan), $
'dm_ref_array', make_array(nSNe,5,/string, value='reference'), $
'dm_z_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'dm_z_err_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'dm_z_test_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'dm_z_test_err_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'dm_z_cor_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'dm_z_cor_err_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'dm_best_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'dm_best_err_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'dm_best_ref_array', make_array(nSNe,/string, value='dmref'), $
; host morphology
'Host_Morphology_array', make_array(nSNe,/string, value=!values.f_nan), $
'morph_array', make_array(nSNe,/string, value=!values.f_nan), $
'petrosian_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'petrosianminor_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'C9050_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
;'galmagarray', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
;'galmagerrarray', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'galmag_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'galmag_err_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
;  SN fitting
'appmag_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'appmagerr_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'bpeakappmag_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'bpeakmjd_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'bpeakappmagerr_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'peaktime_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'firstepochmjd6_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'firstepochmjd_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'absmag_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'absmagerr_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'bestbabsmag_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'bestbabsmagerr_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'bestvabsmag_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'bestvabsmagerr_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'dm15_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
'dm15err_array', make_array(nSNe,6,/FLOAT, value=!values.f_nan), $
;’mu_z_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
;’mu_z_err_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
;’mu_z_cor_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
;’mu_z_cor_err_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
;’mu_best_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
;’mu_best_err_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'v_best_err_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'v_best_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'b_best_err_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'b_best_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'dmb15_best_err_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'dmb15_best_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
; velocity info
'velocityclass_array', make_array(nSNe,/STRING, value=!values.f_nan), $
'vgclass_array', make_array(nSNe,/STRING, value=!values.f_nan), $
'si0velocity_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'ebvvelocityclass_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
'ebvvelocity_array', make_array(nSNe,/FLOAT, value=!values.f_nan), $
 'data_array', make_array(nSNe,/integer, value=' '), $
 'mast_array', make_array(nSNe,/integer, value=' '), $
 'fit_array', make_array(nSNe,/integer, value=' '), $
 'galfile_array', make_array(nSNe,/integer, value=' '), $
 'galphot_array', make_array(nSNe,/integer, value=' '), $
 'png_array', make_array(nSNe,/integer, value=' ') $
)


host.SNname_array=SNnames

selection=where(hostnames eq '          NaN',count)
if count gt 0 then hostnames[selection]=' '

host.hostname_array=hostnames

selection=where(SNnames2 eq 'SNname2',count)
if count gt 0 then SNnames2[selection]=' '

selection=where(SNnames2 eq '0',count)
if count gt 0 then SNnames2[selection]=' '


selection=where(SNnames2 eq !values.f_nan,count)
if count gt 0 then SNnames2[selection]=' '

selection=where(SNnames2 eq '          NaN',count)
if count gt 0 then SNnames2[selection]=' '
host.SNname2_array=SNnames2


selection=where(PSNnames eq 'PSN',count)
if count gt 0 then PSNnames[selection]=' '
selection=where(PSNnames eq '0',count)
if count gt 0 then PSNnames[selection]=' '
;selection=where(PSNnames eq !values.f_nan,count)
;if count gt 0 then PSNnames[selection]=' '
selection=where(PSNnames eq '          NaN',count)
if count gt 0 then PSNnames[selection]=' '

host.PSNname_array=PSNnames

host.redshift_array=Redshifts
host.redshifttext_array=Redshifts
selection=where(host.redshifttext_array eq !values.f_nan,count)
if count gt 0 then host.redshifttext_array[selection]=' '

;;;;;;;;;;;   SUPERNOVA TYPE


selection=where(hostnames eq '          NaN',count)
if count gt 0 then SNtypes[where(SNtypes eq '          NaN')]=' '

host.SNtype_array=SNtypes



ia=where(SNTypes eq 'Ia' or SNTypes eq 'Ia-91T' or SNTypes eq 'Iax' or SNTypes eq 'Ia-SC' or SNTypes eq 'Ia-91bg' or  SNTypes eq 'Ia-p' or  SNTypes eq 'Iapec' or SNTypes eq 'Ia-99aa' or SNTypes eq 'Ia-99aa?02cx?' or SNTypes eq 'Ia-02cx' or SNTypes eq 'Ia-pec?' or SNTypes eq 'Ia-pec' or SNTypes eq 'Ia-91bg?' or SNTypes eq 'Ia-CSM?' or SNTypes eq 'Ia-CSM' or SNTypes eq 'Ia?' or SNTypes eq 'Ia-91T/99aa' or SNTypes eq 'Ia ')


ibc=where(SNTypes eq 'Ib' or SNTypes eq 'Ic' or SNTypes eq 'Ic-BL' or SNTypes eq 'Ib/c' or SNTypes eq 'Ibc' or SNTypes eq 'Ibn' or SNTypes eq 'Ic-PI?' or SNTypes eq 'Ic/GRB' or  SNTypes eq 'Ib/cpec'  or  SNTypes eq 'CC' or SNTypes eq 'Ib-IIb' or SNTypes eq 'SLSNIc' or SNTypes eq 'Ic-bl' or SNTypes eq 'SLSN-Ic'  )


ii=where(SNTypes eq 'II' or SNTypes eq 'IIP' or SNTypes eq 'IIn' or SNTypes eq 'IIb' or SNTypes eq 'IIL' or SNTypes eq 'IIn/IIL' or SNTypes eq 'II-87K' or  SNTypes eq 'IIp' or  SNTypes eq 'Iib' or  SNTypes eq 'IIn/L?' or  SNTypes eq 'IIb/IIn' or  SNTypes eq 'SLSNI' or SNTypes eq 'SLSN-II' or  SNTypes eq 'SLSN' or SNTypes eq 'SLSNII' or SNTypes eq 'IIn/Ia-CSM' or SNTypes eq 'imp-IIn' or SNTypes eq 'IIn?' )


other=where(SNTypes eq '?' or SNTypes eq 'LBV?' or SNTypes eq 'SN-imp' or SNTypes eq 'LBV' or SNTypes eq 'imp/IIn?' or  SNTypes eq 'IIn/Imp?' or  SNTypes eq 'IIn-Imp?' or SNTypes eq 'LBVgoneSN?' or SNTypes eq 'SLSN-I' or SNTypes eq 'imposter?' or SNTypes eq 'imp?' or SNTypes eq 'I')

host.SNType2_array[ia]='Ia'
host.SNType2_array[ibc]='Ibc'
host.SNType2_array[ii]='II'
host.SNType2_array[other]='other'
	
;;;;;;;;;;;;;;;;;;;;;;;;;
host.Nobs_array=uint(Nobs)


host.TargetIDs_array=TargetIDs
host.SNra_array=SNra
host.SNdec_array=SNdec
host.template_status_array=template_status



host.av_array=av

host.velocity_array[*,0]=float(host_vel)
host.velocity_array[*,1]=float(host_vel_err)
host.velocity_array[*,2]=float(host_vel_corr)
host.velocity_array[*,3]=float(host_vel_corr_err)




host.dm_array[*,0]=float(dm_cepheid)
host.dm_array[*,1]=float(dm_sbf)
;host.dm_array[*,2]=float(dm_pnlf)
;host.dm_array[*,3]=float(dm_other)
;host.dm_array[*,4]=float(dm_tf)

host.dm_err_array[*,0]=float(dm_cepheid_err)
host.dm_err_array[*,1]=float(dm_sbf_err)
;host.dm_err_array[*,2]=float(dm_pnlf_err)
;host.dm_err_array[*,3]=float(dm_other_err)
;host.dm_err_array[*,4]=float(dm_tf_err)

host.dm_ref_array[*,0]=dm_cepheid_ref
host.dm_ref_array[*,1]=dm_sbf_ref
;host.dm_ref_array[*,2]=dm_pnlf_ref
;host.dm_ref_array[*,3]=dm_other_ref
;host.dm_ref_array[*,4]=dm_tf_ref

selection=where(hostnames eq '          NaN',count)
if count gt 0 then for i=0,3 do host.velocity_array[where(host.velocity_array[*,i] eq 0.00000),i]=!VALUES.F_NAN
selection=where(hostnames eq '          NaN',count)
if count gt 0 then for i=0,3 do host.dm_array[where(host.dm_array[*,i] eq 0.00000),i]=!VALUES.F_NAN
selection=where(hostnames eq '          NaN',count)
if count gt 0 then for i=0,3 do host.dm_err_array[where(host.dm_err_array[*,i] eq 0.00000),i]=!VALUES.F_NAN

;;;;; set values of constants
H_0=72.0     ;
H_0_err=5.0;
vel_thermal=200.0     ; uncertainty in velocity of galaxies due to thermal/gravitational 
                      ; motion after large scale structure has been removed
vel_thermal=300.0     ; without large scale structure 

host.dm_z_array=5.0*alog10(host.velocity_array[*,0]/H_0)+25.0

host.dm_z_err_array=sqrt(  ((5.0*host.velocity_array[*,1])/(host.velocity_array[*,0]*alog(10.0)))^2.0 + ((5.0*200.0)/(host.velocity_array[*,0]*alog(10.0)))^2.0 + ( (5*5.0)/(H_0*alog(10.0)) )^2.0 )

host.dm_z_cor_array=5.0*alog10(host.velocity_array[*,2]/H_0)+25

host.dm_z_cor_err_array=sqrt(  ((5.0*host.velocity_array[*,3])/(host.velocity_array[*,2]*alog(10.0)))^2.0 + ((5.0*200.0)/(host.velocity_array[*,2]*alog(10.0)))^2.0 + ( (5.0*5.0)/(H_0*alog(10.0)) )^2.0 )

;host.redshift_ref_array=redshift_ref

; set all to 'z', replace if there is a better distance
for z=0,n_elements(host.dm_best_ref_array)-1 do host.dm_best_ref_array[z]='z '+host.redshift_ref_array[z]
host.dm_best_array=host.dm_z_cor_array
host.dm_best_err_array=host.dm_z_cor_err_array

;
host.dm_z_test_array=5.0*alog10(host.redshift_array*299792/H_0)+25.0

host.dm_z_test_err_array=sqrt(  ((5.0*0.05*host.redshift_array*299792)/(host.redshift_array*299792*alog(10.0)))^2.0 + ((5.0*200.0)/(host.redshift_array*299792*alog(10.0)))^2.0 + ( (5*5.0)/(H_0*alog(10.0)) )^2.0 )

host.dm_best_err_array[where(finite(host.dm_best_array) eq 0)]=host.dm_z_test_err_array[where(finite(host.dm_best_array) eq 0)]
host.dm_best_array[where(finite(host.dm_best_array) eq 0)]=host.dm_z_test_array[where(finite(host.dm_best_array) eq 0)]


;; note, this won't use Tully Fisher distances as the best but will default to Hubble flow
host.dm_best_array[where(finite(host.dm_array[*,3]) eq 1)]=host.dm_array[where(finite(host.dm_array[*,3]) eq 1),3]
host.dm_best_array[where(finite(host.dm_array[*,2]) eq 1)]=host.dm_array[where(finite(host.dm_array[*,2]) eq 1),2]
host.dm_best_array[where(finite(host.dm_array[*,1]) eq 1)]=host.dm_array[where(finite(host.dm_array[*,1]) eq 1),1]
host.dm_best_array[where(finite(host.dm_array[*,0]) eq 1)]=host.dm_array[where(finite(host.dm_array[*,0]) eq 1),0]


host.dm_best_err_array[where(finite(host.dm_array[*,3]) eq 1)]=host.dm_err_array[where(finite(host.dm_array[*,3]) eq 1),3]
host.dm_best_err_array[where(finite(host.dm_array[*,2]) eq 1)]=host.dm_err_array[where(finite(host.dm_array[*,2]) eq 1),2]
host.dm_best_err_array[where(finite(host.dm_array[*,1]) eq 1)]=host.dm_err_array[where(finite(host.dm_array[*,1]) eq 1),1]
host.dm_best_err_array[where(finite(host.dm_array[*,0]) eq 1)]=host.dm_err_array[where(finite(host.dm_array[*,0]) eq 1),0]


host.dm_best_ref_array[where(finite(host.dm_array[*,3]) eq 1)]=host.dm_ref_array[where(finite(host.dm_array[*,3]) eq 1),3]
host.dm_best_ref_array[where(finite(host.dm_array[*,2]) eq 1)]=host.dm_ref_array[where(finite(host.dm_array[*,2]) eq 1),2]
host.dm_best_ref_array[where(finite(host.dm_array[*,1]) eq 1)]=host.dm_ref_array[where(finite(host.dm_array[*,1]) eq 1),1]
host.dm_best_ref_array[where(finite(host.dm_array[*,0]) eq 1)]=host.dm_ref_array[where(finite(host.dm_array[*,0]) eq 1),0]

;;;;;;;;;; host galaxy info  

host.Host_Morphology_array=Host_morphology

morpharray = make_array(nSNe, /string)


for n=0,nSNe-1 do begin

;regrouping specific strings in Host_morphology array

	if strmatch(Host_morphology[n], '*E*') eq 1 then morpharray[n] = 'E' 
	if strmatch(Host_morphology[n], '*S*') eq 1 then morpharray[n] = 'S'

	if strmatch(Host_morphology[n], '*SAbc LINER*') eq 1 then morpharray[n] = 'S'
	if strmatch(Host_morphology[n], 'S0*') eq 1 then morpharray[n] = 'S0'
	if strmatch(Host_morphology[n], '*Sm*') eq 1 then morpharray[n] = 'I'
	if strmatch(Host_morphology[n], '*I0*') eq 1 then morpharray[n] = 'I'
	if strmatch(Host_morphology[n], '*Im*') eq 1 then morpharray[n] = 'I'
	if strmatch(Host_morphology[n], 'I') eq 1 then morpharray[n] = 'I'
	if strmatch(Host_morphology[n], '*IB(s)m*') eq 1 then morpharray[n] = 'I'
	if strmatch(Host_morphology[n], '*IAB(s)m*') eq 1 then morpharray[n] = 'I'
	if strmatch(Host_morphology[n], '*cD*') eq 1 then morpharray[n] = 'E'
	if strmatch(Host_morphology[n], '*ExtendedSrc[SDSS]*') eq 1 then morpharray[n] = ''

endfor

host.morph_array=morpharray

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;  supernova fitting



for n=0,nSNe-1 do begin

SNname=host.SNname_array[n]

	datafile='$SOUSA/data/'+SNname+'_uvotB15.1.dat'
	datatest=file_test(datafile)
	if  template_status[n] ne 'done' then print, '# no template for ', SNname, ' says ', template_status[n]

	if  template_status[n] eq 'done' and datatest eq 0 then print, '# no data for ', SNname


	if datatest eq 1 then begin
	pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat',   dt=dt
	host.bpeakmjd_array=dt.bb[0,where(dt.bb[1,*] eq min(dt.bb[1,*],/nan))]
	host.firstepochmjd_array[n] = dt.time_array[0]
	host.firstepochmjd6_array[n,0] = min(dt.w2[0,*])
	host.firstepochmjd6_array[n,1] = min(dt.m2[0,*])
	host.firstepochmjd6_array[n,2] = min(dt.w1[0,*])
	host.firstepochmjd6_array[n,3] = min(dt.uu[0,*])
	host.firstepochmjd6_array[n,4] = min(dt.bb[0,*])
	host.firstepochmjd6_array[n,5] = min(dt.vv[0,*])

	endif

; old version	fitfile='$DROPSN/SOUSA/fitting/'+SNname+'_6fitsB15.sav'
	fitfile='$DROPSN/SOUSA/fitting/'+SNname+'_6fits16.sav'
	fittest=file_test(fitfile)
	if datatest eq 1 and fittest eq 0 and host.SNtype2_array[n] eq 'Ia' then print, '# no fits for ', SNname


if   datatest eq 1 then host.data_array[n]=1

	mastfile='$SNFOLDER/sousa/formast/SOUSAfits/hlsp_sousa_swift_uvot_'+strlowcase(SNname)+'_w1_v1.0_img.fits.gz'
	masttest=file_test(mastfile)
	rawmastfile='$SNFOLDER/sousa/formast/SOUSAfits/'+SNname+'_w1.img.gz'
	rawmasttest=file_test(rawmastfile)

	w2mastfile='$SNFOLDER/sousa/formast/SOUSAfits/hlsp_sousa_swift_uvot_'+strlowcase(SNname)+'_w2_v1.0_img.fits.gz'
	w2masttest=file_test(w2mastfile)
	w2rawmastfile='$SNFOLDER/sousa/formast/SOUSAfits/'+SNname+'_w2.img.gz'
	w2rawmasttest=file_test(w2rawmastfile)

	m2mastfile='$SNFOLDER/sousa/formast/SOUSAfits/hlsp_sousa_swift_uvot_'+strlowcase(SNname)+'_m2_v1.0_img.fits.gz'
	m2masttest=file_test(mastfile)
	m2rawmastfile='$SNFOLDER/sousa/formast/SOUSAfits/'+SNname+'_m2.img.gz'
	m2rawmasttest=file_test(m2rawmastfile)





if   masttest eq 1  or rawmasttest eq 1 or  m2masttest eq 1  or m2rawmasttest eq 1  or  w2masttest eq 1  or w2rawmasttest eq 1 then host.mast_array[n]=1

if   fittest eq 1 then host.fit_array[n]=1	


	pngfile='$DROPSN/www/SwiftSNe/'+SNname+'_uvot.png'
	pngtest=file_test(pngfile)

if   pngtest eq 1 then host.png_array[n]=1

	galfile='$DROPSN/SOUSA/galdata/'+SNname+'_petfits.sav'
	galtest=file_test(galfile)

if   galtest eq 1 then host.galphot_array[n]=1
if   galtest eq 1 then host.galfile_array[n]=1





;	if fittest eq 0 then print, fitfile
	if fittest eq 1 then begin
		
;print, SNname

	restore, fitfile
;	print, SNname, COMBBPEAKMJD, COMBBPEAKMJDerr

	host.peaktime_array[n,*]=PEAKMJDARRAY6





	host.bpeakmjd_array[n]=combbpeakmjd
	if SNname eq 'SN2005cf' or SNname eq 'SN2005df' or  SNname eq 'SN2011fe' then Bpeaktime=groundbpeakmjd


	host.appmag_array[n,*]=peakmagarray6
	host.appmagerr_array[n,*]=peakmagerrarray6

	host.bpeakappmag_array[n,*]=bpeakmagarray
	host.bpeakappmagerr_array[n,*]=bpeakmagerrarray

	host.dm15_array[n,*]=dm15array6
	host.dm15err_array[n,*]=dm15errarray6


	host.appmag_array[n,4]=combbpeakmag
	host.appmagerr_array[n,4]=combbpeakmagerr
	host.dm15_array[n,4]=combbdm15
	host.dm15err_array[n,4]=combbdm15err

	host.appmag_array[n,5]=combvpeakmag
	host.appmagerr_array[n,5]=combvpeakmagerr
	host.dm15_array[n,5]=combvdm15
	host.dm15err_array[n,5]=combvdm15err


;;; just use ground based for saturated supernovae
if SNname eq 'SN2005cf' or SNname eq 'SN2006dd' or SNname eq 'SN2005df' or  SNname eq 'SN2011fe' or SNname eq 'SN2011iv' then begin 


	host.appmag_array[n,3]=!values.f_nan
	host.appmagerr_array[n,3]=!values.f_nan
	host.dm15_array[n,3]=!values.f_nan
	host.dm15err_array[n,3]=!values.f_nan

	host.appmag_array[n,4]=groundbpeakmag
	host.appmagerr_array[n,4]=groundbpeakmagerr
	host.dm15_array[n,4]=groundbdm15
	host.dm15err_array[n,4]=groundbdm15err

	host.appmag_array[n,5]=groundvpeakmag
	host.appmagerr_array[n,5]=groundvpeakmagerr
	host.dm15_array[n,5]=groundvdm15
	host.dm15err_array[n,5]=groundvdm15err

endif


; if SNname eq 'SN2014J' then stop

endif

		galfile='$SOUSA/galdata/'+SNname+'_petfits.sav'
		test=file_test(galfile)
		if test eq 0  and host.SNtype_array[n] eq 'Ia'   and redshifts[n] lt 0.025 then print, '# no galmags for ', SNname
		if test eq 1 then begin
;			print, '# ', SNname, ' is done '
			restore, galfile

			host.galmag_array[n,*]=pet2mags
			host.galmag_err_array[n,*]=pet2magerrs
	
			host.petrosian_array[n]=petrosian_radius
			host.petrosianminor_array[n]=petrosian_radius*minori[0]/majori[0]
			host.c9050_array[n,*]=C9050
	
		endif
;;;;;;;;;
endfor



reduce=where(host.data_array eq 0 and host.template_status_array eq 'done')

print, ' '
print, 'These SNe have templates but no SOUSA photometry'

if reduce[0] ne -1 then for q=0,n_elements(reduce)-1 do print, host.SNname_array[reduce[q]], ' ', host.SNtype_array[reduce[q]], ' ', host.nobs_array[reduce[q]] 





needfits=where(host.fit_array eq 0 and host.sntype_array eq 'Ia' and host.data_array eq 1 and host.nobs_array gt 3)
print, 'These SNe Ia have SOUSA photometry but no fits'

if needfits[0] ne -1 then print, host.SNname_array[needfits]


needgal=where(host.galfile_array eq 0 and host.data_array eq 1 and host.sntype_array eq 'Ia' and host.data_array eq 1 and host.nobs_array gt 3 and host.redshift_array gt 0.003 and  host.redshift_array lt 0.03)

print, 'These SNe Ia have SOUSA photometry but no galaxy fits'

if needgal[0] ne -1 then print, host.SNname_array[needgal]






ia=where(host.SNtype_array eq 'Ia' or host.SNtype_array eq 'Ia-91T' or host.SNtype_array eq 'Iax' or host.SNtype_array eq 'Ia-SC' or host.SNtype_array eq 'Ia-91bg' or  host.SNtype_array eq 'Ia-p' or  host.SNtype_array eq 'Iapec' or host.SNtype_array eq 'Ia-91bg' or  host.SNtype_array eq 'Ia-p' or  host.SNtype_array eq 'Iapec' or host.SNtype_array eq 'Ia-99aa' or host.SNtype_array eq 'Ia-99aa?02cx?' or host.SNtype_array eq 'Ia-02cx' or host.SNtype_array eq 'Ia-pec?' or host.SNtype_array eq 'Ia-pec' or host.SNtype_array eq 'Ia-91bg?' or host.SNtype_array eq 'Ia-CSM?' or host.SNtype_array eq 'Ia-CSM' or host.SNtype_array eq 'Ia?' or host.SNtype_array eq 'Ia-91T/99aa')

ibc=where(host.SNtype_array eq 'Ib' or host.SNtype_array eq 'Ic' or host.SNtype_array eq 'Ic-BL' or host.SNtype_array eq 'Ib/c' or host.SNtype_array eq 'Ibc' or host.SNtype_array eq 'Ibn' or host.SNtype_array eq 'Ic-PI?' or host.SNtype_array eq 'Ic/GRB' or  host.SNtype_array eq 'Ib/cpec'  or  host.SNtype_array eq 'CC'  or host.SNtype_array eq 'Ib-IIb' or host.SNtype_array eq 'SLSNIc' or host.SNtype_array eq 'Ic-bl' or host.SNtype_array eq 'SLSN-Ic'  )

ii=where(host.SNtype_array eq 'II' or host.SNtype_array eq 'IIP' or host.SNtype_array eq 'IIn' or host.SNtype_array eq 'IIb' or host.SNtype_array eq 'IIL' or host.SNtype_array eq 'IIn/IIL' or host.SNtype_array eq 'II-87K' or  host.SNtype_array eq 'IIp' or  host.SNtype_array eq 'Iib' or  host.SNtype_array eq 'IIn/L?' or  host.SNtype_array eq 'IIb/IIn' or  host.SNtype_array eq 'SLSNI' or host.SNtype_array eq 'SLSN-II' or  host.SNtype_array eq 'SLSN' or host.SNtype_array eq 'SLSNII'  or  host.SNtype_array eq 'SLSN' or host.SNtype_array eq 'SLSNII' or host.SNtype_array eq 'IIn/Ia-CSM' or host.SNtype_array eq 'imp-IIn' or host.SNtype_array eq 'IIn?')

other=where(host.SNtype_array eq '?' or host.SNtype_array eq 'LBV?' or host.SNtype_array eq 'SN-imp' or host.SNtype_array eq 'LBV' or host.SNtype_array eq 'imp/IIn?' or  host.SNtype_array eq 'IIn/Imp?' or  host.SNtype_array eq 'IIn-Imp?' or host.SNtype_array  eq 'LBVgoneSN?' or host.SNtype_array  eq 'SLSN-I' or host.SNtype_array  eq 'imposter?' or host.SNtype_array  eq 'imp?' or host.SNtype_array  eq 'I')



type2=host.SNtype_array
type2[ia]='Ia'
type2[ibc]='Ibc'
type2[ii]='II'
type2[other]='other'

;for x=0,nSNe-1 do print, SNname[x], ' ', type[x], ' ', type2[x]

print, ' '
print, ' SN numbers and fraction by type '

print, 'Ia ', n_elements(ia), nSNe, float(n_elements(ia))/nSNe
print, 'Ibc ', n_elements(ibc), nSNe, float(n_elements(ibc))/nSNe
print, 'II ', n_elements(ii) , nSNe, float(n_elements(ii))/nSNe
print, 'other ', nSNe-(n_elements(ia)+n_elements(ibc)+n_elements(ii)), nSNe, float(nSNe-(n_elements(ia)+n_elements(ibc)+n_elements(ii)))/nSNe



print, ' '
print, ' Info for SNe Ia'
print, n_elements(ia), ' observed'

 ia6=where(strmatch(SNtypes,'*Ia*') eq 1 and nobs gt 5)
print, n_elements(ia6), ' observed at least 6 times'
;         163



 ia3=where(strmatch(SNtypes,'*Ia*') eq 1 and nobs gt 2)
print, n_elements(ia3), ' observed at least 3 times'
;         193
ia3done=where(strmatch(SNtypes,'*Ia*') eq 1 and nobs gt 2 and strmatch(template_status,'done') eq 1 )

print, n_elements(ia3done), ' observed at least 3 times and templates are done'
;          157

ia6done=where(strmatch(SNtypes,'*Ia*') eq 1 and nobs gt 5 and strmatch(template_status,'done') eq 1 )

print, n_elements(ia6done), ' observed at least 6 times and templates are done'
; 137

ia3notemp=where(strmatch(SNtypes,'*Ia*') eq 1 and float(nobs) gt 2 and strmatch(template_status,'done') eq 0 )
;print, template_status[ia3notemp]

print, 'these type Ia supernovae need templates'

print, SNnames[ia3notemp]
;print, SNnames[ia3done]
;print, SNtypes[ia3done]




;pie_chart, [n_elements(ia),n_elements(ibc),n_elements(ii),nSNe-(n_elements(ia)+n_elements(ibc)+n_elements(ii))], pienames=['Ia ','Ibc ','II ','?']

save, filename=savename, host, verbose=1
print, 'saved, continue to update plots'
;print, 'sav file not created, continue to update plots'
stop




;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
print, 'final stop'
stop 
end
