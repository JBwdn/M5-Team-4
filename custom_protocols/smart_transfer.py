from opentrons import instruments, labware, robot


def smart_transfer(vols, labware_plate, from_wells, to_wells):
    for i in range(len(vols)):
        if vols[i] > 30:
            p300.transfer(
                vols[i],
                labware_plate.wells(from_wells[i]),
                labware_plate.wells(to_wells[i]),
                air_gap=20,
                new_tip='never',
                blow_out=True,)
                # mix_after=(5))
        else:
            p10.transfer(
                vols[i],
                labware_plate.wells(from_wells[i]),
                labware_plate.wells(to_wells[i]),
                air_gap=20,
                new_tip='never',
                blow_out=True,)
                # mix_after=(5))


# Labware:
plate = labware.load('96-flat', '1')

p300_tip_rack = labware.load('opentrons_96_tiprack_300ul', '4')
p10_tip_rack = labware.load('opentrons_96_tiprack_10ul', '3')
p300 = instruments.P300_Single(mount='left', tip_racks=[p300_tip_rack])
p10 = instruments.P10_Single(mount='right', tip_racks=[p10_tip_rack])


smart_transfer([2, 7, 15, 200], plate, ['A1', 'A1', 'A1', 'A1'], ['B1', 'C1', 'D1', 'E1'])

for c in robot.commands():
    print(c)