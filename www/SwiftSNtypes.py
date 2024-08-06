"""
Standardize SN types
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib



inputcsv='SortedTrimmedAllSwiftSNlist.csv'
swift= pd.read_csv(inputcsv,on_bad_lines='warn',delimiter=',')

newlist = [] #empty list we'll add objects that meet the criteria

if 'broadtype' not in swift:
    swift['broadtype']=" "
if 'standardtype' not in swift:
    swift['standardtype']=" "


for i, name in enumerate(swift.SNname): #go through doc
    print(name)
    
    if swift.loc[i,'type'].strip() == 'SNIa':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia'
         
    elif swift.loc[i,'type'].strip() == 'SNIa-91T-like':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-91T'
        continue
 
    elif swift.loc[i,'type'].strip() == 'Ia-91bg-like':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'SNIa-91bg'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SNIa-pec':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-pec'
        continue

    elif swift.loc[i,'type'].strip() == 'SNIa-pec?':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-pec'
        continue

    elif swift.loc[i,'type'].strip() == 'SNIax[02cx-like]':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Iax'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SNIax':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Iax'
        continue
 
 
    elif swift.loc[i,'type'].strip() == 'SN02cx-like]':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Iax'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SNIa-CSM ':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-CSM '
        continue
  
    elif swift.loc[i,'type'].strip() == 'SNIa-SC':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-SC'
        continue
  
    elif swift.loc[i,'type'].strip() == 'SNIa-SuperChandra':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-SC'
        continue
  
    elif swift.loc[i,'type'].strip() == 'SNIa-Ca-rich':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-Ca-rich'
        continue

    elif swift.loc[i,'type'].strip() == 'SNII':
        swift.loc[i,'broadtype'] = 'II'
        swift.loc[i,'standardtype'] = 'II'
        continue
  
    elif swift.loc[i,'type'].strip() == 'SNIIP':
        swift.loc[i,'broadtype'] = 'II'
        swift.loc[i,'standardtype'] = 'IIP'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SNIIL':
        swift.loc[i,'broadtype'] = 'II'
        swift.loc[i,'standardtype'] = 'IIL'
        continue
  
    elif swift.loc[i,'type'].strip() == 'SNIIn':
        swift.loc[i,'broadtype'] = 'n'
        swift.loc[i,'standardtype'] = 'IIn'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SLSN-II':
        swift.loc[i,'broadtype'] = 'II'
        swift.loc[i,'standardtype'] = 'II'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SLSN-IIn':
        swift.loc[i,'broadtype'] = 'n'
        swift.loc[i,'standardtype'] = 'SLSN-II'
        continue

    elif swift.loc[i,'type'].strip() == 'SNII-pec':
        swift.loc[i,'broadtype'] = 'II'
        swift.loc[i,'standardtype'] = 'II-pec'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SNIIn-pec':
        swift.loc[i,'broadtype'] = 'n'
        swift.loc[i,'standardtype'] = 'IIn-pec'
        continue
  
    elif swift.loc[i,'type'].strip() == 'SNIIb':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'IIb'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SNIb':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ib'
        continue
  
    elif swift.loc[i,'type'].strip() == 'SNIc':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ic'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SNIc-BL':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ic-BL'
        continue
  
    elif swift.loc[i,'type'].strip() == 'SNIb/c':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ib/c'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SNIbn':
        swift.loc[i,'broadtype'] = 'n'
        swift.loc[i,'standardtype'] = 'Ibn'
        continue
  
    elif swift.loc[i,'type'].strip() == 'SNIb-pec':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ib-pec'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SNIb-Ca-rich':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ib-Ca-rich'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SNIc-Ca-rich':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ic-Ca-rich'
        continue

    elif swift.loc[i,'type'].strip() == 'SNIcn':
        swift.loc[i,'broadtype'] = 'n'
        swift.loc[i,'standardtype'] = 'Icn'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SNIc-pec':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ic-pec'
        continue
  
    elif swift.loc[i,'type'].strip() == 'SNIbn/Icn':
        swift.loc[i,'broadtype'] = 'n'
        swift.loc[i,'standardtype'] = 'Ibn/Icn'
        continue
 
 
 
 
 
 
     
    if swift.loc[i,'type'].strip() == 'Ia':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia'
         
    elif swift.loc[i,'type'].strip() == 'Ia-91T-like':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-91T'
        continue
         
    elif swift.loc[i,'type'].strip() == 'Ia-91T':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-91T'
        continue

    elif swift.loc[i,'type'].strip() == 'Ia-91bg':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-91bg'
        continue

    elif swift.loc[i,'type'].strip() == 'Ia-91bg-like':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-91bg'
        continue

    elif swift.loc[i,'type'].strip() == 'Ia-pec':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-pec'
        continue

    elif swift.loc[i,'type'].strip() == 'Ia-p':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-pec'
        continue

    elif swift.loc[i,'type'].strip() == 'Iax[02cx-like]':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Iax'
        continue
 
    elif swift.loc[i,'type'].strip() == 'Iax':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Iax'
        continue
 
 
    elif swift.loc[i,'type'].strip() == '02cx-like]':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Iax'
        continue
 
    elif swift.loc[i,'type'].strip() == 'Ia-02cx]':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Iax'
        continue

    elif swift.loc[i,'type'].strip() == 'Ia-CSM':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-CSM'
        continue
  
    elif swift.loc[i,'type'].strip() == 'Ia-SC':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-SC'
        continue
  
    elif swift.loc[i,'type'].strip() == 'Ia-SuperChandra':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-SC'
        continue
  
    elif swift.loc[i,'type'].strip() == 'Ia-Ca-rich':
        swift.loc[i,'broadtype'] = 'Ia'
        swift.loc[i,'standardtype'] = 'Ia-Ca-rich'
        continue

    elif swift.loc[i,'type'].strip() == 'II':
        swift.loc[i,'broadtype'] = 'II'
        swift.loc[i,'standardtype'] = 'II'
        continue
  
    elif swift.loc[i,'type'].strip() == 'IIP':
        swift.loc[i,'broadtype'] = 'II'
        swift.loc[i,'standardtype'] = 'IIP'
        continue
 
    elif swift.loc[i,'type'].strip() == 'IIL':
        swift.loc[i,'broadtype'] = 'II'
        swift.loc[i,'standardtype'] = 'IIL'
        continue
  
    elif swift.loc[i,'type'].strip() == 'IIn':
        swift.loc[i,'broadtype'] = 'n'
        swift.loc[i,'standardtype'] = 'IIn'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SLSN-II':
        swift.loc[i,'broadtype'] = 'II'
        swift.loc[i,'standardtype'] = 'II'
        continue
  
    elif swift.loc[i,'type'].strip() == 'II-pec':
        swift.loc[i,'broadtype'] = 'II'
        swift.loc[i,'standardtype'] = 'II-pec'
        continue
  
    elif swift.loc[i,'type'].strip() == 'II-87A':
        swift.loc[i,'broadtype'] = 'II'
        swift.loc[i,'standardtype'] = 'II-pec'
        continue
  
    elif swift.loc[i,'type'].strip() == 'II-87K':
        swift.loc[i,'broadtype'] = 'II'
        swift.loc[i,'standardtype'] = 'II-pec'
        continue

    elif swift.loc[i,'type'].strip() == 'IIn-pec':
        swift.loc[i,'broadtype'] = 'n'
        swift.loc[i,'standardtype'] = 'IIn-pec'
        continue
  
    elif swift.loc[i,'type'].strip() == 'IIb':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'IIb'
        continue
 
    elif swift.loc[i,'type'].strip() == 'Ib':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ib'
        continue
  
    elif swift.loc[i,'type'].strip() == 'Ic':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ic'
        continue
  
    elif swift.loc[i,'type'].strip() == 'Ibc':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ib/c'
        continue

    elif swift.loc[i,'type'].strip() == 'Ic-BL':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ic-BL'
        continue
 
    elif swift.loc[i,'type'].strip() == 'Ic-bl':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ic-BL'
        continue

    elif swift.loc[i,'type'].strip() == 'Ib/c':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ib/c'
        continue
 
    elif swift.loc[i,'type'].strip() == 'Ibn':
        swift.loc[i,'broadtype'] = 'n'
        swift.loc[i,'standardtype'] = 'Ibn'
        continue
  
    elif swift.loc[i,'type'].strip() == 'Ib-pec':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ib-pec'
        continue
 
    elif swift.loc[i,'type'].strip() == 'Ib-Ca-rich':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ib-Ca-rich'
        continue
 
    elif swift.loc[i,'type'].strip() == 'Ic-Ca-rich':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ic-Ca-rich'
        continue

    elif swift.loc[i,'type'].strip() == 'Icn':
        swift.loc[i,'broadtype'] = 'n'
        swift.loc[i,'standardtype'] = 'Icn'
        continue
 
    elif swift.loc[i,'type'].strip() == 'Ic-pec':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'Ic-pec'
        continue
  
    elif swift.loc[i,'type'].strip() == 'Ibn/Icn':
        swift.loc[i,'broadtype'] = 'n'
        swift.loc[i,'standardtype'] = 'Ibn/Icn'
        continue
 
    elif swift.loc[i,'type'].strip() == 'SLSN-I':
        swift.loc[i,'broadtype'] = 'SE CC'
        swift.loc[i,'standardtype'] = 'SLSN-I'
        continue
 

    else:
        print(f"{name} of type {swift.loc[i,'type']} did not process")


print(swift.standardtype)

swift.to_csv('Typed'+inputcsv, index= False)
