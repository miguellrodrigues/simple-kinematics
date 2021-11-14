import numpy as np

from lib.direct_kinematic import Joint, DirectKinematic
# from lib.frame import FrameDrawer

j0 = Joint([np.radians(45), 0, 2, 0])
j1 = Joint([np.radians(45), 0, 1.5, np.pi])
j2 = Joint([0, 2, 0, 0])
j3 = Joint([np.radians(90), .8, 0, 0])

dk = DirectKinematic([j0, j1, j2, j3])
dk.print()

print(dk.get_htm())

# f1 = dk.get_joint_frame(0)
# f2 = dk.get_joint_frame(1)
# f3 = dk.get_joint_frame(2)
# f4 = dk.get_joint_frame(3)
#
#
# def update():
#   theta = dk.get_theta()[0]
#
#   if theta < 1.57:
#     dk.set_theta(0, theta + 0.001)
#
#   f1.data = dk.get_joint_frame(0).data
#   f2.data = dk.get_joint_frame(1).data
#   f3.data = dk.get_joint_frame(2).data
#   f4.data = dk.get_joint_frame(3).data
#
#
# drawer = FrameDrawer([f1, f2, f3, f4], update)
# drawer.show()
