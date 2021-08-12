
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

pro plot_m2lum



SNlist=['SN2011by','SN2007af', 'SN2005ke', 'SN2005hk', 'SN2012dn','SN2007Y',  'SN2006jc',   'SN2006aj',  'SN2011dh', 'SN2012aw', 'SN2008aw',   'SN2010jl', 'SN2008es']

SNlegend=['SN2011by - Ia-blue','SN2007af - Ia-red', 'SN2005ke - Ia-91bg', 'SN2005hk - Ia-02cx','SN2012dn - Ia SC','SN2007Y - Ib',  'SN2006jc - Ibn',  'SN2006aj - Ic/GRB',  'SN2011dh - IIb', 'SN2012aw - IIP', 'SN2008aw - IIL',   'SN2010jl - IIn', 'SN2008es - SLSNII']
SNexplosiondates=[55672.0,54157.12, 53685.77, 53685.1-15.0,56114,54163.3-20.0,  54018,  53784.1,  55712.5, 56002.0, 54526.5,   55470, 54590]
SNexplosionrefs=['Nugent_etal_2011','Brown_etal_2012a','Brown_etal_2012a', 'Phillips_etal_2007','Brown et al. 2013 peak -20','Stritzinger_etal_2009 B peak - 20', 'Nakana_etal_2006 a few days before discovery',   'Campana_etal_2006 GRB trigger time',  'Arcavi_etal_2011', 'Fraser_etal_2012', 'discover - 1.5 days',   'ten days before first observation Stoll et al. 2011', 'ten days before first observation']


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;; set values of constants
H_0=72.0     ;
H_0_err=5.0;
vel_thermal=200.0     ; uncertainty in velocity of galaxies due to thermal/gravitational 
                      ; motion after large scale structure has been removed



nSNe=n_elements(SNlist)

colors=['red','maroon', 'orange', 'orange red','magenta','dark green', 'lawn green',  'black', 'turquoise', 'blue', 'royal blue',   'purple', 'grey']

symnum=[4,5,6,9,7,11,23,25,27,29,35,37,41,4,5,6,9,7,11,23,25,27,29,35,37,41]
symnum=symnum[0:nSNe-1]
psym=[18,17,4,5,6,9,7,11,23,25,27,29,35,37,41,4,5,6,9,7,11,23,25,27,29,35,37,41]
psym=psym[0:nSNe-1]
sizes=[0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8]
sizes=sizes[0:nSNe-1]


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

epochlimit=80

exptime_range=[0,epochlimit]
m2u_range=[-1.5,5.5]
m2v_range=[-2,8]
uv_range=[-1.5,3.5]
m2abs_range=[-10,-24]
m2lum_range=[38.0,44]
nm2uticks=7
nm2absticks=12


uabs_range=[-12,-24]

nexptimeticks=epochlimit/10
nuvticks=5
nm2vticks=10
nuabsticks=12

fontsize=14
dt=0.7
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;   NORMAL COLOR   ;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

SET_PLOT, 'PS'

device, filename='m2lumplot.eps', /encapsulated, xsize=xsize, ysize=ysize, $
/tt_font, set_font='Times', font_size=fontsize
;;;;;;;;;;;;;;;;;


;;;;;;;;;;;;;;;;;;;;;;;;;
;;; top left
;;;
;;; m2 abs v time

cgplot, xdata, ydata, /nodata, /noerase, position=[x1,y1,x2,y2], $
xtitle='Days Since Explosion',   ytitle='log (uvm2 luminosity) [ergs/s] (1900-2500 A)', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=m2lum_range, ystyle=1, xrange=[-2,78], xstyle=1, $
xticks=nexptimeticks, xtickv=xtickvalues, yticks=nm2absticks, ytickv=ytickvalues


