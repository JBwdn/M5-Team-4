# Imports:
from opentrons import instruments, labware, robot


# Parameters:
mode = 'P10'
mount = 'right'
N = 41
end_gap = 0
location = '3'


all_wells = []
for i in range(1,13):
    section = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    all_wells += [section[j] + str(i) for j in range(len(section))]


if mode == 'P300':
    TIP_RACK = labware.load('opentrons_96_tiprack_300ul', location)
    PIPETTE = instruments.P300_Single(mount=mount, tip_racks=[TIP_RACK])
elif mode == 'P10':
    TIP_RACK = labware.load('opentrons_96_tiprack_10ul', location)
    PIPETTE = instruments.P10_Single(mount=mount, tip_racks=[TIP_RACK])


for i in range(N):
    PIPETTE.pick_up_tip(TIP_RACK.wells(all_wells[- (i + end_gap + 1)]))
    PIPETTE.drop_tip(TIP_RACK.wells(all_wells[i]))