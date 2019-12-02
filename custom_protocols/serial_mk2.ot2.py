# Imports:
from opentrons import instruments, labware, robot


# Parameters: 
serial_dict = {'Stock' : {'C' : 700, 
                          'L' : 'A1'},
               'Serial' : {'C' : [500, 300, 150, 75, 25, 5, 0.5],
                           'L' : ['B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1'],
                           'V' : 100},
               'Solvent' : {'L' : 'A2'},
               'First_tip' : {'L' : 'A1'},
               'Pipette' : {'Mode' : 'P300',
                            'Mount' : 'left'}}


def serial_calculator(stock_c, serial_c_list, final_v):
    '''Calculate the volumes needed for a serial dilution'''
    V1 = serial_c_list[0] * final_v / stock_c
    serial_vols = [V1]
    for i in range(1, len(serial_c_list)):
        V = serial_c_list[i] * final_v / serial_c_list[i-1]
        serial_vols.append(V)
    return serial_vols


def serial_bot(serial_dict):
    # Constants:
    tip_location = serial_dict['First_tip']['L']
    solvent_location = serial_dict['Solvent']['L']
    serial_locations = serial_dict['Serial']['L']
    stock_location = serial_dict['Stock']['L']
    serial_volumes = serial_dict['Serial']['Volumes']
    VT = serial_dict['Serial']['V']

    # Pipette solvent:
    pipette.start_at_tip(tip_rack.well(tip_location))
    pipette.pick_up_tip()
    pipette.transfer(
            [VT - vol for vol in serial_volumes],
            plate.wells(solvent_location),
            plate.wells(serial_locations),
            new_tip='never',
            blow_out=True)
    pipette.drop_tip()
    # Serial dilution:
    pipette.pick_up_tip()
    pipette.transfer(
            serial_volumes,
            plate.wells([stock_location] + serial_locations[:-1]),
            plate.wells(serial_locations),
            air_gap=20,
            new_tip='never',
            blow_out=True,
            mix_after=(5, 0.4*VT))
    pipette.drop_tip()


if __name__ == "__main__":
    # Metainformation:
    for key, subdict in serial_dict.items():
        print('\nItem:', key)
        for key in subdict:
            print(key + ':', subdict[key])

    # Labware setup:
    plate = labware.load('96-flat', '1')
    if serial_dict['Pipette']['Mode'] == 'P300':
        tip_rack = labware.load('opentrons_96_tiprack_300ul', '3')
        pipette = instruments.P300_Single(mount=serial_dict['Pipette']['Mount'], tip_racks=[tip_rack])
    elif serial_dict['Pipette']['Mode'] == 'P10':
        tip_rack = labware.load('opentrons_96_tiprack_10ul', '3')
        pipette = instruments.P10_Single(mount=serial_dict['Pipette']['Mount'], tip_racks=[tip_rack])

    # Main:
    stock_conc = serial_dict['Stock']['C']
    serial_concs = serial_dict['Serial']['C']
    serial_vol = serial_dict['Serial']['V']

    serial_dict['Serial']['Volumes'] = serial_calculator(stock_conc, serial_concs, serial_vol)
    serial_bot(serial_dict)

    # Commands:
    print('\n')
    for c in robot.commands():
        print(c)