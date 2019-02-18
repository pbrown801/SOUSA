pro plotallsne6

mjd_2005jan1=53371.0

mjd_swiftlaunch=2453330.2194444-2400000.5

readcol, '$SNFOLDER/www/SwiftSN/SwiftSNweblist.txt', SNname, PSNname, SNname2, Host, redshift, type, nobs, format='a,a,a,a,f,a,i'

;SNname=['SN2005am','SN2006aj','SN2009ip','SN2011fe','SN2012aw']
;type=['Ia','Ic','other','Ia','IIP']

SNe=SNname
SNlist=SNe

nSNe=n_elements(SNe)

SNtype=type

firstepoch=53370
lastepoch=56500
lastepoch=57000
lastepoch=53370+365*10
magrange=[24,24]
nxticks=11

small=0.5

timerange=[firstepoch,lastepoch]

colors=make_array(nSNe,value='black')
symbols=make_array(nSNe,value=4)

missingsupernovae='missing supernovae '

for n=0,nSNe-1 do begin 

if (SNtype[n] eq 'Ia')  then colors[n]='red'
if (SNtype[n] eq 'Iap') then colors[n]='orange'
if (SNtype[n] eq 'Ib')  then colors[n]='dark green'
if (SNtype[n] eq 'Ibc')  then colors[n]='dark green'
if (SNtype[n] eq 'Ib/c')  then colors[n]='dark green'
if (SNtype[n] eq 'Ic')  then colors[n]='dark green'
if (SNtype[n] eq 'Ib/cpec')  then colors[n]='dark green'
if (SNtype[n] eq 'Ic/GRB')  then colors[n]='dark green'
if (SNtype[n] eq 'Ic')  then colors[n]='dark green'
if (SNtype[n] eq 'Ic')  then colors[n]='dark green'
if (SNtype[n] eq 'Ic')  then colors[n]='dark green'
;if (SNtype[n] eq 'Ib')  then colors[n]='black'
;if (SNtype[n] eq 'Ibc')  then colors[n]='black'
;if (SNtype[n] eq 'Ic')  then colors[n]='black'
if (SNtype[n] eq 'IIP') then colors[n]='blue'
if (SNtype[n] eq 'II-P') then colors[n]='blue'
if (SNtype[n] eq 'IIp') then colors[n]='blue'
if (SNtype[n] eq 'II') then colors[n]='blue'
if (SNtype[n] eq 'IIb') then colors[n]='cyan'
if (SNtype[n] eq 'IIn') then colors[n]='violet'
if (SNtype[n] eq 'IIL') then colors[n]='darkorchid'

if (SNtype[n] eq 'Ia?') then colors[n]='red'
if (SNtype[n] eq 'Iap') then colors[n]='red'
if (SNtype[n] eq 'Ia-p') then colors[n]='red'
if (SNtype[n] eq 'Ia-SC') then colors[n]='red'
if (SNtype[n] eq 'Ia-91bg') then colors[n]='red'
if (SNtype[n] eq 'Ia-91T') then colors[n]='red'
if (SNtype[n] eq 'Ia-sub') then colors[n]='red'
if (SNtype[n] eq 'Ia-02cx') then colors[n]='red'
if (SNtype[n] eq 'Iapec') then colors[n]='red'
if (SNtype[n] eq 'Ia-pec?') then colors[n]='red'
if (SNtype[n] eq 'Iax') then colors[n]='red'
if (SNtype[n] eq 'IIb') then colors[n]='blue'
if (SNtype[n] eq 'IIn') then colors[n]='blue'
if (SNtype[n] eq 'SLSNI') then colors[n]='dark green'
if (SNtype[n] eq 'SLSNII') then colors[n]='blue'
if (SNtype[n] eq 'IIn/IIL') then colors[n]='blue'
if (SNtype[n] eq 'IIn/L?') then colors[n]='blue'
if (SNtype[n] eq 'IIn-Imp?') then colors[n]='black'
if (SNtype[n] eq 'LBV') then colors[n]='black'
if (SNtype[n] eq 'imp/IIn?') then colors[n]='black'
if (SNtype[n] eq 'IIb/IIn') then colors[n]='blue'
if (SNtype[n] eq 'imp-IIn') then colors[n]='blue'
if (SNtype[n] eq 'IIL') then colors[n]='blue'
if (SNtype[n] eq 'II-87K') then colors[n]='blue'
if (SNtype[n] eq 'SLSN-II') then colors[n]='blue'
if (SNtype[n] eq 'Q') then colors[n]='dark green'
if (SNtype[n] eq 'Q?') then colors[n]='dark green'
if (SNtype[n] eq 'Ic-PI?') then colors[n]='dark green'
if (SNtype[n] eq 'Ic-BL') then colors[n]='dark green'
if (SNtype[n] eq 'SLSN') then colors[n]='dark green'
if (SNtype[n] eq 'Ibn') then colors[n]='dark green'

