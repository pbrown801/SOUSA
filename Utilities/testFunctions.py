from utilities import *

def setup():
    threader = threading.Thread(target=animate)
    threader.start()
    gals = read_gals('../Inputs/cepheidGals.csv')
    gals, start_coord = get_coords(gals)
    for i in range(0,len(gals)):
        ra, dec = coord_breakup(start_coord[i])
        a_v = tableFill(20,ra,dec,'w',gals[i])
        print(a_v)
    done = True
if __name__ == '__main__':
    setup() #run setup to grab gals and coordinates


