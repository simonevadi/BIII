emittance_data = {
    2: {
        "sig_x_um": 68.59,
        "sig_x_mm": 68.59/1000,
        "sig_xp_urad": 71.65,
        "sig_y_um": 11.21,
        "sig_y_mm": 11.21/1000,
        "sig_yp_urad": 8.75
    },
    10: {
        "sig_x_um": 66.07,
        "sig_x_mm": 66.07/1000,
        "sig_xp_urad": 68.99,
        "sig_y_um": 24.14,
        "sig_y_mm": 24.14/1000,
        "sig_yp_urad": 18.83
    },
    50: {
        "sig_x_um": 56.63,
        "sig_x_mm": 56.63/1000,
        "sig_xp_urad": 59.08,
        "sig_y_um": 46.22,
        "sig_y_mm": 46.22/1000,
        "sig_yp_urad": 36.06
    },
    75: {
        "sig_x_um": 52.46,
        "sig_x_mm": 52.46/1000,
        "sig_xp_urad": 57.70,
        "sig_y_um": 52.41,
        "sig_y_mm": 52.41/1000,
        "sig_yp_urad": 40.89
    },
    100: {
        "sig_x_um": 49.11,
        "sig_x_mm": 49.11/1000,
        "sig_xp_urad": 51.17,
        "sig_y_um": 56.61,
        "sig_y_mm": 56.61/1000,
        "sig_yp_urad": 44.16
    }
}


emittance_standard = emittance_data[2]      # 2 means 2 percent coupling, 10 means 10 percent coupling, etc.

# Note: Coupling 2 % is valid. For all higher couplings, the error is larger.
# BESSY II standard coupling is 2 %.