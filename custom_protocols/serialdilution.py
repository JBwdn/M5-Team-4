# Imports:
from opentrons import instruments, labware


def setup():
    # Labware:
    PLATE = labware.load('96-flat', '2')
    TIP_RACK = labware.load('tiprack-200ul', '1')
    # Pipettes:
    P300_PIPETTE = instruments.P300_Single(mount='left', tip_racks=[TIP_RACK])


# Commands:
def serial():
    P300_PIPETTE.pick_up_tip()

    pass


if __name__ == "__main__":
    setup()
    serial()