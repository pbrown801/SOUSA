
import pandas as pd
import pickle
from datetime import datetime, timedelta
import sys
import subprocess
import time
import os
import csv 


# This is what a wget command looks like:
# wget -nv -w 2 -nH --cut-dirs=2 -r --no-parent --reject "index.html*" http://www.swift.ac.uk/archive/reproc/00881709000/

def main():
    print("Running", end='\r')
    start_dir=os.getcwd()
    #read in the Swift quicklook website to see which sequences are available
    #and when they were last updated

    dfs = pd.read_html('https://swift.gsfc.nasa.gov/sdc/ql/', header=0,converters={'Sequence': str, 'Vers':str})
    dataframe = dfs[0].sort_values("Processed")
    sequence_list_current = dataframe["Processed"].tolist()

    input_file='currentsupernovalist.csv'
    # This begins as a user-generated list of transients and their corresponding target ids
    SN_list = []
    targetid_list = []
    updatetime_list = []

    with open('currentsupernovalist.csv') as input:
        reader=csv.reader(input,delimiter=',')
        for row in reader:
            print(row)
            SNe, targetids, updatetimes=row[0:3]
            SN_list.append(SNe.replace(" ", ""))
            targetid_list.append(targetids.replace(" ", ""))
            updatetime_list.append(updatetimes)
      

    for i, SNname in enumerate(SN_list):
        print("working on "+SNname)
        if not os.path.exists(SNname):
            os.system('mkdir '+SNname)
        os.chdir(SNname)
        print("in directory ", os.getcwd())
        #for i in range(0,len(SN_list)):
        datetime_found = False
        target_id = targetid_list[i]
        
        if updatetime_list[i] != [] and updatetime_list[i] != ' ': 
            last_datetime = datetime.strptime(updatetime_list[i], '%Y-%m-%d %H:%M:%S')
            datetime_found = True

        for process_time in sequence_list_current:
            row = dataframe.loc[dataframe['Processed'] == process_time]
            
            if str(row['Sequence'].iloc[0])[:8] == target_id and 'only' not in str(row['Object'].iloc[0]): 
                read_datetime = datetime.strptime(process_time, '%Y-%m-%dT%X')

                if datetime_found:
                    delta = (read_datetime - last_datetime) / timedelta(minutes=1)

                    if delta > 0:
                        print("Sequence - {}".format(row['Sequence'].iloc[0]))
                        print("Listed as Object - {}".format(row['Object'].iloc[0]))
                        print("Processed - {}\n".format(row['Processed'].iloc[0]))
                        pass
                        os.system('wget -nv -w 2 -nH --cut-dirs=2 -r -erobots=off --no-parent --reject --directory-prefix='+SNname+' "index.html*" \
                 http://www.swift.ac.uk/archive/reproc/{}/uvot/image/'.format(row['Sequence'].iloc[0]))
                        updatetime_list[i] = str(read_datetime)
                else:
                    print("Sequence - {}".format(row['Sequence'].iloc[0]))
                    print("Listed as Object - {}".format(row['Object'].iloc[0]))
                    print("Processed - {}\n".format(row['Processed'].iloc[0]))

                    pass
                    os.system('wget -nv -w 2 -nH --cut-dirs=2 -r -erobots=off --no-parent --reject --directory-prefix='+SNname+' "index.html*" \
             http://www.swift.ac.uk/archive/reproc/{}/uvot/image/'.format(row['Sequence'].iloc[0]))


                    updatetime_list[i] = str(read_datetime)
        if SNname != SN_list[i+1]:
            os.system('/bin/tcsh /Users/pbrown/Desktop/Dropbox/SN/snscripts/makecommands14.1.txt '+SNname)        
            os.system('source '+SNname+'_allcommands.txt')        
            if os.path.exists(SNname+'_3.reg'):
                os.system('/bin/tcsh /Users/pbrown/Desktop/Dropbox/SN/snscripts/SNgalsub15.1.maghist.txt '+SNname)        

            else:
                print('no region file.  Skipping photometry for '+SNname)

        os.chdir(start_dir)
                    
#   update_file(dat    a)
    print('should print')
    f = open('currentsupernovalist.csv', 'w')
    for i, SNname in enumerate(SN_list):
        print(SN_list[i]+','+targetid_list[i]+','+updatetime_list[i])
        f.write(SN_list[i]+','+targetid_list[i]+','+updatetime_list[i])        
        f.write("\n")        
    f.close()

    return()            

if __name__ == '__main__':
    main()
