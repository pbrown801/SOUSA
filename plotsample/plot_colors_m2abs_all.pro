
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

pro plot_colors_m2abs_all

restore, '$DROPSN/www/SwiftSN/host.sav'

SNtypes=host.SNtype_array

nSNe=n_elements(host.SNtype_array)

templatearray=intarr(nSNe)

slsne=where(strmatch(SNtypes, '*SLSN*') eq 1)

host.SNtype2_array[slsne]='SLSN'

colors=make_array(nSNe,value='grey')
peakm2mag_array=make_array(nSNe,/float,value= !values.f_nan)
bluestm2v_array=make_array(nSNe,/float,value= !values.f_nan)

colors[where( host.SNtype2_array eq 'Ia' ) ] ='red'		
colors[where( host.SNtype2_array eq 'Ibc' ) ] ='dark green'		
colors[where( host.SNtype2_array eq 'II'  ) ] ='blue'		
colors[where( host.SNtype_array  eq 'IIn'   ) ] ='purple'		
colors[where( host.SNtype2_array eq 'SLSN' ) ] ='black'



SNlist=host.SNname_array



psym=[18,17,4,5,6,9,7,11,23,25]
psymall=intarr(nSNe)
for n=0,nSNe-1 do psymall[n]= psym[n mod 10]
sizes=make_array(nSNe,value=0.4)
sizes[where( host.SNtype2_array eq 'Ia' ) ] =0.2		

;;;;;;;;;;;;;;;;;

nplots=2
; from http://www.iluvatar.org/~dwijn/idlfigures
!p.font = 1
!p.thick = 2
!x.thick = 2
!y.thick = 2
!z.thick = 2
; the default size is given in centimeters
; 8.8 is made to match a journal column width
xsize = 10.8
wall = 0.05
margin=0.17
a = xsize/8.8 - (margin + wall + margin)
b = a * 2d / (1 + sqrt(5))

ysize = (margin + wall+nplots*(b + wall ) )*xsize
ticklen = 0.01
xticklen = ticklen/b
yticklen = ticklen/a

x1 = margin*8.8/xsize
x2 = x1 + a*8.8/xsize
xc = x2 + wall*8.8/xsize
y1 = margin*b/a*8.8/xsize
y2 = y1 + b*8.8/xsize

nxticks=10
nyticks=12



xdata=[0,1,2,3]
ydata=[2,3,4,5]

epochlimit=80

time_range=[-20,80]
m2u_range=[-1.5,5.5]
m2v_range=[-3,7]
uv_range=[-1.5,3.5]
m2abs_range=[-10,-25]
uabs_range=[-12,-24]

ntimeticks=10
nm2uticks=7
nuvticks=5
nm2vticks=10
nm2absticks=15
nuabsticks=12

fontsize=14
dt=0.7
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;   NORMAL COLOR   ;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

SET_PLOT, 'PS'

device, filename='m2plots.eps', /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=fontsize
;;;;;;;;;;;;;;;;;


;;;;;;;;;;;;;;;;;;;;;;;;;
;;; top left
;;;
;;; uvm2 abs v time

cgplot, xdata, ydata, /nodata, /noerase, position=[x1,y2,x2,y2+y2-y1], $
xtitle=' ',   ytitle='uvm2 absolute mag', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=m2abs_range, ystyle=1, xrange=time_range, xstyle=1, color='black', $
xticks=ntimeticks, xtickv=xtickvalues, yticks=nm2absticks, ytickv=ytickvalues, xtickname=replicate(' ',nxticks+1)



for n=0,nSNe-1 do begin

	SNname=host.SNname_array[n]

	print, SNname

	datafilenamesousa='$SOUSA/data/prelimdata/'+SNname+'_uvotB15.1.dat'

	if file_test(datafilenamesousa) eq 1 then begin
		;; Swift data
		pjb_phot_array_B141, datafilenamesousa, dt=dt

		nfiltersinepoch=intarr(n_elements(dt.time_array))
		filtercheck=intarr(n_elements(dt.time_array),6)
		for q=0,n_elements(dt.time_array)-1 do for f=0,5 do filtercheck[q,f]=finite(dt.mag_array[f,q])
		for q=0,n_elements(dt.time_array)-1 do nfiltersinepoch[q]=total(filtercheck[q,*]) 
		all6=where(nfiltersinepoch eq 6)
		n6epochs=n_elements(all6)

		referenceepoch=dt.time_array[where(dt.mag_array[1,*] eq min(dt.mag_array[1,*],/nan))]

