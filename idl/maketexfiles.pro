pro maketexfiles
; spawn, 'ls ../*14.1.dat > files.dat'
;.run pjb_phot_array_B141

readcol, 'files.dat', files, format='a'
for n=0,n_elements(files)-1 do begin
print, files[n]
pjb_phot_array_B141, files[n], tex6file=files[n]+'.txt', dt=dt
endfor
print, 'final stop'
stop
end