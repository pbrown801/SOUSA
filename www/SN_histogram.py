#  originally written by Kelli Templeton as part of the Aggienova research team 2019

import matplotlib.pyplot as plt
import numpy as np

#with open('SwiftSNlist.txt') as f:
#    swift_list= f.readlines()
with open('NewSwiftSNweblist.csv') as f:
    swift_list=[line.split(',', 1)[0] for line in f]

with open('nonSwiftSNlist.txt') as g:
    non_swift_list= g.readlines()

swift_list=[x.strip() for x in swift_list]
non_swift_list=[x.strip() for x in non_swift_list]

y = str()

for x in swift_list:
    if x==y:
        swift_list.remove(x)

for x in swift_list:
    if 'MASTER' in x:
        swift_list.remove(x)

for x in swift_list:
    if "inPGC" in x:
        swift_list.remove(x)


swift_year_dict = {}
swift_graph=[]

for year in ['05','06','07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2020', '21']:
    swift_year_dict[year] = sum(1 for line in swift_list if year in line)
    for x in range(swift_year_dict[year]):
        if len(year) < 3:
            swift_graph.append('20' + year)
        else:
            swift_graph.append(year)

hst_list=[]
oao_list=[]
iue_list=[]
xmm_list=[]
galex_list=[]
astrosat_list=[]

hst_graph=[]
oao_graph=[]
iue_graph=[]
xmm_graph=[]
galex_graph=[]
astrosat_graph=[]

non_swift_year_list=['1972', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005','2006','2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019','2020','2021']


for x in non_swift_list:
    if 'HST' in x:
        hst_list.append(x)

for x in non_swift_list:
    if 'OAO' in x:
        oao_list.append(x)

for x in non_swift_list:
    if 'IUE' in x:
        iue_list.append(x)

for x in non_swift_list:
    if 'XMM' in x:
        xmm_list.append(x)

for x in non_swift_list:
    if 'GALEX' in x:
        galex_list.append(x)


for x in non_swift_list:
    if 'Astrosat' in x:
        astrosat_list.append(x)


hst_year_dict = {}

for year in non_swift_year_list:
    hst_year_dict[year] = sum(1 for line in hst_list if year in line)
    for x in range(hst_year_dict[year]):
        if len(year) < 3:
            hst_graph.append('20' + year)
        else:
            hst_graph.append(year)


oao_year_dict = {}

for year in non_swift_year_list:
    oao_year_dict[year] = sum(1 for line in oao_list if year in line)
    for x in range(oao_year_dict[year]):
        if len(year) < 3:
            oao_graph.append('20' + year)
        else:
            oao_graph.append(year)

iue_year_dict = {}

for year in non_swift_year_list:
    iue_year_dict[year] = sum(1 for line in iue_list if year in line)
    for x in range(iue_year_dict[year]):
        if len(year) < 3:
            iue_graph.append('20' + year)
        else:
            iue_graph.append(year)

xmm_year_dict = {}

for year in non_swift_year_list:
    xmm_year_dict[year] = sum(1 for line in xmm_list if year in line)
    for x in range(xmm_year_dict[year]):
        if len(year) < 3:
            xmm_graph.append('20' + year)
        else:
            xmm_graph.append(year)

galex_year_dict = {}

for year in non_swift_year_list:
    galex_year_dict[year] = sum(1 for line in galex_list if year in line)
    for x in range(galex_year_dict[year]):
        if len(year) < 3:
            galex_graph.append('20' + year)
        else:
            galex_graph.append(year)


swift_graph = list(map(int, swift_graph))
hst_graph   = list(map(int, hst_graph))
oao_graph   = list(map(int, oao_graph))
iue_graph   = list(map(int, iue_graph))
xmm_graph   = list(map(int, xmm_graph))
galex_graph = list(map(int, galex_graph))

b = np.arange(1971,2026, 1)

bg_color = 'black'
fg_color = 'white'

fig=plt.figure(facecolor=bg_color, edgecolor=fg_color)
axes = fig.add_subplot(111)
axes.patch.set_facecolor(bg_color)
axes.xaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
axes.yaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
for spine in axes.spines.values():
    spine.set_color(fg_color)

plt.rcParams.update({'font.size': 16})
font={'fontname': 'Arial', 'weight':'bold', 'size':'22'}
axis_font={'fontname': 'Arial', 'size':'15'}
plt.hist(swift_graph,b, histtype='bar', rwidth=0.8, axes=axes, label="SWIFT")
plt.hist(hst_graph,  b, histtype='bar', rwidth=0.8, axes=axes, label="HST")
plt.hist(galex_graph,b, histtype='bar', rwidth=0.8, axes=axes, label="GALEX")
plt.hist(oao_graph,  b, histtype='bar', rwidth=0.8, axes=axes, label="OAO-2")
plt.hist(iue_graph,  b, histtype='bar', rwidth=0.8, axes=axes, label="IUE")
plt.hist(xmm_graph,  b, histtype='bar', rwidth=0.8, axes=axes, label="XMM-OM")
plt.legend(loc='upper left')
plt.xlabel("Year", color=fg_color, **font)
plt.xlim(left=1970)
plt.xlim(right=2025)
plt.ylim(top=140)
plt.xticks(np.arange(1970,2025,3), **axis_font)
plt.yticks(**axis_font)
plt.ylabel("Supernovae Observed in the Ultraviolet", color=fg_color, **font)

print(swift_graph)

plt.show() 