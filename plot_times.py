import matplotlib.pyplot as plt
import numpy as np


data = np.loadtxt('./data/toys_rev2.csv', usecols=[2,], skiprows = 1, delimiter = ',')

plt.figure()
plt.hist(np.log10(data), bins=100, range=(0.0,5.0))


plt.figure()
plt.hist(np.log10(data), bins=100, range=(0.0,5.0), cumulative=True)

plt.show()
