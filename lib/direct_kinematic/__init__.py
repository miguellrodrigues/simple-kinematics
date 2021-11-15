import numpy as np

from lib.frame import x_rotation_matrix, z_rotation_matrix, translation_matrix, Frame
from prettytable import PrettyTable

# homogeneous transformation matrix from a generic robot
# A = [Rz(theta1).Tz(d1).Tx(d2).Rx(-90)]. [Rz(theta2).Tz(0).Tx(d3).Rx(0)] . [Rz(theta3).Tz(0).Tx(d4).Rx(0)]


class Link:
  def __init__(self, dhp):
    self.dhp = dhp
    self.A = self.compute_link_htm()
    
  def compute_link_htm(self):
    rz = z_rotation_matrix(self.dhp[0])
    tz = translation_matrix(0, 0, self.dhp[1])
    tx = translation_matrix(self.dhp[2], 0, 0)
    rx = x_rotation_matrix(self.dhp[3])
  
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
    frame = Frame(0, 0, 0, name=f'link{link}')
    
    if link == 0:
      frame.translate(self.links[0].A[0][3],
                      self.links[0].A[1][3],
                      self.links[0].A[2][3])

      frame.rotation = self.links[0].A[0:3, 0:3]
    elif link == len(self.links) - 1:
      frame.translate(self.htm[0][3],
                      self.htm[0][3],
                      self.htm[2][3])
      
      frame.rotation = self.htm[0:3, 0:3]
    else:
      A = self.links[0].A
      
      for i in range(1, link):
        A = A @ self.links[i].A

      frame.translate(A[0][3],
                      A[1][3],
                      A[2][3])

      frame.rotation = A[0:3, 0:3]
    
    return frame

  def print(self):
    t = PrettyTable(['link', 'theta', 'd', 'a', 'alpha'])

    for i, link in enumerate(self.links):
      dhp = np.round(link.dhp, 6)
      t.add_row([f'{i + 1}', dhp[0], dhp[1], dhp[2], dhp[3]])
    
    print(' ')
    print(t)
    print(' ')
  
