pro plotallsne

mjd_2005jan1=53371.0

mjd_swiftlaunch=2453330.2194444-2400000.5

;readcol, '$SNFOLDER/www/SwiftSN/SwiftSNweblist.txt', SNname, PSNname, SNname2, Host, redshift, type, nobs, format='a,a,a,a,f,a,i'

restore, 'host.sav'

SNe=host.SNname_array
SNlist=SNe

nSNe=n_elements(SNe)

SNtype=host.SNtype2_array

firstepoch=53370
lastepoch=56500

c=2.99792458*10^5.0
;velocity=c*host.redshift_array
velocity=host.velocity_array[0,*]
H_0=72.0
d_z =5.0*alog10(velocity/H_0)+25.0


timerange=[firstepoch,lastepoch]


colors=make_array(nSNe,value='black')
symbols=make_array(nSNe,value=4)

for n=0,nSNe-1 do begin 


if (SNtype[n] eq 'Ia')  then colors[n]='red'
if (SNtype[n] eq 'Ibc')  then colors[n]='dark green'
if (SNtype[n] eq 'II') then colors[n]='blue'
if (SNtype[n] eq 'other') then colors[n]='black'


endfor


for n=0,nSNe-1 do symbols[n]=n+1

for n=0,nSNe-1 do while symbols[n] gt 7 do symbols[n]=symbols[n]-7




;;;;;;;;;;


; from http://www.iluvatar.org/~dwijn/idlfigures
!p.font = 1
!p.thick = 2
!x.thick = 2
!y.thick = 2
!z.thick = 2
xsize = 22.0
ysize = 10.0
wall = 0.03
margin=0.18

a = xsize/8.8 - (margin + wall)
a = xsize/8.8 - (2.0*margin + wall)
b = ysize/8.8 - (margin + wall)

ticklen = 0.01
xticklen = ticklen/b
yticklen = ticklen/a

nxticks=10

x1 = margin*8.8/xsize
x2 = x1 + a*8.8/xsize
xc = x2 + wall*8.8/xsize
y1 = margin*8.8/ysize
y2 = y1 + b*8.8/ysize
y3 = y2 + wall*8.8/ysize
y4 = y3 + b*8.8/ysize
yc = y4 + wall*8.8/ysize
xrangemjd=[firstepoch, lastepoch]
xrangeSwiftyears=[0.0,16.0]
nxticks=xrangeSwiftyears[1]
xtitlemjd='Modified Julian Date'
xtitleSwiftyears='Swift Years'
yrangew2=[22,10]
yrangem2=[22,10]
yrangew1=[22,10]
yrangeuu=[22,10]
yrangebb=[22,10]
yrangevv=[22,10]

xdata=[0,1,2,3]
ydata=[2,3,4,5]

fontsize=16

legpos=[0.85,0.9]

plotfile='plotallsne_w1.eps'
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
SET_PLOT, 'PS'

device, filename=plotfile, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=fontsize, Bits_per_Pixel=8, Color=1


;;;;;;;;

cgplot, xdata, ydata,  /nodata, /noerase, position=[x1,y1,x2,y2], $
 ytitle='uvw1 Vega magnitudes', xtitle=xtitleSwiftyears, charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=yrangem2, ystyle=1, xrange=xrangeSwiftyears, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=nyticks, ytickv=ytickvalues

problem = 'problem SNe '

for n=0,nSNe-1 do begin
	SNname=SNlist[n]
	print, SNname

	good=0
	dt=0
	mag=0

	filename1='$SOUSA/data'+'/'+SNname+'_uvotB15.1.dat'

	test1=file_test(filename1)
	if test1 eq 1 then pjb_phot_array_B141, filename1, dt=dt 
	if test1 eq 1 then 	good=where( finite(dt.w1[1,*]) eq 1 )

	if test1 eq 1 then if n_elements(good) gt 2 then oploterror, (dt.w1[0,*]-mjd_swiftlaunch)/365.25, dt.w1[1,good], dt.w1[2,good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])

;	if n_elements(good) gt 2 then if dt.w1[2,good[1]] gt 0.5 then problem=problem + SNname



endfor


;;;;;;;;;

