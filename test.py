import numpy as np

from lib.direct_kinematic import Joint, DirectKinematic
from lib.frame import FrameDrawer

j0 = Joint([0, 1, 1, -np.pi / 2])
j1 = Joint([0, 0, 1, 0])
j2 = Joint([0, 0, 1, 0])

dk = DirectKinematic([j0, j1, j2])
dk.print()

f1 = dk.get_joint_frame(0)
f2 = dk.get_joint_frame(1)
f3 = dk.get_joint_frame(2)


def update():
  theta = dk.get_theta()[0]
  
  if theta > 1.57:
    dk.set_theta(0, theta + 0.001)

  f1.data = dk.get_joint_frame(0).data
  f2.data = dk.get_joint_frame(1).data
  f3.data = dk.get_joint_frame(2).data

  
drawer = FrameDrawer([f1, f2, f3], update)
drawer.show()
