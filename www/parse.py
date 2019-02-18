import numpy as np


snname, hostg, snname2,sntype = np.genfromtxt('fullSNlist.csv', delimiter=',',dtype = str, usecols=(0,1,3,5), unpack=True)


alltypes = []
for item in sntype:
	if item not in alltypes:
		if item:
			if not item.endswith('?'):
				if not item.endswith(' '):
					alltypes.append(item)

def list_by_type():
	iasn = []
	ibcsn = []
    	iisn = []
    	for item in range(len(sntype)):

		if sntype[item].startswith("Ia"):
			iasn.append(snname[item])
		
		if sntype[item].startswith('Ib') or sntype[item].startswith('Ic'):
			ibcsn.append(snname[item])

		if sntype[item].startswith('II'):
			iisn.append(snname[item])

	return iasn,ibcsn,iisn




ia, ibc,ii = list_by_type()


'''
print 'Ia SN: ' + ', '.join(str(e) for e in ia)
print('\n')
print 'Ib SN: ' + ', '.join(str(e) for e in ib)
print('\n')
print 'Ic SN: ' + ', '.join(str(e) for e in ic)
'''	

with open('typeia.txt','w') as typeia:
	for item in ia:
		typeia.write('%s\n' % item)

with open('typeibc.txt','w') as typeibc:
	for item in ibc:
		typeibc.write('%s\n' % item)

with open('typeii.txt','w') as typeii:
	for item in ii:
		typeii.write('%s\n' % item)


