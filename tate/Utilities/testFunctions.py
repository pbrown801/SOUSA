from utilities import *

def setup():
    gals = read_gals('../Inputs/cepheidGals.csv')
    gals, start_coord = get_coords(gals)
if __name__ == '__main__':
    setup() #run setup to grab gals and coordinates


