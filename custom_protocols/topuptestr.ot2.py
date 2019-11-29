# Imports:
from opentrons import instruments, labware, robot

# Parameters:
mode = 'P10'
mount = 'right'
N = 26
end_gap = 2
location = '3'


all_wells = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'A10', 'B10', 'C10', 'D10', 'E10', 'F10','A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'A12', 'B12', 'C12', 'D12', 'E12', 'F12']


if mode == 'P300':
    TIP_RACK = labware.load('opentrons_96_tiprack_300ul', location)
    PIPETTE = instruments.P300_Single(mount=mount, tip_racks=[TIP_RACK])
elif mode == 'P10':
    TIP_RACK = labware.load('opentrons_96_tiprack_10ul', location)
    PIPETTE = instruments.P10_Single(mount=mount, tip_racks=[TIP_RACK])


for i in range(N):
    PIPETTE.pick_up_tip(TIP_RACK.wells(all_wells[- (i + end_gap + 1)]))
    PIPETTE.drop_tip(TIP_RACK.wells(all_wells[i]))


for c in robot.commands():
    print(c)
