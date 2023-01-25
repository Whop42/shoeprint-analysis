import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("data.csv", delimiter=",")

x = data[:, 0]
y = data[:, 1]
z = data[:, 2]

fig = plt.figure()
ax = plt.axes(projection = "3d")

for i in range(0, len(x)):
    ax.plot3D(x[i], y[i], z[i])

plt.show()