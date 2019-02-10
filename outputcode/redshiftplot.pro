pro redshiftplot


readcol, '$SNFOLDER/www/SwiftSN/SwiftSNweblist.txt', SNname, PSNname, SNname2, Host, redshift, type, nobs, format='a,a,a,a,f,a,i'

;for n=0,n_elements(SNname)-1 do print, SNname[n], redshift[n]

ia=where(type eq 'Ia')
goodia=where(type eq 'Ia' and nobs gt 2)

plothist, redshift[goodia], bin=0.002

SNianame=SNname[goodia]
SNiaredshifts=redshift[goodia]

;;;;;;;

zp05=fltarr(51)
for i=0,n_elements(zp05)-1 do zp05[i]=0.001+0.001*i

zp5=fltarr(102)
for i=0,n_elements(zp5)-1 do zp5[i]=-0.005+0.005*i

nearredshifts=fltarr(n_elements(zp05))
for i=0,n_elements(zp05)-2 do nearredshifts[i]=n_elements(where(redshift ge zp05[i] and redshift lt zp05[i+1]))

for i=0,n_elements(zp05)-2 do if (n_elements(where(redshift ge zp05[i] and redshift lt zp05[i+1])) eq 1 ) then if( where(redshift ge zp05[i] and redshift lt zp05[i+1]) eq -1) then nearredshifts[i]=0



allredshifts=fltarr(n_elements(zp5))
for i=0,n_elements(zp5)-2 do allredshifts[i]=n_elements(where(redshift ge zp5[i] and redshift lt zp5[i+1]))

for i=0,n_elements(zp5)-2 do if (n_elements(where(redshift ge zp5[i] and redshift lt zp5[i+1])) eq 1 ) then if( where(redshift ge zp5[i] and redshift lt zp5[i+1]) eq -1) then allredshifts[i]=0



iaredshifts=fltarr(n_elements(zp05))
for i=0,n_elements(zp05)-2 do iaredshifts[i]=n_elements(where(redshift[ia] ge zp05[i] and redshift[ia] lt zp05[i+1]))


for i=0,n_elements(zp05)-2 do if (n_elements(where(redshift[ia] ge zp05[i] and redshift[ia] lt zp05[i+1])) eq 1 ) then if( where(redshift[ia] ge zp05[i] and redshift[ia] lt zp05[i+1]) eq -1) then iaredshifts[i]=0





nplots=1
; from http://www.iluvatar.org/~dwijn/idlfigures
!p.font = 1
!p.thick = 2
!x.thick = 2
!y.thick = 2
!z.thick = 2
; the default size is given in centimeters
; 8.8 is made to match a journal column width
xsize = 8.8
;xsize = 18.0
wall = 0.03
; margin might need to be increased to accomodate the y-axis units
margin=0.14
a = xsize/8.8 - (margin + wall)
b = a * 2d / (1 + sqrt(5))

ysize = (margin + 1.0*(b + wall ) )*xsize
ticklen = 0.01
xticklen = ticklen/b
yticklen = ticklen/a

x1 = margin*8.8/xsize
x2 = x1 + a*8.8/xsize
xc = x2 + wall*8.8/xsize
y1 = margin*8.8/ysize
y2 = y1 + b*8.8/ysize
y3 = y2 + wall*8.8/ysize
y4 = y3 + b*8.8/ysize
yc = y4 + wall*8.8/ysize
xrange=[0,0.05]
yrange1=[0,9]
yrange2=[0,9]

nxticks=5
nyticks=9

fontsize=12
figurename='redshift_SwiftSNeIa.eps'

plotstyle='PS'

SET_PLOT, plotstyle

if plotstyle eq 'JPEG' then fontsize=14

device, filename=figurename,  /encapsulated, xsize=xsize*2.0, ysize=ysize*2.0, $
/tt_font, set_font='Times', font_size=18, bits_per_pixel=8, /color

plot, xrange, yrange2, /nodata, /noerase, position=[x1,y1,x2,y2], $
ytitle='Number of Swift SNe Ia', xtitle='Redshift z', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[0,12], ystyle=1, xrange=xrange, xstyle=1, $
xticks=nxticks, xtickv=xtickvalues, yticks=6, ytickv=ytickvalues

  cgBarPlot, iaredshifts, ytitle=ytitle_top, xtitle='Redshift z', Colors='forest green' , /overplot

device, /close
SET_PLOT, 'X'
$open redshift_SwiftSNeIa.eps


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
figurename='redshift_allSNe.eps'

plotstyle='PS'

SET_PLOT, plotstyle

device, filename=figurename,  /encapsulated, xsize=xsize*2.0, ysize=ysize*2.0, $
/tt_font, set_font='Times', font_size=18, bits_per_pixel=8, /color

plot, xrange, yrange2, /nodata, /noerase, position=[x1,y1,x2,y2], $
ytitle='Number of Swift SNe ', xtitle='Redshift z', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[0,80], ystyle=1, xrange=[0,0.5], xstyle=1, $
xticks=5, xtickv=xtickvalues, yticks=4, ytickv=ytickvalues

;  cgBarPlot, allredshifts, ytitle=ytitle_top, xtitle='Redshift z', Colors='forest green' , /overplot
  cgBarPlot, allredshifts, ytitle=ytitle_top, xtitle='Redshift z', Colors='forest green' , /overplot

farp1=where(redshift ge 0.1)

xoffsets=[-0.005, 0.00002, 0.005, 0.0, -0.000002, 0.0, -0.01, -0.01, 0.005, 0.0, 0.000002  ]

yoffsets=[0.0, 0.0, 0.0, 0.0,  0.0, 0.0, 0.0, 0.0, 25, 0.0, 25   ]

;for x=0,n_elements(farp1)-1 do print, SNname[farp1[x]], redshift[farp1[x]]

for x=0,n_elements(farp1)-1 do XYOutS, redshift[farp1[x]]+xoffsets[x], 10+yoffsets[x], SNname[farp1[x]], Orientation=90.0


device, /close
SET_PLOT, 'X'
$open redshift_allSNe.eps



;;;;;;;;;;;;;;;;;;



figurename='redshift_allSNep05.eps'

plotstyle='PS'

SET_PLOT, plotstyle

device, filename=figurename,  /encapsulated, xsize=xsize*2.0, ysize=ysize*2.0, $
/tt_font, set_font='Times', font_size=18, bits_per_pixel=8, /color

plot, xrange, yrange2, /nodata, /noerase, position=[x1,y1,x2,y2], $
ytitle='Number of Swift SNe ', xtitle='Redshift z', charsize=1.0, $
xminor=1, yminor=1, xticklen=xticklen, yticklen=yticklen, $
 yrange=[0,30], ystyle=1, xrange=[0,0.05], xstyle=1, $
xticks=5, xtickv=xtickvalues, yticks=6, ytickv=ytickvalues

  cgBarPlot, nearredshifts, ytitle=ytitle_top, xtitle='Redshift z', Colors='forest green' , xrange=[0,0.05], /overplot

device, /close
SET_PLOT, 'X'
$open redshift_allSNep05.eps


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


print, 'last stop'

stop
end