;leg=[ 'Ia','Ibc','II']
;legcolors=['red','dark green','blue']
;al_legend, leg, psym=symcat(14), color=legcolors, $
;pos=[3,10.5], charsize=1.0, box=0

device, /close
SET_PLOT, 'X'

$open plotallsne_w1.eps


;;;;;;;;;


plotfile='plotallsne_m2.eps'
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
SET_PLOT, 'PS'

device, filename=plotfile, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=fontsize, Bits_per_Pixel=8, Color=1


;;;;;;;;

cgplot, xdata, ydata,  /nodata, /noerase, position=[x1,y1,x2,y2], $
 ytitle='uvm2 Vega magnitudes', xtitle=xtitleSwiftyears, charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=yrangem2, ystyle=1, xrange=xrangeSwiftyears, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=nyticks, ytickv=ytickvalues

problem = 'problem SNe '

for n=0,nSNe-1 do begin
	SNname=SNlist[n]
	print, SNname

	good=0
	dt=0
	mag=0

	filename1='$SNFOLDER/SwiftSNarchive/PhotArchive/'+SNname+'_uvotB13.2.dat'
	filename2='$SNFOLDER/tyler/inddat/'+SNname+'_uvotB13.dat'
	filename2='$SNFOLDER/tyler/sne_data_arch_old/'+SNname+'_m2_mags3.dat'

	filename3='$SNFOLDER/SwiftSNarchive/'+SNname+'/'+SNname+'_uvotB13.2.dat'
	filename4='$SNFOLDER/SwiftSNarchive/'+SNname+'/'+SNname+'_uvotB13.dat'
	filename5='$SNFOLDER/currentSwiftSNe/'+SNname+'/'+SNname+'_uvotB13.2.dat'
	filename6='$SNFOLDER/currentSwiftSNe/'+SNname+'/'+SNname+'_uvotB13.dat'

	test1=file_test(filename1)
	test2=file_test(filename2)
	test3=file_test(filename3)
	test4=file_test(filename4)
	test5=file_test(filename5)
	test6=file_test(filename6)

	if test6 eq 1 then snphot_array, filename6, 'temp.fits', dt=dt 
	if test6 eq 1 then good=where( finite(dt.m2[1,*]) eq 1 )

	if test5 eq 1 then pjb_phot_array_B132, filename5, dt=dt 
	if test5 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

	if test4 eq 1 then snphot_array, filename4, 'temp.fits', dt=dt 
	if test4 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

	if test3 eq 1 then pjb_phot_array_B132, filename3, dt=dt 
	if test3 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

;	if test2 eq 1 then snphot_array, filename2, 'temp.fits', dt=dt 
;	if test2 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

	if test2 eq 1 then readcol, filename2, mjd, mag, magerr
	if test2 eq 1 then 	good=where( finite(mag) eq 1 )

; if test2 eq 1 then if magerr[0] gt 0.5 then problem=problem + SNname[n]


	if test1 eq 1 then pjb_phot_array_B132, filename1, dt=dt 
	if test1 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

	if test2 eq 0 then	if n_elements(good) gt 2 then oploterror, (dt.m2[0,good]-mjd_swiftlaunch)/365.25, dt.m2[1,good], dt.m2[2,good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])


	if test2 eq 1 then if n_elements(good) gt 2 then oploterror, (mjd+50000-mjd_swiftlaunch)/365.25, mag[good], magerr[good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])

;	if n_elements(good) gt 2 then if dt.m2[2,good[1]] gt 0.5 then problem=problem + SNname



endfor


;;;;;;;;;

leg=[ 'Ia','Ibc','II']
legcolors=['red','dark green','blue']
al_legend, leg, psym=symcat(14), color=legcolors, $
pos=legpos, /norm, charsize=1.0, box=0

device, /close
SET_PLOT, 'X'

$open plotallsne_m2.eps





;;;;;;;;;


plotfile='plotallsne_m2abs.eps'
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
SET_PLOT, 'PS'

device, filename=plotfile, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=fontsize, Bits_per_Pixel=8, Color=1


;;;;;;;;

yrangem2abs=[-8,-25]

cgplot, xdata, ydata,  /nodata, /noerase, position=[x1,y1,x2,y2], $
 ytitle='uvm2 absolute magnitudes', xtitle=xtitleSwiftyears, charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=yrangem2abs, ystyle=1, xrange=xrangeSwiftyears, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=nyticks, ytickv=ytickvalues