endfor

;;;;;;;;;;;;;;;

ia=where(colors eq 'red')
ibc=where(colors eq 'dark green')
ii=where(colors eq 'blue')
other=where(colors eq 'black')

type2=type
type2[ia]='Ia'
type2[ibc]='Ibc'
type2[ii]='II'
type2[other]='other'


for n=0,nSNe-1 do symbols[n]=n+1

for n=0,nSNe-1 do while symbols[n] gt 7 do symbols[n]=symbols[n]-7

;;;;;;;;;;





;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;  6 PLOT  ;;;;;;;;;;;;;;;;;;;;
;

nplots=6
; from http://www.iluvatar.org/~dwijn/idlfigures
!p.font = 1
!p.thick = 2
!x.thick = 2
!y.thick = 2
!z.thick = 2
; the default size is given in centimeters
; 8.8 is made to match a journal column width
xsize = 8.8
ysize = 12.0
wall = 0.03
margin=0.12
a = xsize/8.8 - (margin + wall)
b = a * 2d / (1 + sqrt(5))
b = a * 2d / (1 + sqrt(5))
b= (ysize/xsize - margin - wall)/ nplots
; ysize = (margin + nplots*(b + wall ) )*xsize
ticklen = 0.01
xticklen = ticklen/b
yticklen = ticklen/a

x1 = margin*8.8/xsize
x2 = x1 + a*8.8/xsize
xc = x2 + wall*8.8/xsize
y1 = margin*8.8/ysize
y2 = y1 + b*8.8/ysize

yrangew2=[22,10]
yrangem2=[22,10]
yrangew1=[22,10]
yrangeuu=[22,10]
yrangebb=[22,10]
yrangevv=[22,10]
yrange=[22,10]

xdata=[0,1,2,3]
ydata=[2,3,4,5]

fontsize=16


xrangeswiftyears=[0,11]
xrangemjd=[firstepoch, lastepoch]
xrangeSwiftyears=[0.0,11.0]
nxticks=11

ytitles=['uvw2','uvm2','uvw1','u','b','v']
xtitles=[' ',' ',' ',' ',' ','Swift Years']

xtitlemjd='Modified Julian Date'
xtitleSwiftyears='Swift Years'
nyticks=4

figurename='plotall_6.eps'

SET_PLOT, 'PS'

device, filename=figurename, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=12, bits_per_pixel=8, /color

for g=0,5 do begin
f=5-g

plot, xdata, ydata, /nodata, /noerase, $
position=[x1,y1+(g)*b*8.8/ysize,x2,y2+(g)*b*8.8/ysize], $
xtitle=xtitles[f],   ytitle=ytitles[f], charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=yrange, ystyle=1, xrange=xrangeswiftyears, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=4, ytickv=ytickvalues, xtickname=replicate(' ',nxticks+1)

if f eq 5 then begin

plot, xdata, ydata, /nodata, /noerase, $
position=[x1,y1+(g)*b*8.8/ysize,x2,y2+(g)*b*8.8/ysize], $
xtitle=xtitles[f],   ytitle=ytitles[f], charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=yrange, ystyle=1, xrange=xrangeswiftyears, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=4, ytickv=ytickvalues

endif

