
#! C:\Users\edudi\OneDrive\Documents\AggieNovaCode\pythonProject1\myenv\Scripts\python.exe


import csv
import matplotlib.pyplot as plt
import numpy as np


#eduardo Diaz

# ____________________________________________________________________________________________________________________________________________________________________________
# |!Instruction for the changeing and editing of the of the pie chart!
# |
# |For those who want to edit and change the piechart look for the  #--------------------------------EDIT THIS, and read the instruction below how to edit these areas
# |
# |Catagories_<Type> is the number of supernovea sub catagories you want to see on the sub plot for each type, One more will be added for eveything outside the sub catagories being searched
# |
# |If you just want to change the what data the sub plot is going look for, just change the the string in the if statment at #--------------------------------EDIT SEARCH Items,
# |Make sure it is in the Catagories_<Type> bounds you have set.
# |
# |Next is adding a new classified for the sub plot.You need to be editing the if statment that look like: if((Catagories_IA>=1)&(str(list_of_rows[index][3])=="Iax")):
# |To add a new catagories , copy the last elif() statement , incrament all of the numbers of the if statment by 1 (execpt the plus +1), and... 
# |...change the thing being searched in csv (str(list_of_rows[index][3])=="<thing being searched in csv>"")
# |
# |Editing the lables should be easy, just edit the strings in lable list. The lables follow the order of the data array, meaning its goes in order of IA/(subplots),II/(subplots),Ibc/(subplots),other/(subplots)
# |WARNING!!!!!, make sure for subplot lables that the number of lables is equal to (largest amount of catagories+1)*4, matplotlib will break if you dont
# |For example:
# |    Catagories_IA =0
# |    Catagories_II =2
# |    Catagories_Ibc =3
# |    Catagories_Other =5
# |    you would need (5+1)*4=24 lables
# |unwanted lables can be put as "" and will not show up on the pie chart.
# |
# |Lastly there is colors, Add colors from the matplotlib website to the list for each designated type of supernova.Purple(or "Plum") means the code has run out of that type of color and we need to add more
# |Look at described area for more context
# |
# |Pieplot Has many tools so you can fanagle with it how you please.
# |That is all good luck
#____________________________________________________________________________________________________________________________________________________________________________

