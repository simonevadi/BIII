emittance_data = {
    2: {
        "sig_x_um": 226.50,
        "sig_x_mm": 226.50/1000,
        "sig_xp_urad": 21.66,
        "sig_y_um": 18.76,
        "sig_y_mm": 18.76/1000,
        "sig_yp_urad": 5.23
    },
    10: {
        "sig_x_um": 218.10,
        "sig_x_mm": 218.10/1000,
        "sig_xp_urad": 20.86,
        "sig_y_um": 40.40,
        "sig_y_mm": 40.40/1000,
        "sig_yp_urad": 11.25
    },
    50: {
        "sig_x_um": 186.90,
        "sig_x_mm": 186.90/1000,
        "sig_xp_urad": 17.86,
        "sig_y_um": 77.35,
        "sig_y_mm": 77.35/1000,
        "sig_yp_urad": 21.55
    },
    75: {
        "sig_x_um": 173.10,
        "sig_x_mm": 173.10/1000,
        "sig_xp_urad": 16.54,
        "sig_y_um": 87.71,
        "sig_y_mm": 87.71/1000,
        "sig_yp_urad": 24.43
    },
    100: {
        "sig_x_um": 161.90,
        "sig_x_mm": 161.90/1000,
        "sig_xp_urad": 15.47,
        "sig_y_um": 94.74,
        "sig_y_mm": 94.74/1000,
        "sig_yp_urad": 26.39
    }
}


emittance_standard = emittance_data[2]      # 2 means 2 percent coupling, 10 means 10 percent coupling, etc.

# Note: Coupling 2 % is valid. For all higher couplings, the error is larger.
# BESSY II standard coupling is 2 %.