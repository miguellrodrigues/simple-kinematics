import matplotlib.pyplot as plt
import numpy as np

from lib.arrow3d import Arrow3D


def rotate_x(theta):
  """
  Rotation matrix around the x axis
  """
  return np.array([[1, 0, 0, 0],
                   [0, np.cos(theta), -np.sin(theta), 0],
                   [0, np.sin(theta), np.cos(theta), 0],
                   [0, 0, 0, 1]])


def rotate_y(theta):
  """
  Rotation matrix around the y axis
  """
  return np.array([[np.cos(theta), 0, np.sin(theta), 0],
                   [0, 1, 0, 0],
                   [-np.sin(theta), 0, np.cos(theta), 0],
                   [0, 0, 0, 1]])


def rotate_z(theta):
  """
  Rotation matrix around the z axis
  """
  return np.array([[np.cos(theta), -np.sin(theta), 0, 0],
                   [np.sin(theta), np.cos(theta), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])


def rotate_x_y_z(theta_x, theta_y, theta_z):
  """
  Rotation matrix around the x, y and z axis
  """
  return rotate_z(theta_z).dot(rotate_y(theta_y)).dot(rotate_x(theta_x))


class Frame:
  def __init__(self, x, y, z):
    self.translation = np.array([
      [1, 0, 0, x],
      [0, 1, 0, y],
      [0, 0, 1, z],
      [0, 0, 0, 1]
    ])
  
  def translate(self, dx, dy, dz):
    self.translation = self.translation @ np.array([
      [1, 0, 0, dx],
      [0, 1, 0, dy],
      [0, 0, 1, dz],
      [0, 0, 0, 1]])
  
  def rotate(self, theta_x, theta_y, theta_z):
    self.translation = rotate_x_y_z(theta_x, theta_y, theta_z) @ self.translation
  
  def get_x_component(self):
    return self.translation[0, 3]
  
  def get_y_component(self):
    return self.translation[1, 3]
  
  def get_z_component(self):
    return self.translation[2, 3]
  
  def draw(self, fig, ax):
    arrow_prop_dict = dict(mutation_scale=40, arrowstyle='->', shrinkA=0, shrinkB=0)
    
    x, y, z = [
      self.get_x_component(),
      self.get_y_component(),
      self.get_z_component()
    ]
    
    _x = [
      [x, x + self.translation[0, 0]],
      [y, y + self.translation[1, 0]],
      [z, z + self.translation[2, 0]]
    ]
    
    _y = [
      [x, x + self.translation[0, 1]],
      [y, y + self.translation[1, 1]],
      [z, z + self.translation[2, 1]]
    ]
    
    _z = [
      [x, x + self.translation[0, 2]],
      [y, y + self.translation[1, 2]],
      [z, z + self.translation[2, 2]]
    ]
    
    x_arr = Arrow3D(
      _x[0],
      _x[1],
      _x[2],
      **arrow_prop_dict, color='r')
    
    y_arr = Arrow3D(
      _y[0],
      _y[1],
      _y[2],
      **arrow_prop_dict, color='g')
    
    z_arr = Arrow3D(
      _z[0],
      _z[1],
      _z[2],
      **arrow_prop_dict, color='b')
    
    ax.add_artist(x_arr)
    ax.add_artist(y_arr)
    ax.add_artist(z_arr)
    
    ax.text(x, y, z, r'$o$')
    ax.text(_x[0][1], _x[1][1], _x[2][1], r'$x$')
    ax.text(_y[0][1], _y[1][1], _y[2][1], r'$y$')
    ax.text(_z[0][1], _z[1][1], _z[2][1], r'$z$')
    
    ax.view_init(azim=-90, elev=90)
    ax.set_axis_off()
