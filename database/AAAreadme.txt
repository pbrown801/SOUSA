download from https://www.wis-tns.org/system/files/tns_public_objects/tns_public_objects.csv.zip

copy into this folder

unzip tns_public_objects.csv.zip 

python getAltData.py   creates altnames.json from tns



# use jupyter notebook instead python PossibleSwiftSupernovae.py  creates PossibleSwiftSupernovae.csv

(the code to update found.json was not found, so I used the above csv in MatchSwiftTNS.py)

%%%

ProfBrown — 9/11/25, 12:02 PM
except: #shouldn't ever happen... every comp sci major's famous last words
        print(f"Something went wrong! Skipping for now...\n")
ssally
 — 9/11/25, 12:02 PM
LOL
I remember this
It’a happened before a few times, only when the API is completely down
ProfBrown — 9/11/25, 12:06 PM
I pasted your code into a jupyter notebook and it isn't giving the same error.  Sometimes my terminal is fussy because some things were installed for the Mac M1 chip and others were pretending it was the Intel chip.
ssally
 — 9/11/25, 12:06 PM
yea, programming is one of the most frustrating things I’ve done
for the record, most of my work could now be one shotted by ChatGPT or Claude, they are powerful
ProfBrown — 9/11/25, 12:24 PM
Well, your code gave me what I needed, so I'll keep using it for now

%%%


jupyter notebook PossibleSwiftSNe.py

makes PossibleSwiftSupernovae.csv

python MatchSwiftTNS.py creates MatchedSwiftTNS.csv


>ra and dec are in a different format.  
>TNS prefix column can be dropped.  
> Alternate names should be added.
> drop duplicates


this was then combined via excel with the headers of SwiftSNweblist2016PTF.csv to create SwiftSNweblist2016on.csv

duplicates were trimmed by hand as spotted. (a lot from 2016 as 
SwiftSNweblist2016PTF.csv went through 2016hzm and 2016on started at the beginning of 2016)(.
saved as TrimmedAllSwiftSNlist.csv



240228 version with help of chatGPT

python mergeoldSwiftnewTNSchatgpt.py creates CombinedTrimmedAllSwiftSNlist.csv

complete duplicates dropped, conflicting rows fixed by hand in CombinedTrimmedAllSwiftSNlist


cp CombinedTrimmedAllSwiftSNlist.csv CombinedTrimmedAllSwiftSNlist.orig.csv
cp CombinedTrimmedAllSwiftSNlist2026.csv CombinedTrimmedAllSwiftSNlist.csv


cp CombinedTrimmedAllSwiftSNlist2026.csv FinalforSwiftSNyears.csv

SwiftSNyears.py takes FinalforSwiftSNyears.csv
 and makes SortedCombinedTrimmedAllSwiftSNlist.csv.csv and SwiftSNyears.png -- a histogram of Swift SNe per year 


SN_histogram makes the plot with the other UV satelites.  Plot has to be scaled to make labels visible.



SwiftSNtypes.py creates TypedSortedTrimmedAllSwiftSNlist.csv with two new columns --standardtype and broadtype
standard type is based on the TNS labels to make things more uniform while preserving the questioning of the original column.
a column for the classification source is needed, filled in with a TNS query if appropriate
but a TNS classification should not override a manual one
eventually all manual ones should also have a reference
broadgroups uses Ia, SE CCSN, II, and n for those groups.


SNpie.py is Eddie's code to make a donut pie chart with the broad type and subtypes.  This should be updated to use the new columns in TypedSortedTrimmedAllSwiftSNlist.csv


