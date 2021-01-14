# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 17:17:46 2020

@author: Alexander Crabtree

modified by Peter Brown Jan 12 2020 to put index file in root directory and fix links
"""
import numpy as np
import pandas as pd
import os
from os import path
import webbrowser



swift= pd.read_csv('NewSwiftSNweblist.csv')
swift= swift.drop(swift.index[0]) #delete header row
swift.dropna(subset=["SNname"], inplace= True) #drops all nan in SNname column
swift= swift.reset_index(drop=True) #reset the index from 0
swift = swift.replace(np.nan, '', regex=True) #turn all NANs into '' so it looks nice on webpage

#define all of the columns needed from Swift CSV

snname= swift.SNname 
host= swift.HostName 
othersn= swift.OtherName
red= swift.Redshift
#rounds the redshift numbers to the 6th decimal place
red= red.map(lambda x: round(x, 6) if isinstance(x, (int, float)) else x)
sntype= swift.type
psn= swift.PSN 

def topHTML(): #creates new HTML code for swift_sn_top.txt
    text= """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    
<html>

  <head>
  
    <meta http-equiv="content-type" content="text/html; charset=ISO-8859-1">
    
    <title>Swift Supernovae</title>
    
    <meta name="keywords" content="Swift, supernova, supernovae, SNe, gamma-ray
    , gamma ray, burst, BAT, UVOT, XRT, astronomy, satellite,observatory, GRB">
    
    <!--#include virtual="/docs/swiftheader.html"-->
    
    <meta content="Swift Supernova Team" name="author"> <meta content="Swift Supernova (SN) Team Aggienova Team TAMU NASA GSFC PSU" name="description">
    
  </head>
  
  <body>
  
    <h1 style="text-align: center;">Swift Supernovae<span style="font-style: italic;"></span><br></h1> 
    
    
    <table style="width: 800px; text-align: left; margin-left: auto;
      margin-right: auto;" border="0" cellpadding="1" cellspacing="0"> 
      
      <tbody>  <tr> <td style="vertical-align: top;"> <br> <br>
      
          </td> <td colspan="6" rowspan="1" style="vertical-align: top;"> <br>
          
          </td> </tr> <tr> <td colspan="7" rowspan="1" style="vertical-align: top;"> 
          <div style="text-align: justify;"><a href="www/SN100_Swift.png">
          <img src="www/SN100_Swift.png" alt="Swift SN Mosaic by Peter Brown, Swift rendering by NASA/Sonoma State University/Aurore Simonnet" style="border: 0px solid ; width: 800px; " align="center" hspace="5"> <br>
          
<br></a>Below is a list of young supernovae (SNe) observed by <a href="http://heasarc.gsfc.nasa.gov/docs/swift/">Swift</a>, along with Swift <a href="http://heasarc.gsfc.nasa.gov/docs/swift/about_swift/uvot_desc.html">Ultraviolet/Optical Telescope (UVOT)</a>, light curves and data (where available).  The Swift SN Mosaic above is by Peter Brown using actual observations and a Swift rendering by NASA/Sonoma State University/Aurore Simonnet.  A working list of publications is posted at:  
                <a href="http://ultravioletsupernova.blogspot.com/2013/10/swift-supernova-publications.html"> Swift Supernova Publications</a>.<br> <br>
                

</tr>  <tr>  <td colspan="7" rowspan="1" style="vertical-align: top;"> 
<div style="text-align: justify;"><a href="www/sousa_galaxy.png">
<img src="www/sousa_galaxy.png" alt="Swift Optical/Ultraviolet Supernova Archive" style="border: 0px solid ; width: 146px; height: 250px;" align="right" hspace="5"></a>


