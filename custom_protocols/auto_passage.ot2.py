# Imports:
from opentrons import instruments, labware, robot, modules


metadata = {
    "protocolName": "auto_passage",
    "author": "Jake Bowden - Imperial Student Biofoundry",
    "source": "github.com/JBwdn/M5-Team-4",
}


# Parameters:
sample_ODs = [0.3]
sample_wells = ["A1"]
sample_destinations = ["A2"]
LB_well = "A1"
passage_vol = 50
P300_tip_column = 0
P10_first_tip = "A1"

master_settings = {
    "P300_multi": {"Mount": "right", "Rack": "10"},
    "P10_single": {"Mount": "left", "Rack": "11"},
    "Plate": {"Position": "9"},
    "Tube_rack": {"Position": "4"},
    "Temp_module": {"Position": "8"},
}


# Labware:
tempdeck = modules.load("tempdeck", master_settings['Temp_module']["Position"])
hotplate = labware.load(
    "opentrons_24_aluminumblock_generic_2ml_screwcap", master_settings['Temp_module']["Position"], share=True
)
sample_plate = labware.load(
    "4ti-0960_FrameStar", 
    master_settings["Plate"]["Position"]
)

p10_tip_rack = labware.load(
    "opentrons_96_tiprack_10ul", 
    master_settings["P10_single"]["Rack"]
)
P10 = instruments.P10_Single(
    mount=master_settings["P10_single"]["Mount"], 
    tip_racks=[p10_tip_rack]
)
P10.start_at_tip(p10_tip_rack.well(P10_first_tip))

p300_tip_rack = labware.load(
    "opentrons_96_tiprack_300ul", 
    master_settings["P300_multi"]["Rack"]
)
P300 = instruments.P300_Multi(
    mount=master_settings["P300_multi"]["Mount"], 
    tip_racks=[p300_tip_rack]
)
P300.start_at_tip(p300_tip_rack.cols(P300_tip_column))


# Main:
LB_vols = [passage_vol * OD for OD in sample_ODs]
tempdeck.set_temperature(37)
tempdeck.wait_for_temp()
robot.comment(
    "Insert sample plate into position:" + master_settings["Plate"]["Position"]
)
robot.pause()

# Resuspend cells:
P300.pick_up_tip()
P300.mix(10, 100, sample_plate.cols(0).bottom(1))
P300.return_tip()

# Pipette LB and passage:
for i in range(len(sample_ODs)):
    P10.pick_up_tip()
    P10.mix(3, 10, hotplate.well(LB_well))  # Wet tip...
    P10.transfer(
        LB_vols[i],
        hotplate.well(LB_well),
        sample_plate(sample_destinations[i]),
        new_tip="never",
    )
    P10.transfer(
        passage_vol - LB_vols[i],
        sample_plate(sample_wells[i]),
        sample_plate(sample_destinations[i]),
        air_gap=2,
        new_tip="never",
    )
    P10.mix(10, 10, sample_plate.well(sample_destinations[i]).bottom(1))
    P10.drop_tip()

# Dispose of previous sample:
P300.pick_up_tip()
P300.aspirate(280, sample_plate.cols(0).bottom(1))
P300.air_gap(20)
P300.return_tip()


# Debugging:
if __name__ == "__main__":
    for c in robot.commands():
        print(c)
