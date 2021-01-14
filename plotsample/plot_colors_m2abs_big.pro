
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

pro plot_colors_m2abs_big

restore, '$DROPSN/www/SwiftSN/host.sav'

SNtypes=host.SNtype_array

nSNe=n_elements(host.SNtype_array)

templatearray=intarr(nSNe)

slsne=where(strmatch(SNtypes, '*SLSN*') eq 1)
slsneii=where(strmatch(SNtypes, '*SLSN*') eq 1 and strmatch(SNtypes, '*ii*') eq 1)
slsneiin=where(strmatch(SNtypes, '*SLSN*') eq 1 and strmatch(SNtypes, '*iin*') eq 1)

host.SNtype2_array[slsne]='SLSNI'
host.SNtype2_array[slsneii]='SLSNII'
host.SNtype2_array[slsneiin]='SLSNIIn'

colors=make_array(nSNe,value='grey')

colors[where( host.SNtype2_array eq 'Ia' ) ] ='red'		
colors[where( host.SNtype2_array eq 'Ibc' ) ] ='dark green'		
colors[where( host.SNtype2_array eq 'II'  ) ] ='blue'		
colors[where( host.SNtype_array  eq 'IIn'   ) ] ='purple'		
colors[where( host.SNtype2_array eq 'SLSN' ) ] ='black'
colors[where( host.SNtype2_array eq 'SLSNI' ) ] ='dark green'
colors[where( host.SNtype2_array eq 'SLSNII' ) ] ='blue'
colors[where( host.SNtype2_array eq 'SLSNIIn' ) ] ='purple'
colors[where( host.SNname_array eq 'ASASSN-15lh' ) ] ='white'



SNlist=host.SNname_array



psym=[18,17,4,5,6,9,7,11,23,25]
psymall=intarr(nSNe)
for n=0,nSNe-1 do psymall[n]= psym[n mod 10]
sizes=make_array(nSNe,value=0.4)
sizes[where( host.SNtype2_array eq 'Ia' ) ] =0.2		

;;;;;;;;;;;;;;;;;

nplots=2
; from http://www.iluvatar.org/~dwijn/idlfigures


nxticks=10
nyticks=12



xdata=[0,1,2,3]
ydata=[2,3,4,5]

epochlimit=80

time_range=[-20,80]
m2u_range=[-1.5,5.5]
m2v_range=[-2,7]
uv_range=[-1.5,3.5]
m2abs_range=[-10,-25]
uabs_range=[-12,-24]

ntimeticks=10
nm2uticks=7
nuvticks=5
nm2vticks=9
nm2absticks=15
nuabsticks=12

fontsize=180
dt=0.7
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;   NORMAL COLOR   ;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

SET_PLOT, 'PS'

device, filename='m2plotsbig.eps', /encapsulated, xsize=160, ysize=200, $
/tt_font, set_font='Times', font_size=fontsize
;;;;;;;;;;;;;;;;;


;;;;;;;;;;;;;;;;;;;;;;;;;
;;; top left
;;;
;;; uvm2 abs v time

cgplot, xdata, ydata, /nodata, /noerase, position=[0.1,0.55,0.80, 0.99], $
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



vvgood=where( finite(dt.mag_array[5,*]) eq 1)
uugood=where( finite(dt.mag_array[3,*]) eq 1)
m2good=where( finite(dt.mag_array[1,*]) eq 1)
m2ugood=where(finite(dt.mag_array[1,*]) eq 1  and  finite(dt.mag_array[3,*]) eq 1)
uvgood=where( finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[1,*]) eq 1)
m2uvgood=where(finite(dt.mag_array[1,*]) eq 1  and   finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[5,*]) eq 1)



oploterror, dt.time_array[m2good]-referenceepoch[0], dt.mag_array[1,m2good]-host.dm_best_array[n], dt.magerr_array[1,m2good], linestyle=2, psym=-(psymall[n]), symsize=sizes[n], color=cgcolor(colors[n]), errcolor=cgcolor(colors[n]), hatlength=0

endif
endfor


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; bottom left
cgplot, xdata, ydata, /nodata, /noerase, position=[0.1,0.1,0.80, 0.55], $
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



al_legend, SNlist[0:158],   psym=psymall[0:158], symsize=0.1759, color=colors[0:158], $
pos=[0.80,0.99], /norm, charsize=0.1759, box=1, background_color='white'
al_legend, SNlist[0+159:158+159],   psym=psymall[0+159:158+159], symsize=0.1759, color=colors[0+159:158+159], $
pos=[0.85,0.99], /norm, charsize=0.1759, box=1, background_color='white'
al_legend, SNlist[0+159+159:158+159+159],   psym=psymall[0+159+159:158+159+159], symsize=0.1759, color=colors[0+159+159:158+159+159], $
pos=[0.90,0.99], /norm, charsize=0.1759, box=1, background_color='white'
al_legend, SNlist[0+159+159+159:nSNe-1],   psym=psymall[0+159+159+159:nSNe-1], symsize=0.1759, color=colors[0+159+159+159:nSNe-1], $
pos=[0.95,0.99], /norm, charsize=0.1759, box=1, background_color='white'



device, /close
SET_PLOT, 'X'



$ open m2plotsbig.eps


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; now without legend

time_range=[-20,80]
m2u_range=[-1.5,5.5]
m2v_range=[-3,7]
uv_range=[-1.5,3.5]
m2abs_range=[-10,-23]
uabs_range=[-12,-24]

ntimeticks=10
nm2uticks=7
nuvticks=5
nm2vticks=10
nm2absticks=13
nuabsticks=12


SET_PLOT, 'PS'

device, filename='m2plotsbig_nolegend.eps', /encapsulated, xsize=160, ysize=200, $
/tt_font, set_font='Times', font_size=fontsize
;;;;;;;;;;;;;;;;;


;;;;;;;;;;;;;;;;;;;;;;;;;
;;; top left
;;;
;;; uvm2 abs v time

cgplot, xdata, ydata, /nodata, /noerase, position=[0.2,0.55,0.90, 0.99], $
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



vvgood=where( finite(dt.mag_array[5,*]) eq 1)
uugood=where( finite(dt.mag_array[3,*]) eq 1)
m2good=where( finite(dt.mag_array[1,*]) eq 1)
m2ugood=where(finite(dt.mag_array[1,*]) eq 1  and  finite(dt.mag_array[3,*]) eq 1)
uvgood=where( finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[1,*]) eq 1)
m2uvgood=where(finite(dt.mag_array[1,*]) eq 1  and   finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[5,*]) eq 1)



oploterror, dt.time_array[m2good]-referenceepoch[0], dt.mag_array[1,m2good]-host.dm_best_array[n], dt.magerr_array[1,m2good], linestyle=2, psym=-(psymall[n]), symsize=sizes[n], color=cgcolor(colors[n]), errcolor=cgcolor(colors[n]), hatlength=0

endif
endfor


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; bottom left
cgplot, xdata, ydata, /nodata, /noerase, position=[0.2,0.1,0.90, 0.55], $
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


device, /close
SET_PLOT, 'X'



$ open m2plotsbig_nolegend.eps

print, 'final stop'
stop
end