Swift's Optical/Ultraviolet Supernova Archive (SOUSA) is an effort to reprocess and rereduce all of the Swift 
supernova data  using the Breeveld et al. 2011 zeropoints and time-dependent sensitivity correction to be on the same system.  
Available data is linked from the sousaphone icons.  We are beginning with the already published supernovae which need to be 
updated to the new photometric zeropoints and those with host galaxy template observations, so most of those with data are at
 the bottom of the list.  The paper describing SOUSA has been published in the special UV issue of Astrophysics & Space Science. 
 <a href="http://adsabs.harvard.edu/abs/2014Ap%26SS.354...89B"> ADS link</a>.  This link discusses  
 <a href="http://ultravioletsupernova.blogspot.com/2015/03/sousa-data-use.html">how to cite</a>  SOUSA.  
 The <a href="https://archive.stsci.edu/prepds/sousa/">Mikulski Archive for Space Telescopes</a> is hosting the (large) 
 image sets if you want to do your own photometry on the supernovae or other objects in the field or the host galaxy. 
 If you just want the final light curves, click on the sousaphone links below for individual objects or download a tar file of 270+ supernovae  
 <a href="http://people.physics.tamu.edu/pbrown/SwiftSN/SOUSA160823.tar">here</a>.  
 To encourage the proper use of Swift data, especially in the case of converting to flux for use in creating spectral 
 energy distributions or bolometric light curves, I wrote a 
 <a href="http://ultravioletsupernova.blogspot.com/2016/08/interpreting-flux-from-broadband.html">paper</a> describing some of the complications.
<br>


<br>
Much of the data linked from this website is under construction and will be available at a later time.  
If you would like to be added to an e-mail list to find out when significant chunks of data have been added, 
report SNe missing from this list, or have any questions about Swift SNe, data, etc, please email uv dot supernova at gmail dot com  
If you want older versions of the data that were used in specific publications, please contact me via e-mail.-- Peter J. Brown <br></tr>

    </table>
    
    
    
    <table id= "SNTable"; style="width: 800px; text-align: left; margin-left: auto;
      margin-right: auto;" border="0" cellpadding="1" cellspacing="0">

              <div align="left"><br>
 	<tr>  <td style="vertical-align: top;"><br></td>
     
          <td colspan="6" rowspan="1" style="vertical-align: top; width:
            30px;"><br></td> 
            
          <tr class="header"> <th style="background-color: rgb(51, 51, 51); vertical-align:
            top; text-align: center;" align="center"><span style="color:
              rgb(255, 255, 255);">No.</span><br>
              </th>
              
              
          <th style="background-color: rgb(51, 51, 51); vertical-align:
            top; text-align: center;" align="center"><span style="color:
              rgb(255, 255, 255);">Supernova</span><br>
              </th> 
            
          <th style="background-color: rgb(51, 51, 51); vertical-align:
            top; text-align: center;" align="center"><span style="color:
              rgb(255, 255, 255);">Host
              Galaxy</span><br>
              </th> 
              
          <th style="background-color: rgb(51, 51, 51); vertical-align:
            top; text-align: center;" align="center"><span style="color:
              rgb(255, 255, 255);">Redshift</span><br>
              </th> 
              
          <th style="background-color: rgb(51, 51, 51); vertical-align:
            top; text-align: center;" align="center"><span style="color:
              rgb(255, 255, 255);">Type&nbsp;</span><br>
              </th> 
            
          <th style="background-color: rgb(51, 51, 51); vertical-align:
            top; text-align: center;" align="center"><span style="color:
              rgb(255, 255, 255);">Image&nbsp; |&nbsp; Plot&nbsp;          |&nbsp; Data</span><br></th>  
        </tr>  
        <tr class="header">
          <td vertical-align: top; text-align: center;" align="center"><br></td>  
              
          <td vertical-align: top; text-align: center;" align="center">
          <input type="text" id="SNInput" onkeyup="SNFunction()" placeholder="Supernova Name..."><br></td> 
          
          <td vertical-align: top; text-align: center;" align="center">
          <input type="text" id="HostInput" onkeyup="HostFunction()" placeholder="Host Galaxy Name..."><br></td>
          
          <td vertical-align: top; text-align: center;" align="center">
          <input type="text" id="RedshiftInput" onkeyup="RedshiftFunction()" placeholder="Redshift..."><br></td>
          
          <td vertical-align: top; text-align: center;" align="center">
          <input type="text" id="TypeInput" onkeyup="TypeFunction()" placeholder="Supernova Type..."><br></td>
          
          <td vertical-align: top; text-align: center;" align="center"><br></td>
          
          <td vertical-align: top; text-align: center;" align="center"><br></td>
          </tr>

