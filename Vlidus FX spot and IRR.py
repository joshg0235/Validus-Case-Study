import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt

# PART A, MC paths for Spot FX rate over 5 years
paths = 1000
T = 1  # will use a year as time frame, with each column used at S_0 in next step
s0 = 1.2401     # spot
sig = 0.1228    # vol
mu = 0          # included for scalability if needed in future use
s = np.zeros((paths, 6), dtype=float)     # each row will be a separate path and column i the ith year from start
s[:, 0] = s0        # set column one to be starting FX spot rate

# generate random Gaussian values, need matrix of one for each step
epsilon = np.random.randn(paths, 5)
#print(epsilon)

for j in range(1, 6):
    for i in range(paths):
        s[i, j] = s[i, j-1] * math.exp((sig * epsilon[i, j-1] * math.sqrt(T)) + (mu - (0.5 * sig**2)) * T)

# quick check to see the evolution of spot prices
#print(s)
#plt.ylabel('Spot FX')
#plt.xlabel('Years ahead')
#plt.plot(s.T)
#plt.show()



# PART B, find adjusted CFS and evaluate and plot IRR
# base case of the IRR, built in python IRR assumes even spaced intervals, doesnt account for leap years
#print(np.irr([-100, 15, 15, 15, 15, 100]))

# create matrix where each row is the cashflows for each path
cashflows = np.zeros((paths, 6), dtype=float)
cashflows[:, 0] = -100
cashflows[:, 1] = cashflows[:, 2] = cashflows[:, 3] = cashflows[:, 4] = 15
cashflows[:, 5] = 100

# matrix of adjusted cashflows by multiplying through found spots
MC_cashflows = s*cashflows

# column vector of IRR for each path
MC_IRR = np.zeros((paths, 1), dtype=float)
for i in range(paths):
    MC_IRR[i] = np.irr(MC_cashflows[i])

# print(MC_cashflows)

# sort IRR for simulated paths and print out percentiles
MC_IRR = np.sort(MC_IRR, axis=0)
# print(MC_IRR)
print("The 5th Percentile is: ", MC_IRR[int((paths*.05)-1)])
print("The 50th Percentile is: ", MC_IRR[int((paths*.5)-1)])
print("The 95th Percentile is: ", MC_IRR[int((paths*.95)-1)])

# plot the distribution of the IRR
bins_size = np.arange(MC_IRR.min(), MC_IRR.max()+.1, 0.02)
plt.hist(MC_IRR, bins=bins_size)
plt.ylabel('Frequency')
plt.xlabel('IRR')
plt.title('IRR Distribution')
plt.show()
