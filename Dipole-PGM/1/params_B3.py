import pandas as pd

# sig in µm
# sig_prime µrad
b3_dict = {
    2: {'sig_x': 17.15, 'sig_x_prime': 5.72, 'sig_y': 2.43, 'sig_y_prime': 0.81},
    10: {'sig_x': 16.51, 'sig_x_prime': 5.51, 'sig_y': 5.22, 'sig_y_prime': 1.74},
    50: {'sig_x': 14.14, 'sig_x_prime': 4.71, 'sig_y': 10.00, 'sig_y_prime': 3.33},
    75: {'sig_x': 13.09, 'sig_x_prime': 4.36, 'sig_y': 11.34, 'sig_y_prime': 3.78},
    100: {'sig_x': 12.25, 'sig_x_prime': 4.08, 'sig_y': 12.25, 'sig_y_prime': 4.08}
}



# Creating DataFrame
b3_params = pd.DataFrame(b3_dict)
