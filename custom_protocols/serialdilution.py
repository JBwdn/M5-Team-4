# Parameters:
stock_conc_uM = 50
serial_concs_uM = [10, 0.3, 0.1, 0.05]
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
        V = serial_c_list[i] * serial_v / serial_vols[-1]
        serial_vols.append(V)
        dilutant_vols.append(serial_v - V)

    return serial_vols, dilutant_vols


print(serial(stock_conc_uM, serial_concs_uM, final_vol_uL))