for n=0,nSNe-1 do begin
	SNname=SNlist[n]
	print, SNname

	good=0
	dt=0
	mag=0

	filename1='$SOUSA/data/'+SNname+'_uvotB14.1.dat'
	filename2='~/Desktop/Dropbox/SN/PrelimArchive/'+SNname+'_uvotB14.1.dat'
	filename3='~/Desktop/Dropbox/SN/PhotArchive/'+SNname+'_uvotB13.2.dat'
	filename4='~/Desktop/Dropbox/SN/PrelimArchive/'+SNname+'_uvotB13.2.dat'
	filename5='/Users/pbrown/Desktop/SN/tyler/CCSN_DATA/inddat/'+SNname+'_w1_mags3.dat'
	test5=file_test(filename5)

	test1=file_test(filename1)
	test2=file_test(filename2)
	test3=file_test(filename3)
	test4=file_test(filename4)

	if test4 eq 1 then begin
		pjb_phot_array_B132, filename4, dt=dt 
	
		fin=finite(dt.mag_array[f,*])
		if fin[0] ne -1 then	good=where( finite(dt.mag_array[f,*]) eq 1 )

	endif

	if test3 eq 1 then begin
		pjb_phot_array_B132, filename3, dt=dt 
	
		fin=finite(dt.mag_array[f,*])
		if fin[0] ne -1 then	good=where( finite(dt.mag_array[f,*]) eq 1 )

	endif

	if test2 eq 1 then begin
		pjb_phot_array_B141, filename2, dt=dt 
	
		fin=finite(dt.mag_array[f,*])
		if fin[0] ne -1 then	good=where( finite(dt.mag_array[f,*]) eq 1 )

	endif

	if test1 eq 1 then begin

		pjb_phot_array_B141, filename1, dt=dt 
		good=where( finite(dt.mag_array[f,*]) eq 1 )
		up=where(finite(dt.mag_array[f,*]) eq 0 and finite(dt.maguplimit_array[f,*]) eq 1 )
		down=where(finite(dt.mag_array[f,*]) eq 0 and finite(dt.magsatlimit_array[f,*]) eq 0 )


		sort=sort(dt.mag_array[f,*])
		connect=dt.mag_array[f,*]
		if down[0] ne -1 then connect[down]=dt.magsatlimit_array[f,down]
		if up[0] ne -1  then connect[up]=dt.maguplimit_array[f,up]

;		if n_elements(connect) gt 2 then oploterror, (dt.dt.time_array[good]-mjd_swiftlaunch)/365.25, dt.mag_array[f,good], dt.magerr_array[f,good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])


if good[0] ne -1 then oploterror, [0.0,0, reform((dt.time_array[good]-mjd_swiftlaunch)/365.25)], [!values.f_nan,!values.f_nan, reform(dt.mag_array[f,good])], [0.0,0, reform(dt.magerr_array[f,good])], psym=cgsymcat(symbols[n]), color=cgcolor(colors[n]), errcolor=cgcolor(colors[n]), symsize=small

if up[0] ne -1 then oplot, [0.0,0, reform((dt.time_array[up]-mjd_swiftlaunch)/365.25)], [!values.f_nan,!values.f_nan,  reform(dt.maguplimit_array[f,up])], psym=cgsymcat(11), color=cgcolor(colors[n]),symsize=small


if down[0] ne -1 then oplot, [0.0,0, reform((dt.time_array[down]-mjd_swiftlaunch)/365.25)], [!values.f_nan,!values.f_nan,  reform(dt.magsatlimit_array[f,down])], psym=cgsymcat(5), color=cgcolor(colors[n]), symsize=small

if n_elements(connect) gt 1 then oplot, (dt.time_array[sort]-mjd_swiftlaunch)/365.25, connect[sort], linestyle=2, color=cgcolor(colors[n]),     symsize=small

endif

	if test2+test4 gt 0 then 	if n_elements(good) gt 2 then oploterror, (dt.time_array[good]-mjd_swiftlaunch)/365.25, dt.mag_array[f,good], dt.magerr_array[f,good], linestyle=2, psym=-symbols[n], symsize=small, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])

	if test5 eq 1 then readcol, filename5, mjd, mag, magerr
	if test5 eq 1 then 	good=where( finite(mag) eq 1 )

	if test5 eq 1 and n_elements(good) gt 2 then oploterror, (mjd[good]-mjd_swiftlaunch)/365.25, mag[good], magerr[good], linestyle=2, psym=-symbols[n], symsize=small, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])


	if test1+test3+test2+test4+test5 eq 0 then missingsupernovae=missingsupernovae+SNname
;	if test1+test3+test2+test4+test5 eq 0 then stop

endfor





endfor



leg=[ 'Ia','Ibc','II']
legcolors=['red','dark green','blue']
legpos=[0.86,0.97]
al_legend, leg, psym=symcat(14), color=legcolors, $
pos=legpos, /norm, charsize=1.0, box=0, background_color=white

device, /close
SET_PLOT, 'X'
$open plotall_6.eps 

stop


f=1

