import numpy as np

from lib.direct_kinematic import Link, DirectKinematic

j0 = Link([0, 4.5, 1.5, -np.pi / 2])
j1 = Link([-np.pi / 2, 0, 5.1, 0])
j2 = Link([0, 0, 1.3, np.pi / 2])
j3 = Link([0, -6.47, 0, -np.pi / 2])
j4 = Link([0, 0, 0, np.pi / 2])
j5 = Link([np.pi, -.95, 0, np.pi])

dk = DirectKinematic([j0, j1, j2, j3, j4, j5])
dk.print()

print(dk.get_htm())
