# Parameters:
stock_conc_uM = 1000
serial_concs_uM = [100, 10, 1, 0.1, 0.01]
final_vol_uL = 100

# Main algorithm:
def serial(stock_c, serial_c_list, serial_v):
    N = len(serial_c_list)
    dilutant_vols = []
    serial_vols = []

    v1 = serial_c_list[0] * serial_v / stock_c
    serial_vols.append(v1)
    dilutant_vols.append(serial_v - v1)

    for i in range(1, N):
        V = serial_c_list[i] * serial_v / serial_c_list[i-1]
        serial_vols.append(V)
        dilutant_vols.append(serial_v - V)
    return serial_vols, dilutant_vols

def serial2(stock_c, serial_c_list, final_v):
    '''Calculate the volumes needed for a serial dilution'''
    N = len(serial_c_list)
    V1 = serial_c_list[0] * final_v / stock_c
    serial_vols = [V1]
    for i in range(1, N):
        V = serial_c_list[i] * final_v / serial_c_list[i-1]
        serial_vols.append(V)
    return serial_vols

print(serial(stock_conc_uM, serial_concs_uM, final_vol_uL))
print(serial2(stock_conc_uM, serial_concs_uM, final_vol_uL))
