import numpy as np
import os
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import math

# IMU
# 1. mathematiacally check transforms (y_coordinates, z_coordinated interchanged)
# y -y : S R T

CONST_EULER_ANGLE = [-np.pi/12, -np.pi/24, 0]


enable_3D = True 
enable_2D = True
enable_depth = True

def eulerAnglesToRotationMatrix(theta) :
  R_x = np.array([[1,         0,                  0                   ],
                  [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                  [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                  ])

  R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                  [0,                     1,      0                   ],
                  [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                  ])

  R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                  [math.sin(theta[2]),    math.cos(theta[2]),     0],
                  [0,                     0,                      1]
                  ])

  R = np.dot(R_z, np.dot( R_y, R_x )) 
  ###CHECK


  return R
###########################Ground truths###########################################################

CONST_R_MATRIX = eulerAnglesToRotationMatrix(CONST_EULER_ANGLE)
print(CONST_R_MATRIX)

x=[]
y=[]
z=[]

file1 = open('outputx.txt', 'r')
file2= open('outputy.txt', 'r')
file3 = open('outputz.txt', 'r')

for line in file1.readlines():
  x.append(float(line))

for line2 in file2.readlines():
  y.append(float(line2))

for line3 in file3.readlines():
  z.append(float(line3))  
# X Y Z ARE GT
###########################ORB###########################################################

array2D = [ ]
with open('bag1_rgbd.txt_cam_traj.txt' , 'r') as f:
    for line in f.readlines():
        array2D.append(line.split(' '))
x_coordinates = [0]
y_coordinates = [0]
z_coordinates = [0]

for i in range (len(array2D)):

    x_coordinates.append(array2D[i][1])
    y_coordinates.append(array2D[i][2])
    z_coordinates.append(array2D[i][3])


x_coordinates = [float(x) for x in x_coordinates]
y_coordinates = [float(x) for x in y_coordinates]
z_coordinates = [float(x) for x in z_coordinates]

current_pos = [0,0,0]

for i in range (len(x_coordinates)):
  current_pos[0] = x_coordinates[i]
  current_pos[1] = y_coordinates[i]
  current_pos[2] = z_coordinates[i]

  new_pos = np.dot(CONST_R_MATRIX, current_pos)

  x_coordinates[i] = new_pos[0]
  y_coordinates[i] = new_pos[1]
  z_coordinates[i] = new_pos[2]

###########################TRANSLATION+SCALE###########################################################


  #  x:  8.3 cm
  #  y: -3.0 cm
  #  z: -4.5 cm


transform = [.083,-.03,-.045]

sx = 6.4
sz = 6.4


for i in range (len(x_coordinates)):
  x_coordinates[i] = sx*(x_coordinates[i]) +x[0]+ transform[0]
  y_coordinates[i] = (y_coordinates[i] + z[0] + transform[2])
  z_coordinates[i] = sz*(z_coordinates[i]) + y[0]+ transform[1]

for i in range (len(y_coordinates)):
   y_coordinates[i] = -1*y_coordinates[i]
#####################################PLOT##################################################################



print ("inital GROUND TRUTH" , x[0],y[0],z[0] )
print ("inital ORB " , x_coordinates[0],y_coordinates[0],z_coordinates[0] )
if enable_3D:
    plt.style.use('seaborn-poster')
    fig = plt.figure(figsize = (8,8))
    ax = plt.axes(projection='3d')
    ax.grid()


    ax.plot3D(x_coordinates, z_coordinates, y_coordinates)
    ax.plot3D(x,y,z)
    ax.set_title('3D- Trajectory')

    ax.set_xlabel('x (meters)', labelpad=20)
    ax.set_ylabel('y', labelpad=20)
    ax.set_zlabel('z', labelpad=20)

    plt.show()

if enable_2D:

    plt.plot(x_coordinates,z_coordinates, 'r')
    plt.plot(x,y,'g')
    ax = plt.axes()
    ax.grid()
    plt.axis('scaled')

    ax.set_xlabel('x (meters)', labelpad=20)
    ax.set_ylabel('y', labelpad=20)
    plt.show()

# y_coordinates2 = []

# half = int (len(y_coordinates)/2)
# for i in range (len(y_coordinates)):
#    if (i<=half):
#       y_coordinates2.append(-1*y_coordinates[i])
#    else:
#       y_coordinates2.append(y_coordinates[i])



if enable_depth:
    t1 = np.linspace(0, 1, len(y_coordinates))
    t2 = np.linspace(0, 1, len(z))

    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('counts')
    ax1.set_ylabel('depth_orb', color=color)
    ax1.plot(t1, y_coordinates, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('depth_gt', color=color)  # we already handled the x-label with ax1
    ax2.plot(t2, z, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()