peakm2mag_array[n]=dt.mag_array[1,where(dt.mag_array[1,*] eq min(dt.mag_array[1,*],/nan))]-host.dm_best_array[n]

bluestm2v_array[n]=dt.mag_array[1,where(dt.mag_array[1,*]-dt.mag_array[5,*] eq min(dt.mag_array[1,*]-dt.mag_array[5,*],/nan))]-dt.mag_array[5,where(dt.mag_array[1,*]-dt.mag_array[5,*] eq min(dt.mag_array[1,*]-dt.mag_array[5,*],/nan))]

vvgood=where( finite(dt.mag_array[5,*]) eq 1)
uugood=where( finite(dt.mag_array[3,*]) eq 1)
m2good=where( finite(dt.mag_array[1,*]) eq 1)
m2ugood=where(finite(dt.mag_array[1,*]) eq 1  and  finite(dt.mag_array[3,*]) eq 1)
uvgood=where( finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[1,*]) eq 1)
m2uvgood=where(finite(dt.mag_array[1,*]) eq 1  and   finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[5,*]) eq 1)



oploterror, dt.time_array[m2good]-referenceepoch[0], dt.mag_array[1,m2good]-host.dm_best_array[n], dt.magerr_array[1,m2good], linestyle=2, psym=-(psymall[n]), symsize=sizes[n], color=cgcolor(colors[n]), errcolor=cgcolor(colors[n]), hatlength=0

endif
endfor


;cgAxis, YAxis=1,YRange=abs(m2abs_range-20),  yticks=nm2absticks,charsize=1, yminor=1, ytitle='Distance Modulus Limit', /Save

H_0=72.0
c_kms=3.0*10.0^5.0
dm=34.0
;dm=[30.0,31,32,33,34,35,36,37,38,39,40,41,42,43,44]
z=H_0/c_kms*10.0^((dm-25.0)/5.0)

zticks=['0.0024','0.0038','0.006','0.01',' 0.015','0.024','0.038','0.06','0.1','0.15','0.24','0.38','0.60','0.96','1.51']

;  using cosmology calculator
zticks=['0.0023','0.0037','0.0059','0.0092','0.015','0.023', '0.036','0.056','0.087','0.13','0.20','0.3','0.45','0.66','0.95']
zticks=['0.002','0.004','0.006','0.009','0.015','0.023', '0.036','0.056','0.087','0.13','0.20','0.3','0.45','0.66','0.95', ' ']


cgAxis, YAxis=1,YRange=abs(m2abs_range-20),  yticks=nm2absticks, charsize=1, yminor=1, ytitle='Redshift Limit', ytickname=zticks, /Save

;;;
;;; u-v  v time


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; bottom left
cgplot, xdata, ydata, /nodata, /noerase, position=[x1,y1,x2,y2], $
xtitle='Days since UV Peak Brightness',   ytitle='uvm2 - v', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=m2v_range, ystyle=1, xrange=time_range, xstyle=1, color=black, $
xticks=ntimeticks, xtickv=xtickvalues, yticks=nm2vticks, ytickv=ytickvalues



for n=0,nSNe-1 do begin

	SNname=host.SNname_array[n]

	print, SNname

	datafilenamesousa='$SOUSA/data/prelimdata/'+SNname+'_uvotB15.1.dat'

	if file_test(datafilenamesousa) eq 1 then begin
		;; Swift data
		pjb_phot_array_B141, datafilenamesousa, dt=dt

		nfiltersinepoch=intarr(n_elements(dt.time_array))
		filtercheck=intarr(n_elements(dt.time_array),6)
		for q=0,n_elements(dt.time_array)-1 do for f=0,5 do filtercheck[q,f]=finite(dt.mag_array[f,q])
		for q=0,n_elements(dt.time_array)-1 do nfiltersinepoch[q]=total(filtercheck[q,*]) 
		all6=where(nfiltersinepoch eq 6)
		n6epochs=n_elements(all6)

		referenceepoch=dt.time_array[where(dt.mag_array[1,*] eq min(dt.mag_array[1,*],/nan))]



vvgood=where( finite(dt.mag_array[5,*]) eq 1)
uugood=where( finite(dt.mag_array[3,*]) eq 1)
m2good=where( finite(dt.mag_array[1,*]) eq 1)
m2ugood=where(finite(dt.mag_array[1,*]) eq 1  and  finite(dt.mag_array[3,*]) eq 1)
m2vgood=where(finite(dt.mag_array[1,*]) eq 1  and  finite(dt.mag_array[5,*]) eq 1)
uvgood=where( finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[1,*]) eq 1)
m2uvgood=where(finite(dt.mag_array[1,*]) eq 1  and   finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[5,*]) eq 1)