plot, xdata, ydata, /nodata, /noerase, $
position=[x1,y1+(f-1)*b*8.8/ysize,x2,y1+(f+0)*b*8.8/ysize], $
xtitle=' ',   ytitle='uvw1', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[10,22], ystyle=1, xrange=xrangeswiftyears, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=5, ytickv=ytickvalues, xtickname=replicate(' ',nxticks+1)

f=2

plot, xdata, ydata, /nodata, /noerase, $
position=[x1,y1+(f-1)*b*8.8/ysize,x2,y1+(f+0)*b*8.8/ysize], $
xtitle=' ',   ytitle='uvw1', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[10,22], ystyle=1, xrange=xrangeswiftyears, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=5, ytickv=ytickvalues, xtickname=replicate(' ',nxticks+1)

f=3

plot, xdata, ydata, /nodata, /noerase, $
position=[x1,y1+(f-1)*b*8.8/ysize,x2,y1+(f+0)*b*8.8/ysize], $
xtitle=' ',   ytitle='uvw1', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[10,22], ystyle=1, xrange=xrangeswiftyears, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=5, ytickv=ytickvalues, xtickname=replicate(' ',nxticks+1)

f=4

plot, xdata, ydata, /nodata, /noerase, $
position=[x1,y1+(f-1)*b*8.8/ysize,x2,y1+(f+0)*b*8.8/ysize], $
xtitle=' ',   ytitle='uvw1', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[10,22], ystyle=1, xrange=xrangeswiftyears, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=5, ytickv=ytickvalues, xtickname=replicate(' ',nxticks+1)

for n=0,nSNe-1 do begin
	SNname=SNlist[n]
	print, SNname

	good=0
	dt=0
	mag=0

	filename1='$SOUSA/data/'+SNname+'_uvotB14.1.dat'
	filename2='~/Desktop/Dropbox/SN/PrelimArchive/'+SNname+'_uvotB14.1.dat'
	filename3='~/Desktop/Dropbox/SN/PhotArchive/'+SNname+'_uvotB13.2.dat'
	filename4='~/Desktop/Dropbox/SN/PrelimArchive/'+SNname+'_uvotB13.2.dat'
	filename5='/Users/pbrown/Desktop/SN/tyler/CCSN_DATA/inddat/'+SNname+'_w1_mags3.dat'
	test5=file_test(filename5)

	test1=file_test(filename1)
	test2=file_test(filename2)
	test3=file_test(filename3)
	test4=file_test(filename4)

	if test4 eq 1 then pjb_phot_array_B132, filename4, dt=dt 
	if test4 eq 1 then if finite(dt.w1[1,*]) ne -1 then	good=where( finite(dt.w1[1,*]) eq 1 )

;	if test3 eq 1 then pjb_phot_array_B132, filename3, dt=dt 
;	if test3 eq 1 then if finite(dt.w1[1,*]) ne -1 then	 	good=where( finite(dt.w1[1,*]) eq 1 )

	if test2 eq 1 then pjb_phot_array_B141, filename2, dt=dt 
	if test2 eq 1 then if finite(dt.w1[1,*]) ne -1 then	 	good=where( finite(dt.w1[1,*]) eq 1 )

	if test1 eq 1 then begin

		pjb_phot_array_B141, filename1, dt=dt 
		good=where( finite(dt.w1[1,*]) eq 1 )
		up=where(finite(dt.w1[1,*]) eq 0 and finite(dt.w1[5,*]) eq 1 )
		down=where(finite(dt.w1[1,*]) eq 0 and finite(dt.w1[5,*]) eq 0 )


		sort=sort(dt.w1[0,*])
		connect=dt.w1[1,*]
		if down[0] ne -1 then connect[down]=dt.w1[4,down]
		if up[0] ne -1  then connect[up]=dt.w1[3,up]

;		if n_elements(connect) gt 2 then oploterror, (dt.w1[0,good]-mjd_swiftlaunch)/365.25, dt.w1[1,good], dt.w1[2,good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])


if good[0] ne -1 then oploterror, [0.0,0, reform((dt.w1[0,good]-mjd_swiftlaunch)/365.25)], [!values.f_nan,!values.f_nan, reform(dt.w1[1,good])], [0.0,0, reform(dt.w2[2,good])], psym=-cgsymcat(symbols[n]), color=cgcolor(colors[n]), errcolor=cgcolor(colors[n]), symsize=normal

