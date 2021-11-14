import numpy as np
from matplotlib import pyplot as plt, animation

from lib.arrow3d import Arrow3D


def rotate_x(yaw):
  """
  Rotation matrix around the x axis
  """
  return np.array([[1, 0, 0, 0],
                   [0, np.cos(yaw), -np.sin(yaw), 0],
                   [0, np.sin(yaw), np.cos(yaw), 0],
                   [0, 0, 0, 1]])


def rotate_y(pitch):
  """
  Rotation matrix around the y axis
  """
  return np.array([[np.cos(pitch), 0, np.sin(pitch), 0],
                   [0, 1, 0, 0],
                   [-np.sin(pitch), 0, np.cos(pitch), 0],
                   [0, 0, 0, 1]])


def rotate_z(roll):
  """
  Rotation matrix around the z axis
  """
  return np.array([[np.cos(roll), -np.sin(roll), 0, 0],
                   [np.sin(roll), np.cos(roll), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])


def rotate_x_y_z(yaw, pitch, roll):
  """
  Rotation matrix around the x, y and z axis
  """
  return rotate_x(yaw).dot(rotate_y(pitch)).dot(rotate_z(roll))


def rotate_around_arbitrary_vector(theta, v):
  """
  Rotation matrix around an arbitrary vector
  """
  v = v / np.linalg.norm(v)
  v_x = np.array([[0, -v[2], v[1], 0],
                  [v[2], 0, -v[0], 0],
                  [-v[1], v[0], 0, 0],
                  [0, 0, 0, 1]])
  
  return np.eye(4) + v_x + np.dot(v_x, v_x) * (1 - np.cos(theta))


def translate(dx, dy, dz):
  return np.array([
    [1, 0, 0, dx],
    [0, 1, 0, dy],
    [0, 0, 1, dz],
    [0, 0, 0, 1]])


class Frame:
  def __init__(self, x, y, z):
    self.position = np.array([
      [1, 0, 0, x],
      [0, 1, 0, y],
      [0, 0, 1, z],
      [0, 0, 0, 1]
    ])
    
    self.rotation = np.eye(4)
  
  def translate(self, dx, dy, dz):
    self.position = translate(dx, dy, dz) @ self.position
    
    return self.position
  
  def rotate(self, yaw, pitch, roll):
    self.rotation = rotate_x_y_z(yaw, pitch, roll) @ self.rotation
    return self.rotation
  
  def rotate_around_arbitrary_vector(self, theta, v):
    self.rotation = rotate_around_arbitrary_vector(theta, v) @ self.rotation
  
  def get_x_component(self):
    return self.position[0, 3]
  
  def get_y_component(self):
    return self.position[1, 3]
  
  def get_z_component(self):
    return self.position[2, 3]
  
  def translate_to(self, other, p=.01):
    dx = other.get_x_component() - self.get_x_component()
    dy = other.get_y_component() - self.get_y_component()
    dz = other.get_z_component() - self.get_z_component()
    
    self.translate(
      dx * p,
      dy * p,
      dz * p
    )
    
    return np.linalg.norm([dx, dy, dz])

  def rotation_matrix(self):
    return self.rotation
  
  def rotation_to(self, other):
    yaw = np.arctan2(other.rotation[2, 1], other.rotation[2, 2]) - np.arctan2(self.rotation[2, 1], self.rotation[2, 2])
    pitch = np.arctan2(other.rotation[2, 0], other.rotation[2, 2]) - np.arctan2(self.rotation[2, 0], self.rotation[2, 2])
    roll = np.arctan2(other.rotation[1, 0], other.rotation[0, 0]) - np.arctan2(self.rotation[1, 0], self.rotation[0, 0])
    
    return [yaw, pitch, roll]
  
  def get_frame_cords(self):
    x, y, z = [
      self.get_x_component(),
      self.get_y_component(),
      self.get_z_component()
    ]
    
    _x = [
      [x, x + self.rotation[0, 0]],
      [y, y + self.rotation[1, 0]],
      [z, z + self.rotation[2, 0]]
    ]
    
    _y = [
      [x, x + self.rotation[0, 1]],
      [y, y + self.rotation[1, 1]],
      [z, z + self.rotation[2, 1]]
    ]
    
    _z = [
      [x, x + self.rotation[0, 2]],
      [y, y + self.rotation[1, 2]],
      [z, z + self.rotation[2, 2]]
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
    self.ax.view_init(azim=-40, elev=70)
    self.ax.set_axis_off()
    
    self.update = update_func
  
  def plot(self):
    for frame in self.frames:
      frame.draw(self.ax)
  
  def show(self):
    self.plot()
    
    if self.update:
      ani = animation.FuncAnimation(self.fig, self.animate, 200, interval=1, blit=False)
      # ani.save('animation.gif', fps=60, dpi=300)
    
    plt.show()
  
  def animate(self, num):
    self.ax.artists.clear()
    self.update()
    self.plot()
