# Imports:
from opentrons import instruments, labware, robot


# Parameters: 
serial_dict = {'Stock' : {'C' : 1000, 
                          'L' : 'A1'},
               'Serial' : {'C' : [500, 250, 125, 62.5],
                           'L' : ['B1', 'C1', 'D1', 'E1'],
                           'V' : 100},
               'Solvent' : {'L' : 'A2'},
               'First_tip' : {'L' : 'A1'}}


def serial(stock_c, serial_c_list, final_v):
    '''Calculate the volumes needed for a serial dilution'''
    N = len(serial_c_list)
    V1 = serial_c_list[0] * final_v / stock_c
    serial_vols = [V1]
    for i in range(1, N):
        V = serial_c_list[i] * final_v / serial_vols[-1]
        serial_vols.append(V)
    return serial_vols


def serialbot(serial_vols):
    PIPETTE.start_at_tip(TIP_RACK.well(serial_dict['First_tip']['L']))
    # Pipette solvent:
    PIPETTE.pick_up_tip()
    PIPETTE.transfer([serial_dict['Serial']['V'] - vol for vol in serial_vols],
                    PLATE.wells(serial_dict['Solvent']['L']),
                    PLATE.wells(serial_dict['Serial']['L']),
                    new_tip='never',
                    blow_out=True)
    PIPETTE.drop_tip()
    # Serial dilution:
    PIPETTE.pick_up_tip()
    PIPETTE.transfer(serial_vols,
                    PLATE.wells([serial_dict['Stock']['L']] + serial_dict['Serial']['L'][:-1]),
                    PLATE.wells(serial_dict['Serial']['L']),
                    air_gap=20,
                    new_tip='never',
                    blow_out=True,
                    mix_after=(5, 0.4 * serial_dict['Serial']['V']))
    PIPETTE.drop_tip()


if __name__ == "__main__":
    # Metainformation:
    for key, subdict in serial_dict.items():
        print('\nItem:', key)
        for key in subdict:
            print(key + ':', subdict[key])
    # Labware setup:
    PLATE = labware.load('96-flat', '1')
    TIP_RACK = labware.load('opentrons_96_tiprack_300ul', '3')
    PIPETTE = instruments.P300_Single(mount='right', tip_racks=[TIP_RACK])
    # Main:
    serial_vols = serial(serial_dict['Stock']['C'], serial_dict['Serial']['C'], serial_dict['Serial']['V'])
    serialbot(serial_vols)
    # Commands:
    print('\n')
    for c in robot.commands():
        print(c)