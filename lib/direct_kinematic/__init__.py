import numpy as np

from lib.frame import rotate_x, rotate_z, translate, Frame
from prettytable import PrettyTable

# homogeneous transformation matrix from a generic robot
# A = [Rz(theta1).Tz(d1).Tx(d2).Rx(-90)]. [Rz(theta2).Tz(0).Tx(d3).Rx(0)] . [Rz(theta3).Tz(0).Tx(d4).Rx(0)]


class Link:
  def __init__(self, dhp):
    self.dhp = dhp
    self.A = self.compute_link_htm()
    
  def compute_link_htm(self):
    rz = rotate_z(self.dhp[0])
    tz = translate(0, 0, self.dhp[1])
    tx = translate(self.dhp[2], 0, 0)
    rx = rotate_x(self.dhp[3])
  
    return rz @ tz @ tx @ rx

  def update_link_htm(self, i, v):
    self.dhp[i] = v
    
    self.A = self.compute_link_htm()


class DirectKinematic:
  def __init__(self, links):
    self.links = links
    self.htm = self.compute_htm()
  
  def compute_htm(self):
    htm = self.links[0].A
    for i in range(1, len(self.links)):
      htm = htm @ self.links[i].A
      
    return htm

  def get_htm(self):
    return self.htm
  
  def get_x_y_z(self):
    return self.htm[0:3, 3]
  
  def get_theta(self):
    return np.array([link.dhp[0] for link in self.links])

  def set_theta(self, link, theta):
    self.links[link].update_link_htm(0, theta)
    
    self.htm = self.compute_htm()

  def get_link_frame(self, link):
    frame = Frame(0, 0, 0)
    
    if link == 0:
      frame.data = self.links[0].A
    elif link == len(self.links) - 1:
      frame.data = self.htm
    else:
      for i in range(0, link):
        frame.data = frame.data @ self.links[i].A
      frame.data = np.linalg.inv(frame.data)
    
    return frame

  def print(self):
    t = PrettyTable(['link', 'theta', 'd', 'a', 'alpha'])

    for i, link in enumerate(self.links):
      t.add_row([f'{i + 1}', link.dhp[0], link.dhp[1], link.dhp[2], link.dhp[3]])
    
    print(' ')
    print(t)
    print(' ')
  
