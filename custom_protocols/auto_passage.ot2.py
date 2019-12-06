# Imports:
from opentrons import instruments, labware, robot


metadata = {
    'protocolName': 'auto_passage',
    'author': 'Jake Bowden - Imperial Student Biofoundry',
    'source': 'github.com/JBwdn/M5-Team-4'
    }


# Parameters:
sample_ODs = []
sample_wells = []
sample_wells = []
LB_well = 'A1'


def dilution_calc():
    '''Calculate the dilution required for each sample from OD.'''
    pass


# Labware:


# Main:



if __name__ == "__main__":
    for c in robot.commands():
        print(c)