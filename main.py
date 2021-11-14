from math import radians

import numpy as np

from lib.frame import Frame, FrameDrawer, rotate_around_arbitrary_vector

zero = Frame(0, 0, 0)
f1 = Frame(1, 1, 0)

f1.rotate(0, 0, 1)

print(f1.get_x_component(),
      f1.get_y_component(),
      f1.get_z_component())

drawer = FrameDrawer([zero, f1])
drawer.show()
