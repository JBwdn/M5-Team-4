# Imports:
from opentrons import instruments, labware, robot


metadata = {
    "protocolName": "Customisable Serial Dilution",
    "author": "Jake Bowden - Imperial Student Biofoundry",
    "source": "github.com/JBwdn/M5-Team-4",
}


# Parameters:
master_settings = {
    "First_tip": {"L": "A1"},
    "Pipette": {"Mode": "P300", "Mount": "right", "Rack": "3"},
    "Plate": {"Position": "1"},
    "Tube_rack": {"Position": "4"},
}

job_1 = {
    "Stock": {"C": 1000, "L": "A1"},
    "Serial": {"C": [500, 250, 125], "L": ["B1", "C1", "D1"], "V": 100},
    "Solvent": {"L": "A2"},
}

job_2 = {
    "Stock": {"C": 600, "L": "A2"},
    "Serial": {"C": [400, 250, 125], "L": ["B2", "C2", "D2"], "V": 100},
    "Solvent": {"L": "A2"},
}

job_list = [job_1, job_2]


# Functions:
def serial_calculator(stock_c, serial_c_list, final_v):
    """Calculate the volumes needed for a serial dilution with predefined target concentrations."""
    serial_vols = [0 for i in range(len(serial_c_list))]
    serial_vols[0] = serial_c_list[0] * final_v / stock_c
    for i in range(1, len(serial_c_list)):
        V = serial_c_list[i] * final_v / serial_c_list[i - 1]
        serial_vols[i] = V
    return serial_vols


def serial_bot(serial_dict):
    """Execute the serial dilution laid out in the input dictionary on Opentrons OT-2."""
    # Constants:
    solvent_location = serial_dict["Solvent"]["L"]
    serial_locations = serial_dict["Serial"]["L"]
    stock_location = serial_dict["Stock"]["L"]
    serial_volumes = serial_dict["Serial"]["Volumes"]
    VT = serial_dict["Serial"]["V"]
    # Pipette solvent:
    pipette.pick_up_tip()
    pipette.transfer(
        [VT - vol for vol in serial_volumes],
        tube_rack.wells(solvent_location),
        plate.wells(serial_locations),
        new_tip="never",
        blow_out=True,
    )
    pipette.drop_tip()
    # First dilution:
    pipette.pick_up_tip()
    pipette.transfer(
        serial_volumes[0],
        tube_rack.well(stock_location),
        plate.well(serial_locations[0]),
        air_gap=20,
        new_tip="never",
        blow_out=False,
        mix_after=(5, 0.3 * VT),
    )
    # Serial dilution:
    pipette.transfer(
        serial_volumes[1:],
        plate.wells(serial_locations[:-1]),
        plate.wells(serial_locations[1:]),
        air_gap=20,
        new_tip="never",
        blow_out=False,
        mix_after=(5, 0.3 * VT),
    )
    pipette.drop_tip()


# Labware setup:
plate = labware.load("4ti-0960_FrameStar", master_settings["Plate"]["Position"])
tube_rack = labware.load(
    "tube-rack_E1415-1500", master_settings["Tube_rack"]["Position"]
)

if master_settings["Pipette"]["Mode"] == "P300":
    tip_rack = labware.load(
        "opentrons_96_tiprack_300ul", master_settings["Pipette"]["Rack"]
    )
    pipette = instruments.P300_Single(
        mount=master_settings["Pipette"]["Mount"], tip_racks=[tip_rack]
    )
elif master_settings["Pipette"]["Mode"] == "P10":
    tip_rack = labware.load(
        "opentrons_96_tiprack_10ul", master_settings["Pipette"]["Rack"]
    )
    pipette = instruments.P10_Single(
        mount=master_settings["Pipette"]["Mount"], tip_racks=[tip_rack]
    )

tip_location = master_settings["First_tip"]["L"]
pipette.start_at_tip(tip_rack.well(tip_location))


# Main loop:
for job in job_list:
    stock_conc = job["Stock"]["C"]
    serial_concs = job["Serial"]["C"]
    serial_vol = job["Serial"]["V"]
    job["Serial"]["Volumes"] = serial_calculator(stock_conc, serial_concs, serial_vol)
    serial_bot(job)


# Debugging:
if __name__ == "__main__":
    # Print parameters:
    for key, subdict in master_settings.items():
        print("\n", key)
        for key in subdict:
            print(key + ":", subdict[key])
    # Print commands:
    print("\n")
    for c in robot.commands():
        print(c)
