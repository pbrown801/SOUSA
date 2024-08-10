download from https://www.wis-tns.org/system/files/tns_public_objects/tns_public_objects.csv.zip

copy into this folder

run getAltData.py   creates altnames.json

run PossibleSwiftSupernovae.py  creates PossibleSwiftSupernovae.csv

(the code to update found.json was not found, so I used the above csv in MatchSwiftTNS.py)
run MatchSwiftTNS.py creates MatchedSwiftTNS.csv
>ra and dec are in a different format.  
>TNS prefix column can be dropped.  
> Alternate names should be added.
> drop duplicates


this was then combined via excel with the headers of SwiftSNweblist2016PTF.csv to create SwiftSNweblist2016on.csv

duplicates were trimmed by hand as spotted. (a lot from 2016 as 
SwiftSNweblist2016PTF.csv went through 2016hzm and 2016on started at the beginning of 2016)(.
saved as TrimmedAllSwiftSNlist.csv





SwiftSNyears.py takes TrimmedAllSwiftSNlist.csv and makes SortedTrimmedAllSwiftSNlist.csv and SwiftSNyears.png -- a histogram of Swift SNe per year 


SN_histogram makes the plot with the other UV satelites.  Plot has to be scaled to make labels visible.



SwiftSNtypes.py creates TypedSortedTrimmedAllSwiftSNlist.csv with two new columns --standardtype and broadtype
standard type is based on the TNS labels to make things more uniform while preserving the questioning of the original column.
a column for the classification source is needed, filled in with a TNS query if appropriate
but a TNS classification should not override a manual one
eventually all manual ones should also have a reference
broadgroups uses Ia, SE CCSN, II, and n for those groups.


SNpie.py is Eddie's code to make a donut pie chart with the broad type and subtypes.  This should be updated to use the new columns in TypedSortedTrimmedAllSwiftSNlist.csv


