# Imports:
from opentrons import instruments, labware, robot


# Parameters:
stock_conc_uM = 100
stock_posn = 'A1'
dilutant_posn = 'A2'
serial_concs_uM = [50, 25, 12.5]
serial_posn = ['B1', 'C1', 'D1']
final_vol_uL = 100


def serial(stock_c, serial_c_list, serial_v):
    '''Calculate the volumes needed for a serial dilution'''
    N = len(serial_c_list)
    dilutant_vols = []
    serial_vols = []

    v1 = serial_c_list[0] * serial_v / stock_c
    serial_vols.append(v1)
    dilutant_vols.append(serial_v - v1)
    for i in range(1, N):
        V = serial_c_list[i] * serial_v / serial_vols[-1]
        serial_vols.append(V)
        dilutant_vols.append(serial_v - V)
    return serial_vols, dilutant_vols


def serialbot(serial_vols, dilutant_vols):
    # Pipette dilutant:
    PIPETTE.pick_up_tip()
    for i in range(len(serial_vols)):
        PIPETTE.aspirate(dilutant_vols[i], PLATE.wells(dilutant_posn))
        PIPETTE.dispense(dilutant_vols[i], PLATE.wells(serial_posn[i]))
    PIPETTE.drop_tip()

    # First dilution:
    PIPETTE.pick_up_tip()
    PIPETTE.aspirate(serial_vols[0], PLATE.wells(stock_posn))
    PIPETTE.dispense(serial_vols[0], PLATE.wells(serial_posn[0]))
    # PIPETTE.mix(5, final_vol_uL*0.8, PLATE.wells(serial_posn[0]))

    # Dilution loop:
    for i in range(1, len(serial_vols)):
        PIPETTE.aspirate(serial_vols[i], PLATE.wells(serial_posn[i-1]))
        PIPETTE.dispense(serial_vols[i], PLATE.wells(serial_posn[i]))
        # PIPETTE.mix(5, final_vol_uL*0.4, PLATE.wells(serial_posn[i]))
    PIPETTE.drop_tip()

# Labware setup:
PLATE = labware.load('96-flat', '1')
TIP_RACK = labware.load('opentrons_96_tiprack_300ul', '3')
PIPETTE = instruments.P300_Single(mount='right', tip_racks=[TIP_RACK])

# Main program:
serial_vols, dilutant_vols = serial(stock_conc_uM, serial_concs_uM, final_vol_uL)
print(serial_vols, dilutant_vols)
serialbot(serial_vols, dilutant_vols)
for c in robot.commands():
    print(c)
