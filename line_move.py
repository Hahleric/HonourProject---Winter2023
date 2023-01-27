# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import mpl_toolkits.axisartist as ax
import Robot as r
import random
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation
from plain_move import plain_move

matplotlib.use("TkAgg")
# figure for line, 15*5 is the size of the figure
LINE_FIGURE_SIZE = (15, 5)
# number of robots we have in figure
ROBOT_NUMBER = 10
# length of the line
N = 32768
# random pick number
RANDOM_PICK_NUMBER = 1

# creating an x-axis
fig = plt.figure(figsize=LINE_FIGURE_SIZE)
ind = np.arange(N)
axis = ax.Subplot(fig, 111)
axis.axis[:].set_visible(False)
fig.add_axes(axis)
axis.axis["x"] = axis.new_floating_axis(0, 0, axis_direction="bottom")
plt.xlim(-N, N)

# create robots based on numbers, add their x and y to a list
robot_list = []
for i in range(ROBOT_NUMBER):
    robot_list.append(r.Robot(str(i + i), random.randint(-N, N), 0))

print([m.name for m in robot_list], [m.x for m in robot_list])
robots_x = [i.x for i in robot_list]
robots_y = [i.y for i in robot_list]

robot_points = []
for i in range(len(robot_list)):
    robot_points.append(axis.plot(robots_x[i], robots_y[i], 'o', color='blue')[0])

for i in robot_list:
    i.ano = axis.annotate(i.name, xy=(i.x, i.y),
                          xytext=(i.x, i.y),
                          textcoords="data",
                          )


def get_random_robots(robot_p):
    random_robots = []
    for i in range(RANDOM_PICK_NUMBER):
        random_robots.append(random.choice(robot_p))
    return random_robots


# function update for matlibplot animation, it will move r1 to a random position in every frame

def line_update(robot_p, robot_l):
    to_move_positions = []
    for robot in robot_p:
        random_r = get_random_robots(robot_p)
        distance = np.array([], dtype='longlong')
        for i in random_r:
            # get the distance between robot and random robot
            distance = np.append(distance,
                                 abs(int(robot.get_xdata()[0])
                                     - int(i.get_xdata()[0])))
        # get the indices of minimum distance
        min_indices = np.where(distance == np.amin(distance))
        min_index = np.random.choice(min_indices[0])
        # get the position of minimum distance
        min_position = random_r[min_index].get_xdata(), random_r[min_index].get_ydata()
        to_move_positions.append(min_position)
    print([m.name for m in robot_l], [m for m in to_move_positions])
    for m in range(len(robot_p)):
        x, y = to_move_positions[m]
        robot_p[m].set_markersize(6.0)
        robot_p[m].set_xdata(x)
        robot_p[m].set_ydata(y)


def is_finished():
    for i in range(len(robot_points)):
        if robot_points[i].get_xdata()[0] != robot_points[0].get_xdata()[0]:
            return False
    return True


t = 0


def update(n):
    for m in range(len(robot_list)):
        robot_list[m].ano.set_position((robot_points[m].get_xdata(), robot_points[m].get_ydata()[0]))
    global t
    t += 1
    line_update(robot_points, robot_list)
    for m in range(len(robot_list)):
        robot_list[m].ano.set_position((robot_points[m].get_xdata(), robot_points[m].get_ydata()[0]))
    for i in range(len(robot_points)):
        for j in range(i, len(robot_points)):
            if robot_points[i].get_xdata() == robot_points[j].get_xdata() and robot_points[i].get_ydata() == robot_points[j].get_ydata():
                size = robot_points[i].get_markersize()
                robot_points[i].set_markersize(size + 3)
                robot_points[j].set_markersize(size + 3)
    if is_finished():
        print("done")
        print(t)
        ani.pause()
    return robot_points


# ani = FuncAnimation(fig, update, interval=1000, frames=60)
# plt.show()

plain_move(robot_list, robot_points)
