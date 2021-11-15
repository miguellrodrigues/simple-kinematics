import numpy as np

from lib.direct_kinematic import Link, DirectKinematic

l2 = .2
l3 = .15
l4 = .1
l5 = .08

d3 = .1

j0 = Link([np.pi / 4, 0, l2, 0])
j1 = Link([np.pi / 4, 0, l3, np.pi])
j2 = Link([0, l4 + d3, 0, 0])
j3 = Link([np.pi / 2, l5, 0, 0])

dk = DirectKinematic([j0, j1, j2, j3])
dk.print()

print(np.round(dk.get_htm(), 6))