for n=0,nSNe-1 do begin
	SNname=SNlist[n]
	print, SNname

	filename='$SOUSA/www/host.sav'
	restore, filename
	;;;;;; compute extinction magnitudes
	
	index=where(host.snname_array eq SNname)

	EBV_MW_SCHLAFLY=host.AV_SCHLAFLY_array[index]/3.1
	R_MW_92A=[6.44, 8.06, 5.45, 4.91, 4.16, 3.16]
	A_lambda=EBV_MW_SCHLAFLY[0]*R_MW_92A

	pjb_phot_array_B141, '$SOUSA/data/'+SNname+'_uvotB15.1.dat',   dt=dt, delta_t=0.4


	mu_best=host.dm_best_array[index]
	mu_best_err=host.dm_best_err_array[index]
	mu_best_ref=host.dm_best_ref_array[index]


vvgood=where( finite(dt.mag_array[5,*]) eq 1 and dt.time_array-SNexplosiondates[n] lt epochlimit)
uugood=where( finite(dt.mag_array[3,*]) eq 1  and dt.time_array-SNexplosiondates[n] lt epochlimit)
m2good=where( finite(dt.mag_array[1,*]) eq 1  and dt.time_array-SNexplosiondates[n] lt epochlimit)
m2ugood=where(finite(dt.mag_array[1,*]) eq 1  and  finite(dt.mag_array[3,*]) eq 1  and dt.time_array-SNexplosiondates[n] lt epochlimit)
uvgood=where( finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[1,*]) eq 1  and dt.time_array-SNexplosiondates[n] lt epochlimit)
m2uvgood=where(finite(dt.mag_array[1,*]) eq 1  and   finite(dt.mag_array[3,*]) eq 1  and  finite(dt.mag_array[5,*]) eq 1  and dt.time_array-SNexplosiondates[n] lt epochlimit)

;  oploterror, dt.time_array[m2good]-SNexplosiondates[n], dt.mag_array[1,m2good]-mu_best[0]-A_lambda[1], dt.magerr_array[1,m2good], linestyle=2, psym=-symcat(psym[n]), symsize=sizes[n], color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])
distance = 10.0d^((mu_best[0] + 5.0 ) /5.0)*3.086*10.0^18.0   ; in centimeters

; 8.5 *10^-16  flux density to count conversion
; width of wavelength range integrated by Chris
; 2504.7 A - 1898.6 A   M2 (4.95-6.53eV)
; wavelength range 606.1

;oploterror, dt.time_array[m2good]-SNexplosiondates[n], dt.counts_array[1,m2good]*(8.5*10.0^(-16)*606.1)*4.0*3.1416*distance^2.0, dt.magerr_array[1,m2good], linestyle=2, psym=-symcat(psym[n]), symsize=sizes[n], color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])



oploterror, dt.time_array[m2good]-SNexplosiondates[n], alog10(dt.counts_array[1,m2good]*(8.5*10.0^(-16)*606.1)*4.0*3.1416*distance^2.0), dt.magerr_array[1,m2good], linestyle=2, psym=-symcat(psym[n]), symsize=sizes[n], color=cgcolor(colors[n]), errcolor=cgcolor(colors[n])


endfor


;cgAxis, YAxis=1,YRange=abs(m2abs_range-20),  yticks=nm2absticks,charsize=1, yminor=1, ytitle='Distance Modulus Limit', /Save

H_0=72.0
c_kms=3.0*10.0^5.0
dm=34.0
;dm=[30.0,31,32,33,34,35,36,37,38,39,40,41,42,43,44]
z=H_0/c_kms*10.0^((dm-25.0)/5.0)

;  using cosmology calculator
;zticks=['0.002','0.004','0.006','0.009','0.015','0.023', '0.036','0.056','0.087','0.13','0.20','0.3','0.45','0.66','0.95']
;cgAxis, YAxis=1,YRange=abs(m2abs_range-20),  yticks=nm2absticks, charsize=1, yminor=1, ytitle='Redshift Limit', ytickname=zticks, /Save

;;;

al_legend, SNlegend,   psym=psym, symsize=sizes, color=colors, $
pos=[0.517,0.665], /norm, charsize=0.8, box=1, background_color='white'



device, /close
SET_PLOT, 'X'



$ open m2lumplot.eps
spawn, 'open m2lumplot.eps'
print, 'final stop'
stop


end





