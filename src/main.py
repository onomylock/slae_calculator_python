import solver

sol = solver.SolverSLAE()

sol.read_input()
sol.generate_matrix_b()
k, res = sol.solve()

print(k)
print(res)
