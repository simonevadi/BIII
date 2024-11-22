import pandas as pd
import numpy as np

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



dtype = [
    ('coupling', 'int32'),  # Add this line to include the keys
    ('sig_x', 'float64'),
    ('sig_x_prime', 'float64'),
    ('sig_y', 'float64'),
    ('sig_y_prime', 'float64')
]


# Create an empty list to hold the data
data = []

# Fill the list with the data from the dictionary, including the keys
for key, values in b3_dict.items():
    # Append a tuple that starts with the key and follows with the values
    entry = (key,) + tuple(values[name] for name in ['sig_x', 'sig_x_prime', 'sig_y', 'sig_y_prime'])
    data.append(entry)

# Create the structured numpy array
b3_array = np.array(data, dtype=dtype)