oploterror, dt.time_array[m2vgood]-referenceepoch[0], dt.mag_array[1,m2vgood]-dt.mag_array[5,m2vgood], dt.magerr_array[1,m2good], linestyle=2, psym=-(psymall[n]), symsize=sizes[n], color=cgcolor(colors[n]), errcolor=cgcolor(colors[n]), hatlength=0

endif
endfor



;al_legend, SNlist,   psym=psymall, symsize=0.8, color=colors, $
;pos=[0.665,0.47], /norm, charsize=0.8, box=1, background_color='white'



device, /close
SET_PLOT, 'X'



$ open m2plots.eps


brightest=reverse(sort(peakm2mag_array))

for n=0, nSNe-1 do print, host.SNname_array[brightest[n]], ' ', host.SNtype_array[brightest[n]], ' ', peakm2mag_array[brightest[n]]

stop

;;;;;;;;;;;;;;;;;;  uvm2  absolute magnitude plot

nplots=1
; from http://www.iluvatar.org/~dwijn/idlfigures
!p.font = 1
!p.thick = 2
!x.thick = 2
!y.thick = 2
!z.thick = 2
; the default size is given in centimeters
; 8.8 is made to match a journal column width
xsize = 10.8
wall = 0.05
margin=0.17
a = xsize/8.8 - (margin + wall + margin)
b = a - margin ;* 2d / (1 + sqrt(5))

ysize = (margin + wall+nplots*(b + wall ) )*xsize
ticklen = 0.01
xticklen = ticklen/b
yticklen = ticklen/a

x1 = margin*8.8/xsize
x2 = x1 + a*8.8/xsize
xc = x2 + wall*8.8/xsize
y1 = margin*8.8/xsize
y2 = 1.0-wall

nxticks=10
nyticks=12



xdata=[0,1,2,3]
ydata=[2,3,4,5]

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;   NORMAL COLOR   ;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

SET_PLOT, 'PS'

device, filename='m2absplot.eps', /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=fontsize
;;;;;;;;;;;;;;;;;


;;;;;;;;;;;;;;;;;;;;;;;;;
;;; top left
;;;
;;; m2 abs v time

cgplot, xdata, ydata, /nodata, /noerase, position=[x1,y1,x2,y2], $
xtitle='Days Since UV Peak Brightness',   ytitle='uvm2 absolute mag', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=m2abs_range, ystyle=1, xrange=[-20,80], xstyle=1, color='black', $
xticks=ntimeticks, xtickv=xtickvalues, yticks=nm2absticks, ytickv=ytickvalues



for n=0,nSNe-1 do begin

	SNname=host.SNname_array[n]

	print, SNname

	datafilenamesousa='$SOUSA/data/prelimdata/'+SNname+'_uvotB15.1.dat'

	if file_test(datafilenamesousa) eq 1 then begin
		;; Swift data
		pjb_phot_array_B141, datafilenamesousa, dt=dt

		nfiltersinepoch=intarr(n_elements(dt.time_array))
		filtercheck=intarr(n_elements(dt.time_array),6)
		for q=0,n_elements(dt.time_array)-1 do for f=0,5 do filtercheck[q,f]=finite(dt.mag_array[f,q])
		for q=0,n_elements(dt.time_array)-1 do nfiltersinepoch[q]=total(filtercheck[q,*]) 
		all6=where(nfiltersinepoch eq 6)
		n6epochs=n_elements(all6)

		referenceepoch=dt.time_array[where(dt.mag_array[1,*] eq min(dt.mag_array[1,*],/nan))]



vvgood=where( finite(dt.mag_array[5,*]) eq 1)
uugood=where( finite(dt.mag_array[3,*]) eq 1)
m2good=where( finite(dt.mag_array[1,*]) eq 1)
m2ugood=where(finite(dt.mag_array[1,*]) eq 1  and  finite(dt.mag_array[3,*]) eq 1)
uvgood=where( finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[1,*]) eq 1)
m2uvgood=where(finite(dt.mag_array[1,*]) eq 1  and   finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[5,*]) eq 1)



oploterror, dt.time_array[m2good]-referenceepoch[0], dt.mag_array[1,m2good]-host.dm_best_array[n], dt.magerr_array[1,m2good], linestyle=2, psym=-(psymall[n]), symsize=sizes[n], color=cgcolor(colors[n]), errcolor=cgcolor(colors[n]), hatlength=0


endif

endfor


