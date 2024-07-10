# Initialize lists
Swiftnames = []
Swifttypes = []
Swiftra = []
Swiftdec = []
SwiftPTFnames = []
SwiftPTFtypes = []
SwiftPTFredshifts = []
SwiftPTFra = []
SwiftPTFdec = []

# Read AllSwiftSupernovae.csv
with open('AllSwiftSupernovae.csv', 'r') as allswiftlist:
    for line in allswiftlist:
        line = line.split(',')
        Swiftnames.append(line[0].strip())
        Swifttypes.append(line[1].strip())
        Swiftra.append(line[2].strip())
        Swiftdec.append(line[3].strip())

checked_names = set()

# Read PTF_CClist.txt
with open('PTF_CClist.txt', 'r') as ptflist:
    for line in ptflist:
        line = line.split()
        ptf_name = line[0].strip().lower()
        if ptf_name in checked_names:
            continue
        for nova in Swiftnames:
            if nova.lower() == ptf_name:
                SwiftPTFnames.append(line[0])
                SwiftPTFtypes.append(line[1])
                SwiftPTFredshifts.append(line[2])
                SwiftPTFra.append(line[5] + ' ' + line[6] + ' ' + line[7])
                SwiftPTFdec.append(line[8] + ' ' + line[9] + ' ' + line[10])
                print(f'Added {line[0]} with type {line[1]} and redshift {line[2]}.')
                checked_names.add(ptf_name)

# Read iPTFlist.txt
with open('iPTFlist.txt', 'r') as iptflist:
    for line in iptflist:
        line = line.split()
        curr = 'iPTF' + line[0].strip()
        curr_lower = curr.lower()
        if curr_lower in checked_names:
            continue
        print('in iPTFlist', curr)
        for nova in Swiftnames:
            if nova.strip().lower() == curr_lower:
                SwiftPTFnames.append(curr)
                SwiftPTFtypes.append('Ia')
                SwiftPTFredshifts.append('')
                SwiftPTFra.append('')
                SwiftPTFdec.append('')
                print(curr, "is also in Swift list")
                checked_names.add(curr_lower)