#can edit what csv is opened here
with open('SortedTrimmedAllSwiftSNlist.csv','r') as csv_file:
    print("index:")
    reader =csv.reader(csv_file)
    list_of_rows = list(reader)  # Pass reader object to list() to get a list of lists

    

    Num_IA=0
    Num_II=0
    Num_Ibc=0
    Num_Other=0
    Num_total=len(list_of_rows)-3
    Num_total_dubug=0



    #--------------------------------EDIT THIS
    Catagories_IA =1
    Catagories_II =2
    Catagories_Ibc =3
    Catagories_Other =4
    #--------------------------------
    List_Catagories=[Catagories_IA,Catagories_II,Catagories_Ibc,Catagories_Other]

    
    Cat_Num_IA = []
    Cat_Num_II = []
    Cat_Num_Ibc = []
    Cat_Num_other = []

    for index in range(Catagories_IA):
        Cat_Num_IA.append(0)
    for index in range(Catagories_II):
        Cat_Num_II.append(0)
    for index in range(Catagories_Ibc):
        Cat_Num_Ibc.append(0)
    for index in range(Catagories_Other):
        Cat_Num_other.append(0)
    #Cat_Num_other = np.arange(Catagories_Other)


    print(Catagories_IA>=4)


    uncatagorized_IA=0
    uncatagorized_II=0
    uncatagorized_Ibc=0
    uncatagorized_other=0

    for index in range(3,len(list_of_rows)):
        list_of_rows[index][3]=list_of_rows[index][3].strip() # get rid of spaces in the front or the end of the type


        if (str(list_of_rows[index][3]).strip() == "Iax[02cx-like]" or str(list_of_rows[index][3]) == "Ia-02cx"):  # case were Iax[02cx-like] type is changed to Iax
            list_of_rows[index][3] = 'Iax'

        if (str(list_of_rows[index][3]).strip() == "Ia-91T" ):  # case were  
            list_of_rows[index][3] = 'Ia-91T-like'

        if (str(list_of_rows[index][3]).strip() == "Ibc" ):  # case were  
            list_of_rows[index][3] = 'Ib/c'

        if (str(list_of_rows[index][3]).strip() == "Ibc" ):  # case were  
            list_of_rows[index][3] = 'Ib/c'
        

        # all of theses check and print out the row , the name ,the new type, and the Group it got put in to

        #Ia
        if(str(list_of_rows[index][3])=="Iax" or str(list_of_rows[index][3])=="Ia" or str(list_of_rows[index][3])=="Ia-91T-like" or str(list_of_rows[index])=="Ia-91bg" or str(list_of_rows[index][3])=="Ia-pec" or str(list_of_rows[index][3])=="Ia-CSM"  or str(list_of_rows[index][3])=="Ia-SC" or str(list_of_rows[index][3])=="Ia-Ca-rich"): # check for all supernova type one a
            #print("row:"+str(index)+" Name:"+list_of_rows[index][0]+" Type:"+list_of_rows[index][3]+" Group: Ia")
            Num_IA=Num_IA+1
            if((Catagories_IA>=1)&(str(list_of_rows[index][3])=="Iax")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_IA[0]=Cat_Num_IA[0]+1
            elif((Catagories_IA>=2)&(str(list_of_rows[index][3])=="Ia-91bg")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_IA[1]=Cat_Num_IA[1]+1
            elif((Catagories_IA>=3)&(str(list_of_rows[index][3])=="Ia-SC")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_IA[2]=Cat_Num_IA[2]+1
            elif((Catagories_IA>=4)&(str(list_of_rows[index][3])=="Ia")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_IA[3]=Cat_Num_IA[3]+1
            else:
                uncatagorized_IA=uncatagorized_IA+1
            #--------------------------------EXPAND IF STATMENT IF NEEDED

            

        #II
        elif(str(list_of_rows[index][3].strip())=="II" or str(list_of_rows[index][3].strip())=="IIn" or str(list_of_rows[index][3].strip())=="IIP" or str(list_of_rows[index][3].strip())=="IIb" or str(list_of_rows[index][3].strip())=="SLSN-II"  or str(list_of_rows[index][3].strip())=="SN II-pec" or str(list_of_rows[index][3].strip())=="SN IIn-pec" or str(list_of_rows[index][3].strip())=="IIL"): # check for all supernova type one a
            #print("row:"+str(index)+" Name:"+list_of_rows[index][0]+" Type:"+list_of_rows[index][3]+" Group: II")
            Num_II=Num_II+1
            if((Catagories_II>=1)&(str(list_of_rows[index][3]).strip()=="II")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_II[0]=Cat_Num_II[0]+1
            elif((Catagories_II>=2)&(str(list_of_rows[index][3])=="SLSN-II")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_II[1]=Cat_Num_II[1]+1
            elif((Catagories_II>=3)&(str(list_of_rows[index][3]).strip()=="SN IIn")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_II[2]=Cat_Num_II[2]+1
            elif((Catagories_II>=4)&(str(list_of_rows[index][3])=="IIL")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_II[3]=Cat_Num_II[3]+1
            else:
                uncatagorized_II=uncatagorized_II+1
            #--------------------------------EXPAND IF STATMENT IF NEEDED




        #Ib/c
        elif(str(list_of_rows[index][3].strip())=="Ic-bl" or str(list_of_rows[index][3].strip())=="Ic" or str(list_of_rows[index][3].strip())=="Ib" or str(list_of_rows[index][3].strip())=="SLSN-I" or str(list_of_rows[index][3].strip())=="Ic-BL" or str(list_of_rows[index][3].strip())=="Ib/c" or str(list_of_rows[index][3].strip())=="Ibn"  or str(list_of_rows[index][3].strip())=="Ib-pec"  or str(list_of_rows[index][3].strip())=="Ib-Ca-rich" or str(list_of_rows[index][3].strip())=="Icn" or str(list_of_rows[index][3].strip())=="Ic-pec" or str(list_of_rows[index][3].strip())=="Ibn/Icn" or str(list_of_rows[index][3].strip())=="Ic-Ca-rich"): # check for all supernova type one a
            #print("row:"+str(index)+" Name:"+list_of_rows[index][0]+" Type:"+list_of_rows[index][3]+" Group: Ib/c")
            Num_Ibc=Num_Ibc+1
            if((Catagories_Ibc>=1)&(str(list_of_rows[index][3])=="Ic-bl")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_Ibc[0]=Cat_Num_Ibc[0]+1
            elif((Catagories_Ibc>=2)&(str(list_of_rows[index][3])=="Ic")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_Ibc[1]=Cat_Num_Ibc[1]+1
            elif((Catagories_Ibc>=3)&(str(list_of_rows[index][3])=="Ib")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_Ibc[2]=Cat_Num_Ibc[2]+1
            elif((Catagories_Ibc>=4)&(str(list_of_rows[index][3])=="Ic-Ca-rich")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_Ibc[3]=Cat_Num_Ibc[3]+1                    
            else:
                uncatagorized_Ibc=uncatagorized_Ibc+1         
            #--------------------------------EXPAND IF STATMENT IF NEEDED
        #nadaSN
        elif(str(list_of_rows[index][3].lower())=="ILRT"or str(list_of_rows[index][3].lower())=="cv" or str(list_of_rows[index][3].lower())=="tde" or str(list_of_rows[index][3].lower())=="agn"or str(list_of_rows[index][3])=="LBV"): # check for all supernova type one a
            #print("row:"+str(index)+" Name:"+list_of_rows[index][0]+" Type:"+list_of_rows[index][3]+" Group: nada SN")
            if((Catagories_Other>=1)&(str(list_of_rows[index][3])=="ILRT")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_other[0]=Cat_Num_other[0]+1
            elif((Catagories_Other>=2)&(str(list_of_rows[index][3])=="cv")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_other[1]=Cat_Num_other[1]+1
            elif((Catagories_Other>=3)&(str(list_of_rows[index][3])=="tde")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_other[2]=Cat_Num_other[2]+1
            elif((Catagories_Other>=4)&(str(list_of_rows[index][3])=="agn")):    #--------------------------------EDIT SEARCH Items
                Cat_Num_other[3]=Cat_Num_other[3]+1      
            else:
                uncatagorized_other=uncatagorized_other+1
            Num_Other=Num_Other+1
      
        else:
            print("row:"+str(index)+" Name:"+list_of_rows[index][0]+" Type:"+list_of_rows[index][3]+" No Idea")

        



    #if I delete this, it breaks, so im just not gonna touch this failed attempt
    if(1==2):
        ax = plt.subplots(figsize=(10, 7),subplot_kw=dict(polar=True))


        sting_ting =str(Num_IA) +" "+str(Num_II)+" "+str(Num_Ibc)+" "+str(Num_Other)
        print(sting_ting)
        y = np.array([Num_IA, Num_II, Num_Ibc, Num_Other])
        mylabels = ["Ia", "II", "Ibc", "Others"]
        plt.pie(y,labels = mylabels)
            
        plt.show()

    else:

        size = 1.2
        mylabels =["Ia", "II", "Ibc", "Others"]
        sublabels =["1", "2", "3", "4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"] #add lables here
        sublabels =['Iax','Ia-91bg','Ia-SC','Ia','II','SLSN-II','SN IIn','IIL','Ic-bl','Ic','Ib','Ic-Ca-Rich','ILRT','cv','tde','agn']

        #adds unregistered supernovie to pie chart

        Cat_Num_IA.append(uncatagorized_IA)
        Cat_Num_II.append(uncatagorized_II)
        Cat_Num_Ibc.append(uncatagorized_Ibc)
        Cat_Num_other.append(uncatagorized_other)

        for x in range(max(Catagories_IA,Catagories_II,Catagories_Ibc,Catagories_Other)):
            if(x+1>Catagories_IA):
                Cat_Num_IA.append(0)
            if(x+1>Catagories_II):
                Cat_Num_II.append(0)
            if(x+1>Catagories_Ibc):
                Cat_Num_Ibc.append(0)
            if(x+1>Catagories_Other):
                Cat_Num_other.append(0) 
        
        print("final Catagories")
        print(Cat_Num_IA)
        print(Cat_Num_II)
        print(Cat_Num_Ibc)
        print(Cat_Num_other)
        print([Cat_Num_IA, Cat_Num_II,Cat_Num_Ibc, Cat_Num_other])

        data = np.array([Cat_Num_IA, Cat_Num_II,Cat_Num_Ibc, Cat_Num_other])
 
        norm = data / np.sum(data)*2 * np.pi
        
        # obtaining ordinates of bar edges
        left = np.cumsum(np.append(0,norm.flatten()[:-1])).reshape(data.shape)
        
        # Color Stuff---------------------------------------------------------------------EDIT THIS
        # Add colors if you either are geting error (there is more catagories than colors), Or you are seeing PURPLE in the pie chart
        # for colors see https://matplotlib.org/2.0.2/examples/color/named_colors.html
        outer_colors = ("salmon","yellowgreen","teal","silver")

        #inner color selection
        IA_redColorOptions=["brown","firebrick","red","maroon","coral","mistyrose","tomato","lightcoral","darkred","plum","plum","plum"]#lastIn list are purple for error boundry testing
        II_greenColorOptions= ["lime","seagreen","mediumseagreen","g","lightgreen","palegreen","seagreen","plum","plum","plum"]
        Ibc_blueColorOptions= ["blue","c","navy","aqua","mediumslateblue","skyblue","plum","plum","plum"]
        other_greyColorOptions=["dimgrey","slategray","gray","darkgray","grey","lightslategrey","plum","plum","plum"]

        # Color Stuff----------------------------------------------------------------------------------------------------$


        innerColor_created=[]
        for x in range(max(Catagories_IA,Catagories_II,Catagories_Ibc,Catagories_Other)+1):#plus one since there is one more catagory of supernova, the uncatagorized ones
            innerColor_created.append(IA_redColorOptions[x])
        for x in range(max(Catagories_IA,Catagories_II,Catagories_Ibc,Catagories_Other)+1):
            innerColor_created.append(II_greenColorOptions[x])
        for x in range(max(Catagories_IA,Catagories_II,Catagories_Ibc,Catagories_Other)+1):
            innerColor_created.append(Ibc_blueColorOptions[x])
        for x in range(max(Catagories_IA,Catagories_II,Catagories_Ibc,Catagories_Other)+1):
            innerColor_created.append(other_greyColorOptions[x])

        print(innerColor_created)

        inner_colors =  (innerColor_created)

        # Creating plot
        fig, ax = plt.subplots(figsize=(10, 7))
        #fig, ax = plt.subplots(figsize=(10, 7),subplot_kw=dict(polar=True))

        #outer Chart
        #ax.bar(x=left[:, 0],#width=norm.sum(axis=1),#bottom=1-size,#height=size,#color=outer_colors,#edgecolor='w',#linewidth=1,#labels = mylabels,#align="edge")
        #innerChart
        #ax.bar(x=left.flatten(),#width=norm.flatten(),#bottom=1-2 * size,#height=size,#color=inner_colors,#edgecolor='w',#linewidth=1,#align="edge")

        plt.rcParams['font.size'] = size*17
        ax.pie(data.sum(axis=1), radius=size, colors=outer_colors,labels=mylabels,textprops=dict(color="k") )

        plt.rcParams['font.size'] = size*7
        ax.pie(data.flatten(), radius=size/1.66,labels=sublabels, colors=inner_colors)

        #plum color means error
        
        
        #ax.set(title="Super Nova Test chart")
        ax.set_axis_off()
        
        # show plot
        plt.show()

    csv_file.close()


