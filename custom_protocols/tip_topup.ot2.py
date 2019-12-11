# Imports:
from opentrons import instruments, labware, robot


# Parameters:
mode = 'P10'
mount = 'right'
N = 41
end_gap = 0
location = '3'


if mode == 'P300':
    TIP_RACK = labware.load('opentrons_96_tiprack_300ul', location)
    PIPETTE = instruments.P300_Single(mount=mount, tip_racks=[TIP_RACK])
elif mode == 'P10':
    TIP_RACK = labware.load('opentrons_96_tiprack_10ul', location)
    PIPETTE = instruments.P10_Single(mount=mount, tip_racks=[TIP_RACK])


def tip_rerack(tiprack_obj, pipette_obj, N_tips, end_gap):
    for i in range(N_tips):
        pipette_obj.pick_up_tip(tiprack_obj.wells(-(i + end_gap + 1)))
        pipette_obj.drop_tip(tiprack_obj.wells(i))


tip_rerack(TIP_RACK, PIPETTE, 5, 0)

if __name__ == "__main__":
    for c in robot.commands():
        print(c)