;cgAxis, YAxis=1,YRange=abs(m2abs_range-20),  yticks=nm2absticks,charsize=1, yminor=1, ytitle='Distance Modulus Limit', /Save

H_0=72.0
c_kms=3.0*10.0^5.0
dm=34.0
;dm=[30.0,31,32,33,34,35,36,37,38,39,40,41,42,43,44]
z=H_0/c_kms*10.0^((dm-25.0)/5.0)

zticks=['0.0024','0.0038','0.006','0.01',' 0.015','0.024','0.038','0.06','0.1','0.15','0.24','0.38','0.60','0.96','1.51']

;  using cosmology calculator
zticks=['0.0023','0.0037','0.0059','0.0092','0.015','0.023', '0.036','0.056','0.087','0.13','0.20','0.3','0.45','0.66','0.95']
zticks=['0.002','0.004','0.006','0.009','0.015','0.023', '0.036','0.056','0.087','0.13','0.20','0.3','0.45','0.66','0.95', ' ']


cgAxis, YAxis=1,YRange=abs(m2abs_range-20),  yticks=nm2absticks, charsize=1, yminor=1, ytitle='Redshift Limit for Swift Observations', ytickname=zticks, color='black', /Save

;;;

;al_legend, SNlegend,   psym=psym, symsize=sizes, color=colors, $
;pos=[0.517,0.665], /norm, charsize=0.8, box=1, background_color='white'



device, /close
SET_PLOT, 'X'



$ open m2absplot.eps


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;   NORMAL COLOR   ;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

SET_PLOT, 'PS'

device, filename='m2-v_all.eps', /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=fontsize
;;;;;;;;;;;;;;;;;


;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; bottom left
cgplot, xdata, ydata, /nodata, /noerase, position=[x1,y1,x2,y2], $
xtitle='Days since UV Peak Brightness',   ytitle='uvm2 - v', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=m2v_range, ystyle=1, xrange=time_range, xstyle=1, color=black, $
xticks=ntimeticks, xtickv=xtickvalues, yticks=nm2vticks, ytickv=ytickvalues



for n=0,nSNe-1 do begin

	SNname=host.SNname_array[n]

	print, SNname

	datafilenamesousa='$SOUSA/data/prelimdata/'+SNname+'_uvotB15.1.dat'

	if file_test(datafilenamesousa) eq 1 then begin
		;; Swift data
		pjb_phot_array_B141, datafilenamesousa, dt=dt

		nfiltersinepoch=intarr(n_elements(dt.time_array))
		filtercheck=intarr(n_elements(dt.time_array),6)
		for q=0,n_elements(dt.time_array)-1 do for f=0,5 do filtercheck[q,f]=finite(dt.mag_array[f,q])
		for q=0,n_elements(dt.time_array)-1 do nfiltersinepoch[q]=total(filtercheck[q,*]) 
		all6=where(nfiltersinepoch eq 6)
		n6epochs=n_elements(all6)

		referenceepoch=dt.time_array[where(dt.mag_array[1,*] eq min(dt.mag_array[1,*],/nan))]



vvgood=where( finite(dt.mag_array[5,*]) eq 1)
uugood=where( finite(dt.mag_array[3,*]) eq 1)
m2good=where( finite(dt.mag_array[1,*]) eq 1)
m2ugood=where(finite(dt.mag_array[1,*]) eq 1  and  finite(dt.mag_array[3,*]) eq 1)
m2vgood=where(finite(dt.mag_array[1,*]) eq 1  and  finite(dt.mag_array[5,*]) eq 1)
uvgood=where( finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[1,*]) eq 1)
m2uvgood=where(finite(dt.mag_array[1,*]) eq 1  and   finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[5,*]) eq 1)



oploterror, dt.time_array[m2vgood]-referenceepoch[0], dt.mag_array[1,m2vgood]-dt.mag_array[5,m2vgood], dt.magerr_array[1,m2good], linestyle=2, psym=-(psymall[n]), symsize=sizes[n], color=cgcolor(colors[n]), errcolor=cgcolor(colors[n]), hatlength=0

endif
endfor



;al_legend, SNlist,   psym=psymall, symsize=0.8, color=colors, $
;pos=[0.665,0.47], /norm, charsize=0.8, box=1, background_color='white'



device, /close
SET_PLOT, 'X'


spawn, 'open m2-v_all.eps'


bluest=reverse(sort(bluestm2v_array))

for n=0, nSNe-1 do print, host.SNname_array[bluest[n]], ' ', host.SNtype_array[bluest[n]], ' ', bluestm2v_array[bluest[n]]

print, 'final stop'
stop


end





