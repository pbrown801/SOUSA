import pandas as pd
import csv, json

#

SwiftNames=[]
SwiftTooTypes=[]
SwiftTooTypers=[]
SwiftRa=[]
SwiftDec=[]
SwiftTypes=[""]
SwiftRedshifts=[]
SwiftTNSprefix=[]
names, types, redshifts, ra, dec = [], [], [], [], []


with open("PossibleSwiftSupernovae.csv", newline="") as csvFile:
    
    reader = csv.reader(csvFile)

    for row in reader: # row is a list containing [name, type, ra, dec]
        
        SwiftNames.append(row[0].replace(" ","").replace("-","").upper())
        SwiftRa.append([row[2]])
        SwiftDec.append([row[3]])
        SwiftTypes.append("")
        SwiftRedshifts.append("")
        SwiftTNSprefix.append("")
  

# load all the json TNS  data as lowercased
with open('altnames.json', 'r') as json_file:
    json_data = json.load(json_file)

altnames = {}
for key, value in json_data.items():
    curr = []
    for item in value:
        item = item.strip()
        if item[-1] == ',': item = item[:-1]
        curr.append(item.lower())
    altnames[key] = curr



# search for cross-matches and missing redshifts
changed = 0
prefixes = ['ztf', 'ptf', 'iptf', 'atlas', 'dlt', 'gaia', 'asassn']
for i, name in enumerate(SwiftNames):
    name = name.lower()
    # skip any nova that does not have these prefixes
    if not any(name.startswith(prefix) for prefix in prefixes): continue
    # check all novae in Transient Name Server data for cross-matches
    for item in altnames:
        # if a SN match is found, change the name to the SN name
        if name.lower().strip() in altnames[item]:
            if 'PTF' in name:
                print(f'Cross-match successful: {names[i]} was changed to {item}.')
            SwiftNames[i] = item
            changed += 1
            break

# reformat SN supernovae so they have the correct(?) casing
print(f'\n{changed} cross-matches found. Formatting...')
for i, name in enumerate(SwiftNames):
    if name[:2].lower() == 'sn' and name[:3].lower() != 'snf':
        SwiftNames[i] = 'SN' + name[2:].lower()

# search for missing redshifts and other data
print('Searching for missing redshifts...')
names_shifts = {}
names_types = {}
names_prefix = {}
refs_types = {}
ras = {}
decs = {}
with open('tns_public_objects.csv', 'r') as tnscsv:
    reader = csv.reader(tnscsv)
    next(reader, None)
    next(reader, None)
    for row in reader:
        # print(f'SN{row[2]} -> {row[5]}?')
#        currname = 'SN' + row[2]
        prefix = row[1]
        currname = row[2]
        if isinstance(row[7], str) and row[7].strip():
            names_types[currname] = row[7].split()[-1]
            
        if isinstance(row[19], str) and row[19].strip():
            refs_types[currname] = row[19]
        names_prefix[currname]=row[1]
        names_shifts[currname] = row[5]
        ras[currname] = row[3]
        decs[currname] = row[4]

for i, name in enumerate(SwiftNames):
    if name[0:2] == 'SN' or name[0:2] == 'AT' or name[0:2] == 'sn' or name[0:2] == 'at':
        checkname=name[2:].lower()
    else:
        checkname=name
    print(checkname)
    if SwiftTypes[i] == '':
        try:
            SwiftTypes[i] = names_types[checkname]
            print(names_types[checkname])
        except:
            do_nothing = 1

    if SwiftTNSprefix[i] == '':
        try:
            SwiftTNSprefix[i] = names_prefix[checkname]
            # print(f"{name}'s redshift was updated to {names_shifts[name]}.")
        except:
            do_nothing = 1
            # print(f'No redshift found for {name}.')


    if SwiftRedshifts[i] == '':
        try:
            SwiftRedshifts[i] = names_shifts[checkname]
            # print(f"{name}'s redshift was updated to {names_shifts[name]}.")
        except:
            do_nothing = 1
            # print(f'No redshift found for {name}.')
        


    try:
        SwiftRa[i] = ras[checkname]
    except:
        do_nothing = 1

    try:
        SwiftDec[i] = decs[checkname]
    except:
        do_nothing = 1
            # print('not found')

'''

    if SwiftRa[i] == '':
        try:
            SwiftRa[i] = ras[checkname]
        except:
            do_nothing = 1

    if SwiftDec[i] == '':
            # print('not found')
        try:
            SwiftDec[i] = decs[checkname]
        except:
            do_nothing = 1
            # print('not found')
'''

Swiftfixedname=[]
ATfixedname=[]
for i,name in enumerate(SwiftNames):
    lowname=name.lower()
    if lowname[0:3] == 'snf':
        fixedname=lowname.replace("snf","SNF")
        print(name)
    if lowname[0:2] == 'sn':
        fixedname=lowname.replace('sn','SN')
    if lowname[0:2] == 'at':
        fixedname=lowname.replace('at','AT')
    if lowname[0:2] == 'iptf':
        fixedname=lowname.replace('iptf','iPTF')
    if lowname[0:2] == 'ptf':
        fixedname=lowname.replace('ptf','PTF')
    if lowname[0:2] == 'ztf':
        fixedname=lowname.replace('ztf','ZTF')
    if lowname[0:2] == 'psn':
        fixedname=lowname.replace('psn','PSN')
    if lowname[0:2] == 'asassn':
        fixedname=lowname.replace('asassn','ASASSN')
    SwiftNames[i]=fixedname
    if SwiftTNSprefix[i]=='SN' and name[0:2] == 'AT':
        ATfixedname=fixedname.replace('AT','SN')
        SwiftNames[i]=ATfixedname

    if SwiftTNSprefix[i] != "":
        print(name)
    if SwiftTypes[i] == 'Iax[02cx-like]':
        SwiftTypes[i]='Iax'
    if SwiftTNSprefix[i] != "":
        print(SwiftNames[i], SwiftTypes[i], SwiftTNSprefix[i])
    

# create df, write to csv
print('Creating dataframe...')
df = pd.DataFrame(list(zip(SwiftNames, SwiftTypes, SwiftRedshifts, SwiftRa, SwiftDec,SwiftTNSprefix)), columns = ['name', 'type', 'redshift', 'right ascension', 'declination','TNSprefix'])


dfmatched=df.loc[df["TNSprefix"]=="SN"]

print(dfmatched)

print('Writing to MatchedSwiftTNS.csv ...')
dfmatched.to_csv('MatchedSwiftTNS.csv', index=False)

print(f'All done! {changed} cross-matches were found.')