<!-- copy template entry and replace values
<tr>

<td align="center" valign="top"> #.<br> </td>

<td align="center" valign="top"><b>SNname</b><br> &nbsp;PSN # <br></td> 

<td align="center" valign="top"><a href=" NED address "> Host Galaxy </a><br></td> 

<td align="center" valign="top"> redshift <br></td> 

<td align="center" valign="top"><a href=" CBET address "> type </a><br> </td>

<td align="center" valign="top"><a href="www/images/SNname_uvot.png">
<img src="pic.jpg" alt="Swift image" style="border: 0px
solid; border: 0px solid; width: 52px; height: 55px;"
border="0" height="55" width="52"></a>

<a href="http://people.physics.tamu.edu/pbrown/SwiftSN/SNname_lightcurve.jpg">
<img src="www/light.jpg" alt="Swift UVOT lightcurve"
style="border: 0px solid; border: 0px solid; width:
52px; height: 55px;" border="0" height="55" width="52"></a>

<a href="http://people.physics.tamu.edu/pbrown/SwiftSN/SNname_uvotB13.dat">
<img src="light.jpg" alt="Swift UVOT data"
style="border: 0px solid; border: 0px solid; width:
52px; height: 55px;" border="0" height="55" width="52"></a></td>

<td align="center" valign="top"><br> </td>

end of template entry --> <tr>"""

    return text

def printsnline(SNnamen, PSNn, SNname2n, galaxyn, redshiftn, typen, n): #creates new HTML code for swift_sn_middle.txt
    owd= os.getcwd()
    os.chdir('..')
#-----------------data,images, and lcplots relative paths --------------------------------------------------------------------

    data_path= "../data/"+SNnamen+"_uvotB15.1.dat"
    
    images_path= "../images/"+SNnamen+"_uvot.png"

    lcplots_path= "../lcplots/"+SNnamen+"_lightcurve.jpg"
    
#-----------------------------------------------------HTML text---------------------------------------------------------------

    text= """<tr> \n
    <td align="center" valign="top"> {n} <br></td> \n
             <td align="center" valign="top"><b> {SNnamen} </b><br> &nbsp; \n
             {PSNn} {SNname2n} \n
             <br> </td> \n
               <td align="center" valign="top"><a \n
                  href="http://ned.ipac.caltech.edu/forms/byname.html"> {galaxyn} </a><br> </td> \n
                     <td align="center" valign="top"> {redshiftn} <br> </td> \n
                        <td align="center" valign="top"><a \n
                        href="http://www.cbat.eps.harvard.edu/cbet/RecentCBETs.html"> {typen} </a><br> </td> \n
                         <td align="center" valign="top"><a \n""".format(**locals())

    #imagefile html section:
    if os.path.exists(images_path)== True:
#        textimage= """href="https://github.com/pbrown801/SOUSA/blob/master/images/{SNnamen}_uvot.png"><img \n
        textimage= """href="images/{SNnamen}_uvot.png"><img \n
                         src="www/pic.jpg" alt="Swift image" style="border: 0px solid; border: 0px solid; width: 52px; height: 55px;" \n
                          border="0" height="55" width="52"></a><a \n""".format(**locals())
        text+= textimage

    #lcfilename html section:
    if os.path.exists(lcplots_path) == True:
        textlc= """href="https://github.com/pbrown801/SOUSA/blob/master/lcplots/{SNnamen}_lightcurve.jpg"><img \n
                    src="www/light.jpg" alt="Swift UVOT lightcurve" \n
                     style="border: 0px solid; border: 0px solid; width: \n
                      52px; height: 55px;" border="0" height="55" width="52"></a><a \n""".format(**locals())
        text+= textlc
                    
    #datafilenmesousa html section:
    if os.path.exists(data_path) == True:
        textdata= """href="https://github.com/pbrown801/SOUSA/blob/master/data/{SNnamen}_uvotB15.1.dat"><img \n
                      src="www/sousa_galaxy_small.png" alt="Swift UVOT data" \n
                       style="border: 0px solid; border: 0px solid; width: \n
                        52px; height: 89px;" border="0" height="89" width="52"></a></td> \n""".format(**locals())
        text+= textdata

                   
    textend= """<td align="center" valign="top"><br> \n
                 </td>\n
                  </tr>"""
                  
                
    
    textcomb= text + textend
    os.chdir(owd)
    return(textcomb)