problem = 'problem SNe '

peakmag=fltarr(nSNe)

for n=0,nSNe-1 do begin
	SNname=SNlist[n]
	print, SNname

	good=0
	dt=0
	mag=0

	filename1='$SNFOLDER/SwiftSNarchive/PhotArchive/'+SNname+'_uvotB13.2.dat'
	filename2='$SNFOLDER/tyler/inddat/'+SNname+'_uvotB13.dat'
	filename2='$SNFOLDER/tyler/sne_data_arch_old/'+SNname+'_m2_mags3.dat'

	filename3='$SNFOLDER/SwiftSNarchive/'+SNname+'/'+SNname+'_uvotB13.2.dat'
	filename4='$SNFOLDER/SwiftSNarchive/'+SNname+'/'+SNname+'_uvotB13.dat'
	filename5='$SNFOLDER/currentSwiftSNe/'+SNname+'/'+SNname+'_uvotB13.2.dat'
	filename6='$SNFOLDER/currentSwiftSNe/'+SNname+'/'+SNname+'_uvotB13.dat'

	test1=file_test(filename1)
	test2=file_test(filename2)
	test3=file_test(filename3)
	test4=file_test(filename4)
	test5=file_test(filename5)
	test6=file_test(filename6)

	if test6 eq 1 then snphot_array, filename6, 'temp.fits', dt=dt 
	if test6 eq 1 then good=where( finite(dt.m2[1,*]) eq 1 )

	if test5 eq 1 then pjb_phot_array_B132, filename5, dt=dt 
	if test5 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

	if test4 eq 1 then snphot_array, filename4, 'temp.fits', dt=dt 
	if test4 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

	if test3 eq 1 then pjb_phot_array_B132, filename3, dt=dt 
	if test3 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

;	if test2 eq 1 then snphot_array, filename2, 'temp.fits', dt=dt 
;	if test2 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

	if test2 eq 1 then readcol, filename2, mjd, mag, magerr
	if test2 eq 1 then 	good=where( finite(mag) eq 1 )

; if test2 eq 1 then if magerr[0] gt 0.5 then problem=problem + SNname[n]

	if test1 eq 1 then pjb_phot_array_B132, filename1, dt=dt 
	if test1 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

;print, test1, test2, test3, test4, test5, test6

		if test2 eq 0 then if n_elements(good) gt 2 then oploterror, (dt.m2[0,good]-mjd_swiftlaunch)/365.25, dt.m2[1,good]-d_z[n], dt.m2[2,good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])

	if test2 eq 1 then if n_elements(good) gt 2 then oploterror, (mjd+50000-mjd_swiftlaunch)/365.25, mag[good]-d_z[n], magerr[good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])

;	if n_elements(good) gt 2 then if dt.m2[2,good[1]] gt 0.5 then problem=problem + SNname

	if n_elements(good) gt 2 then 	if test2 eq 1 then peakmag[n]=min(mag, /nan)-d_z[n]
	if n_elements(good) gt 2 then 	if test2 eq 0 then peakmag[n]=min(dt.m2[1,*], /nan)-d_z[n]

print, SNlist[n], peakmag[n], d_z[n]

endfor

cgAxis, YAxis=1, YRange=yrangem2abs-20.0, yticks=nyticks, /Save, ytitle='Distance Modulus', ytickname=[30,35,40,45],  charsize=1.0, $
yminor=1, yticklen=yticklen,  ystyle=1

;;;;;;;;;

leg=[ 'Ia','Ibc','II']
legcolors=['red','dark green','blue']
al_legend, leg, psym=symcat(14), color=legcolors, $
pos=legpos, /norm, charsize=1.0, box=0

device, /close
SET_PLOT, 'X'

$open plotallsne_m2abs.eps
;;;;;;;;;


plotfile='plotallsne_w1abs.eps'
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
SET_PLOT, 'PS'

device, filename=plotfile, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=fontsize, Bits_per_Pixel=8, Color=1


;;;;;;;;

yrangew1abs=[-8,-25]