if up[0] ne -1 then oplot, [0.0,0, reform((dt.w1[0,up]-mjd_swiftlaunch)/365.25)], [!values.f_nan,!values.f_nan,  reform(dt.w1[3,up])], psym=cgsymcat(11), color=cgcolor(colors[n]),     symsize=small


if down[0] ne -1 then oplot, [0.0,0, reform((dt.w1[0,down]-mjd_swiftlaunch)/365.25)], [!values.f_nan,!values.f_nan,  reform(dt.w1[4,down])], psym=cgsymcat(5), color=cgcolor(colors[n]), symsize=small

if n_elements(connect) gt 1 then oplot, (dt.w1[0,sort]-mjd_swiftlaunch)/365.25, connect[sort], linestyle=2, color=cgcolor(colors[n]),     symsize=small

endif

	if test2+test4 gt 0 then 	if n_elements(good) gt 2 then oploterror, (dt.w1[0,good]-mjd_swiftlaunch)/365.25, dt.w1[1,good], dt.w1[2,good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])

	if test5 eq 1 then readcol, filename5, mjd, mag, magerr
	if test5 eq 1 then 	good=where( finite(mag) eq 1 )

	if test5 eq 1 and n_elements(good) gt 2 then oploterror, (mjd[good]-mjd_swiftlaunch)/365.25, mag[good], magerr[good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])


	if test1+test3+test2+test4+test5 eq 0 then missingsupernovae=missingsupernovae+SNname
;	if test1+test3+test2+test4+test5 eq 0 then stop

endfor



plot, xdata, ydata, /nodata, /noerase, position=[x1,y1,x2,y2], $
xtitle=xtitleSwiftyears,   ytitle='v', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[22,10], ystyle=1, xrange=xrangeSwiftyears, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=nyticks, ytickv=ytickvalues


problem = 'problem SNe '

for n=0,nSNe-1 do begin
	SNname=SNlist[n]
	print, SNname

	good=0
	dt=0
	mag=0

	filename1='$SOUSA/data/'+SNname+'_uvotB14.1.dat'
	filename2='~/Desktop/Dropbox/SN/PrelimArchive/'+SNname+'_uvotB14.1.dat'
	filename3='~/Desktop/Dropbox/SN/PhotArchive/'+SNname+'_uvotB13.2.dat'
	filename4='~/Desktop/Dropbox/SN/PrelimArchive/'+SNname+'_uvotB13.2.dat'
	filename5='/Users/pbrown/Desktop/SN/tyler/CCSN_DATA/inddat/'+SNname+'_w1_mags3.dat'
	test5=file_test(filename5)

	test1=file_test(filename1)
	test2=file_test(filename2)
	test3=file_test(filename3)
	test4=file_test(filename4)

	if test4 eq 1 then pjb_phot_array_B132, filename4, dt=dt 
	if test4 eq 1 then 	good=where( finite(dt.w1[1,*]) eq 1 )

;	if test3 eq 1 then pjb_phot_array_B132, filename3, dt=dt 
;	if test3 eq 1 then 	good=where( finite(dt.w1[1,*]) eq 1 )

	if test2 eq 1 then pjb_phot_array_B141, filename2, dt=dt 
	if test2 eq 1 then 	good=where( finite(dt.w1[1,*]) eq 1 )

	if test1 eq 1 then pjb_phot_array_B141, filename1, dt=dt 
	if test1 eq 1 then 	good=where( finite(dt.w1[1,*]) eq 1 )


	if test2+test4 gt 0 then 	if n_elements(good) gt 2 then oploterror, (dt.w1[0,good]-mjd_swiftlaunch)/365.25, dt.w1[1,good], dt.w1[2,good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])

	if test5 eq 1 then readcol, filename5, mjd, mag, magerr
	if test5 eq 1 then 	good=where( finite(mag) eq 1 )

	if test5 eq 1 and n_elements(good) gt 2 then oploterror, (mjd[good]-mjd_swiftlaunch)/365.25, mag[good], magerr[good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])


	if test1+test3+test2+test4+test5 eq 0 then missingsupernovae=missingsupernovae+SNname
;	if test1+test3+test2+test4+test5 eq 0 then stop

endfor



leg=[ 'Ia','Ibc','II']
legcolors=['red','dark green','blue']
al_legend, leg, psym=symcat(14), color=legcolors, $
pos=legpos, /norm, charsize=1.0, box=0

device, /close
SET_PLOT, 'X'
$open plotall_6.eps 

;;;;;;;;;


;;;;;;;;;
print, 'final stop'
stop
end