def bottomHTML(): #creates new HTML code for swift_sn_bottom.txt
    text= """
        <tr align="center">
          <td colspan="7" rowspan="1" style="vertical-align: top;">
            <hr style="width: 100%; height: 2px;"></td>
        </tr>
        <tr>
          <td style="vertical-align: top;"><br>
          </td>
          <td style="vertical-align: top; width: 50px; text-align:
            left;"><span style="font-weight: bold;">&nbsp; Links:</span><br>
          </td>
          <td colspan="5" rowspan="1" style="vertical-align: top;"><a
              href="http://www.cbat.eps.harvard.edu/lists/Supernovae.html">IAU
List

              of Supernovae</a><br>
            <a href="http://www.rochesterastronomy.org/supernova.html">Latest
SNe

              from Rochester Astronomy</a><br>
          </td>
        </tr>
      </tbody>
    </table>
    <!--#include virtual="/docs/swift/swift_footer.html"--><!--#include virtual="/docs/corpfooter.html"-->
    
    <script>

function SNFunction() {
  // Declare variables
  var filter, table, tr, td, i;

  filter = document.querySelector('#SNInput').value.toUpperCase();
  tr = document.querySelectorAll('#SNTable tr:not(.header)');

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
          
function HostFunction() {
  // Declare variables
  var filter, table, tr, td, i;

  filter = document.querySelector('#HostInput').value.toUpperCase();
  tr = document.querySelectorAll('#SNTable tr:not(.header)');

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[2];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function RedshiftFunction() {
  // Declare variables
  var filter, table, tr, td, i;

  filter = document.querySelector('#RedshiftInput').value.toUpperCase();
  tr = document.querySelectorAll('#SNTable tr:not(.header)');

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[3];
    if (td) {
      if (td.innerHTML.indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
          
function TypeFunction() {
  // Declare variables
  var filter, table, tr, td, i;

  filter = document.querySelector('#TypeInput').value.toUpperCase();

  tr = document.querySelectorAll('#SNTable tr:not(.header)');

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[4];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

  </script>
  
  </body>
</html> """

    return(text)

#writes top html text file
swifttop= open('new_swift_sn_top.txt', 'w')
swifttop.write(topHTML())
swifttop.close()     

#writes middle html text file
swiftmid= open('new_swift_sn_middle.txt', 'w')
for i in range(0,len(snname)):
    if snname[i].startswith(('in', '?', '#'),0,4) != True:
        swiftmid.write(printsnline(str(snname[i]),str(psn[i]),str(othersn[i]),str(host[i]),str(red[i]),str(sntype[i]), i+1))
swiftmid.close

#writes bottom html text file
swiftbot= open('new_swift_sn_bottom.txt', 'w')
swiftbot.write(bottomHTML())
swiftbot.close()

#Opens and reads the HTML code in the .txt files
import codecs
top= codecs.open("new_swift_sn_top.txt",'r')
mid= codecs.open("new_swift_sn_middle.txt", 'r')
bott= codecs.open("new_swift_sn_bottom.txt",'r')

html_t= top.read()
html_m= mid.read()
html_b= bott.read()

#defines a path for the website HTML combined code
path = os.path.abspath('../index.html')
url = 'file://' + path

#Runs all opened HTML .txt files in a browser
with open(path, 'w') as website:
    website.write(html_t)
    website.write(html_m)
    website.write(html_b)
webbrowser.open(url)


