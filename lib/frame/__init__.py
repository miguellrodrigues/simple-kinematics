import numpy as np
from matplotlib import pyplot as plt, animation

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
  
  def get_frame_cords(self):
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
    
    return [_x, _y, _z]
  
  def create_frame_arrows(self):
    arrow_prop_dict = dict(mutation_scale=40, arrowstyle='->', shrinkA=0, shrinkB=0)
    
    x, y, z = self.get_frame_cords()
    
    x_arr = Arrow3D(
      x[0],
      x[1],
      x[2],
      **arrow_prop_dict, color='r')
    
    y_arr = Arrow3D(
      y[0],
      y[1],
      y[2],
      **arrow_prop_dict, color='g')
    
    z_arr = Arrow3D(
      z[0],
      z[1],
      z[2],
      **arrow_prop_dict, color='b')
    
    return [x_arr, y_arr, z_arr]
  
  def draw(self, ax):
    arrows = self.create_frame_arrows()
    
    ax.add_artist(arrows[0])
    ax.add_artist(arrows[1])
    ax.add_artist(arrows[2])


class FrameDrawer:
  def __init__(self, frames, update_func=None):
    self.frames = frames
    
    self.fig = plt.figure()
    self.ax = self.fig.add_subplot(111, projection='3d')
    self.ax.view_init(azim=41, elev=38)
    self.ax.set_axis_off()
    
    self.update = update_func

  def plot(self):
    for frame in self.frames:
      frame.draw(self.ax)
      
  def show(self):
    self.plot()
    
    if self.update:
      ani = animation.FuncAnimation(self.fig, self.animate, 200, interval=1, blit=False)
      ani.save('animation.gif', fps=60, dpi=300)
    
    plt.show()

  def animate(self, num):
    self.ax.artists.clear()
    self.update()
    self.plot()

    