cgplot, xdata, ydata,  /nodata, /noerase, position=[x1,y1,x2,y2], $
 ytitle='uvw1 absolute magnitudes', xtitle=xtitleSwiftyears, charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=yrangew1abs, ystyle=1, xrange=xrangeSwiftyears, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=nyticks, ytickv=ytickvalues

problem = 'problem SNe '

peakmag=fltarr(nSNe)

for n=0,nSNe-1 do begin
	SNname=SNlist[n]
	print, SNname

	good=0
	dt=0
	mag=0

	filename1='$SNFOLDER/SwiftSNarchive/PhotArchive/'+SNname+'_uvotB13.2.dat'
	filename2='$SNFOLDER/tyler/inddat/'+SNname+'_uvotB13.dat'
	filename2='$SNFOLDER/tyler/sne_data_arch_old/'+SNname+'_w1_mags3.dat'

	filename3='$SNFOLDER/SwiftSNarchive/'+SNname+'/'+SNname+'_uvotB13.2.dat'
	filename4='$SNFOLDER/SwiftSNarchive/'+SNname+'/'+SNname+'_uvotB13.dat'
	filename5='$SNFOLDER/currentSwiftSNe/'+SNname+'/'+SNname+'_uvotB13.2.dat'
	filename6='$SNFOLDER/currentSwiftSNe/'+SNname+'/'+SNname+'_uvotB13.dat'

	test1=file_test(filename1)
	test2=file_test(filename2)
	test3=file_test(filename3)
	test4=file_test(filename4)
	test5=file_test(filename5)
	test6=file_test(filename6)

	if test6 eq 1 then snphot_array, filename6, 'temp.fits', dt=dt 
	if test6 eq 1 then good=where( finite(dt.w1[1,*]) eq 1 )

	if test5 eq 1 then pjb_phot_array_B132, filename5, dt=dt 
	if test5 eq 1 then 	good=where( finite(dt.w1[1,*]) eq 1 )

	if test4 eq 1 then snphot_array, filename4, 'temp.fits', dt=dt 
	if test4 eq 1 then 	good=where( finite(dt.w1[1,*]) eq 1 )

	if test3 eq 1 then pjb_phot_array_B132, filename3, dt=dt 
	if test3 eq 1 then 	good=where( finite(dt.w1[1,*]) eq 1 )

;	if test2 eq 1 then snphot_array, filename2, 'temp.fits', dt=dt 
;	if test2 eq 1 then 	good=where( finite(dt.w1[1,*]) eq 1 )

	if test2 eq 1 then readcol, filename2, mjd, mag, magerr
	if test2 eq 1 then 	good=where( finite(mag) eq 1 )

; if test2 eq 1 then if magerr[0] gt 0.5 then problem=problem + SNname[n]

	if test1 eq 1 then pjb_phot_array_B132, filename1, dt=dt 
	if test1 eq 1 then 	good=where( finite(dt.w1[1,*]) eq 1 )

;print, test1, test2, test3, test4, test5, test6

	if test2 eq 0 then	if n_elements(good) gt 2 then oploterror, (dt.w1[0,good]-mjd_swiftlaunch)/365.25, dt.w1[1,good]-d_z[n], dt.w1[2,good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])

	if test2 eq 1 then if n_elements(good) gt 2 then oploterror, (mjd+50000-mjd_swiftlaunch)/365.25, mag[good]-d_z[n], magerr[good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])

;	if n_elements(good) gt 2 then if dt.w1[2,good[1]] gt 0.5 then problem=problem + SNname



	if n_elements(good) gt 2 then 	if test2 eq 1 then peakmag[n]=min(mag, /nan)-d_z[n]
	if n_elements(good) gt 2 then 	if test2 eq 0 then peakmag[n]=min(dt.w1[1,*], /nan)-d_z[n]

print, SNlist[n], peakmag[n], d_z[n]

endfor

;;;;;;;;;

leg=[ 'Ia','Ibc','II']
legcolors=['red','dark green','blue']
al_legend, leg, psym=symcat(14), color=legcolors, $
pos=legpos, /norm, charsize=1.0, box=0

device, /close
SET_PLOT, 'X'

$open plotallsne_w1abs.eps






plotfile='plotallsne_m2distmod.eps'
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
SET_PLOT, 'PS'

device, filename=plotfile, /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=fontsize, Bits_per_Pixel=8, Color=1


;;;;;;;;

