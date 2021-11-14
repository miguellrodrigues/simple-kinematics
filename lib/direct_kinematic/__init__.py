import numpy as np

from lib.frame import rotate_x, rotate_z, translate, Frame
from prettytable import PrettyTable

# homogeneous transformation matrix from a generic robot
# A = [Rz(theta1).Tz(d1).Tx(d2).Rx(-90)]. [Rz(theta2).Tz(0).Tx(d3).Rx(0)] . [Rz(theta3).Tz(0).Tx(d4).Rx(0)]


class Joint:
  def __init__(self, dhp):
    self.dhp = dhp
    self.A = self.compute_joint_htm()
    
  def compute_joint_htm(self):
    rz = rotate_z(self.dhp[0])
    tz = translate(0, 0, self.dhp[1])
    tx = translate(self.dhp[2], 0, 0)
    rx = rotate_x(self.dhp[3])
  
    return rz @ tz @ tx @ rx

  def update_joint_htm(self, theta):
    self.dhp[0] = theta
    self.A = self.compute_joint_htm()


class DirectKinematic:
  def __init__(self, joints):
    self.joints = joints
    self.htm = self.compute_htm()
  
  def compute_htm(self):
    htm = self.joints[0].A
    for i in range(1, len(self.joints)):
      htm = htm @ self.joints[i].A
      
    return htm

  def get_htm(self):
    return self.htm
  
  def get_theta(self):
    return np.array([joint.dhp[0] for joint in self.joints])

  def set_theta(self, joint, theta):
    self.joints[joint].update_joint_htm(theta)
    
    self.htm = self.compute_htm()

  def get_joint_frame(self, joint):
    frame = Frame(0, 0, 0)
    
    if joint == 0:
      frame.data = self.joints[0].A
    elif joint == len(self.joints) - 1:
      frame.data = self.htm
    else:
      for i in range(0, joint):
        frame.data = frame.data @ self.joints[i].A
      frame.data = np.linalg.inv(frame.data)
    
    return frame

  def print(self):
    t = PrettyTable(['Joint', 'theta', 'd', 'a', 'alpha'])

    for i, joint in enumerate(self.joints):
      t.add_row([f'{i + 1}', joint.dhp[0], joint.dhp[1], joint.dhp[2], joint.dhp[3]])
    
    print(' ')
    print(t)
    print(' ')
  
