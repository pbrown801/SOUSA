# -*- coding: utf-8 -*-
'''
Created on Sun Jan 24 12:54:40 2021

@author: Alexander Crabtree
            acrabtree15@gmail.com
'''
import pandas as pd
import requests
from bs4 import BeautifulSoup

swift= pd.read_csv('NewSwiftSNweblist.csv')

sntemp= pd.DataFrame({'SNname':swift['SNname']})

def SNdates(SNname):

    url = "https://www.wis-tns.org/object/"+SNname+"/discovery-cert"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    sn_data= soup.find_all('span', class_='underline')
    
    rec_date= soup.find_all('em', class_='placeholder')[3].text
    
    disc_date= sn_data[0].find_next_sibling('span').text
    disc_string= 'Discovery date: '

    lnd_date= sn_data[1].find_next_sibling('span').text
    lnd_string= 'Last non-detection date: '

    if disc_string in disc_date:
        disc_date= disc_date.replace(disc_string, '')
    
    if lnd_date in ['Archival info: DSS', 'Archival info: Other', 'Archival info: SDSS']:
        lnd_date= ''
        rec_date= "'" + rec_date
        disc_date= "'" + disc_date
        
    else:
        if lnd_string in lnd_date:
            lnd_date= lnd_date.replace(lnd_string, '')
        rec_date= "'" + rec_date
        disc_date= "'" + disc_date
        lnd_date= "'" + lnd_date

    return(rec_date, disc_date, lnd_date)

def GrabSNdates(SNname):
    try:
        rec,disc,lnd= SNdates(SNname)
    except Exception:
        rec,disc,lnd= '','',''
        
    return(pd.Series({'Date Recieved': rec, 'Discover date': disc, 'Last non-detection date': lnd}))

#print(SNdates('2019oys'))

rep= '|'.join(['SN'])
sntemp['SNname']= sntemp['SNname'].str.replace(rep, '')

swiftDates= pd.DataFrame(sntemp.apply(lambda row: GrabSNdates(row['SNname']), axis=1))
swift= pd.concat([swift,swiftDates], axis=1, sort=False)

swift.to_csv('NewSwiftSNweblist.csv', index= False)
