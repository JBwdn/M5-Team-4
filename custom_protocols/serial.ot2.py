# Imports:
from opentrons import instruments, labware, robot

# Parameters:
stock_conc_uM = 200
stock_posn = 'A1'
dilutant_posn = 'A2'
serial_concs_uM = [150, 50, 10, 0.5, 0.1]
serial_posn = ['B1', 'C1', 'D1', 'E1', 'F1']
final_vol_uL = 50


def setup():
    '''Initialize labware and pipettes'''
    global PLATE, TRASH, TIP_RACK, PIPETTE
    PLATE = labware.load('96-flat', '2')
    TRASH = labware.load('trash-box', '11')
    TIP_RACK = labware.load('opentrons_96_tiprack_300ul', '1')
    PIPETTE = instruments.P10_Single(mount='left',
                                           tip_racks=[TIP_RACK],
                                           trash_container=TRASH)


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
    # PIPETTE.mix(5 , final_vol_uL, PLATE.wells(serial_posn[0]))
    PIPETTE.drop_tip()

    # Dilution loop:
    for i in range(1, len(serial_vols)):
        PIPETTE.pick_up_tip()
        PIPETTE.aspirate(serial_vols[i], PLATE.wells(serial_posn[i-1]))
        PIPETTE.dispense(serial_vols[i], PLATE.wells(serial_posn[i]))
        # PIPETTE.mix(5 , final_vol_uL, PLATE.wells())
        PIPETTE.drop_tip()


if __name__ == "__main__":
    setup()
    serial_vols, dilutant_vols = serial(stock_conc_uM,
                                        serial_concs_uM,
                                        final_vol_uL)
    serialbot(serial_vols, dilutant_vols)
    print(serial(stock_conc_uM, serial_concs_uM, final_vol_uL))
    for c in robot.commands():
        print(c)
