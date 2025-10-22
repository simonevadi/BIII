import numpy as np
from scipy.optimize import minimize

# L = 20
# r2_prime = 1.0

# def objective(x):
#     r, r_prime = x
#     r2 = L - r - r_prime - r2_prime
#     return - (r_prime * r2_prime) / (r * r2)

# # Explicit constraint: r2 = L - r - r' - 1 ≥ 1 → r + r' ≤ L - 2
# cons = [{
#     'type': 'ineq',
#     'fun': lambda x: (L - 2) - (x[0] + x[1])  # ≥ 0
# }]

# bounds = [(1.0, L - 3), (1.0, L - 3)]  # r > 1, r' > 1
# x0 = [3.0, 3.0]

# result = minimize(objective, x0, bounds=bounds, constraints=cons)

# r, r_prime = result.x
# r2 = L - r - r_prime - r2_prime
# value = (r_prime * r2_prime) / (r * r2)

# print("Best values found:")
# print(f"r = {r:.4f}")
# print(f"r' = {r_prime:.4f}")
# print(f"r2 = {r2:.4f}")
# print(f"r2' = {r2_prime}")
# print(f"Maximized value = {value:.6f}")
# print(f"Converged: {result.success}")
# print(f"Message: {result.message}")


def calculate_demagnification(p,q,p2,q2):
    print(f'M1:{p/q}, M2:{p2/q2}, tot: {p*p2/(q*q2)}')

calculate_demagnification(10,1,10,1)
calculate_demagnification(15,1,5,1)
calculate_demagnification(21,1, 1, 1)