yrangem2abs=[-31,-43]

cgplot, xdata, ydata,  /nodata, /noerase, position=[x1,y1,x2,y2], $
 ytitle='- distance modulus for limiting mag uvm2=20', xtitle=xtitleSwiftyears, charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=yrangem2abs, ystyle=1, xrange=xrangeSwiftyears, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=nyticks, ytickv=ytickvalues

problem = 'problem SNe '

distmod=fltarr(nSNe)

for n=0,nSNe-1 do begin
	SNname=SNlist[n]
	print, SNname

	good=0
	dt=0
	mag=0
	filename1='$SNFOLDER/SwiftSNarchive/PhotArchive/'+SNname+'_uvotB13.2.dat'
	filename2='$SNFOLDER/tyler/inddat/'+SNname+'_uvotB13.dat'
	filename2='$SNFOLDER/tyler/sne_data_arch_old/'+SNname+'_m2_mags3.dat'

	filename3='$SNFOLDER/SwiftSNarchive/'+SNname+'/'+SNname+'_uvotB13.2.dat'
	filename4='$SNFOLDER/SwiftSNarchive/'+SNname+'/'+SNname+'_uvotB13.dat'
	filename5='$SNFOLDER/currentSwiftSNe/'+SNname+'/'+SNname+'_uvotB13.2.dat'
	filename6='$SNFOLDER/currentSwiftSNe/'+SNname+'/'+SNname+'_uvotB13.dat'

	test1=file_test(filename1)
	test2=file_test(filename2)
	test3=file_test(filename3)
	test4=file_test(filename4)
	test5=file_test(filename5)
	test6=file_test(filename6)

	if test6 eq 1 then snphot_array, filename6, 'temp.fits', dt=dt 
	if test6 eq 1 then good=where( finite(dt.m2[1,*]) eq 1 )

	if test5 eq 1 then pjb_phot_array_B132, filename5, dt=dt 
	if test5 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

	if test4 eq 1 then snphot_array, filename4, 'temp.fits', dt=dt 
	if test4 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

	if test3 eq 1 then pjb_phot_array_B132, filename3, dt=dt 
	if test3 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

;	if test2 eq 1 then snphot_array, filename2, 'temp.fits', dt=dt 
;	if test2 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

	if test2 eq 1 then readcol, filename2, mjd, mag, magerr
	if test2 eq 1 then 	good=where( finite(mag) eq 1 )

; if test2 eq 1 then if magerr[0] gt 0.5 then problem=problem + SNname[n]

	if test1 eq 1 then pjb_phot_array_B132, filename1, dt=dt 
	if test1 eq 1 then 	good=where( finite(dt.m2[1,*]) eq 1 )

;print, test1, test2, test3, test4, test5, test6

		if test2 eq 0 then if n_elements(good) gt 2 then oploterror, (dt.m2[0,good]-mjd_swiftlaunch)/365.25, dt.m2[1,good]-d_z[n]-20.0, dt.m2[2,good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])

	if test2 eq 1 then if n_elements(good) gt 2 then oploterror, (mjd+50000-mjd_swiftlaunch)/365.25, mag[good]-d_z[n]-20.0, magerr[good], linestyle=2, psym=-symbols[n], symsize=size, color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])

;	if n_elements(good) gt 2 then if dt.m2[2,good[1]] gt 0.5 then problem=problem + SNname



	if n_elements(good) gt 2 then 	if test2 eq 1 then distmod[n]=-1.0*(min(mag, /nan)-d_z[n]-20.0)
	if n_elements(good) gt 2 then 	if test2 eq 0 then distmod[n]=-1.0*(min(dt.m2[1,*], /nan)-d_z[n]-20.0)

print, SNlist[n], peakmag[n], d_z[n]

endfor



;;;;;;;;;

leg=[ 'Ia','Ibc','II']
legcolors=['red','dark green','blue']
al_legend, leg, psym=symcat(14), color=legcolors, $
pos=legpos, /norm, charsize=1.0, box=0

device, /close
SET_PLOT, 'X'

$open plotallsne_m2distmod.eps
;;;;;;;;;
;cgAxis, YAxis=1, YLog=1, YRange=[0.1, 100], /Save
;;;;;;;;;;




;;;;;;;;;

stop
end



