from math import radians

from frame import Frame
import matplotlib.pyplot as plt

zero = Frame(0, 0, 0)
f1 = Frame(0, 0, 0)

f1.rotate(0, 0, radians(45))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

zero.draw(fig, ax)
f1.draw(fig, ax)

plt.show()
