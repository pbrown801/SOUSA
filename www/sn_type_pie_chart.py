import matplotlib.pyplot as plt

with open('SNType.txt') as f:
    sn_list= f.readlines()

sn_type_dict = {}

for type in ['Ia','Ib','Ic', 'II']:
    sn_type_dict[type] = sum(1 for line in sn_list if type in line)

print(sn_type_dict)

colors=['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
#plt.pie(list(sn_type_dict.values()), labels=list(sn_type_dict.keys()), colors=colors, autopct='%1.1f%%', startangle=140)
types, texts, values=plt.pie(list(sn_type_dict.values()), colors=colors, autopct='%1.1f%%', startangle=140)
plt.legend(types, list(sn_type_dict.keys()), loc="best")

plt.show()