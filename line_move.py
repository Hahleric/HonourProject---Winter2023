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

matplotlib.use("TkAgg")
# figure for line, 15*5 is the size of the figure
LINE_FIGURE_SIZE = (15, 5)
# number of robots we have in figure
ROBOT_NUMBER = 200
# length of the line
N = 20

# creating an x-axis
fig = plt.figure(figsize=LINE_FIGURE_SIZE)
ind = np.arange(N)
axis = ax.Subplot(fig, 111)
axis.axis[:].set_visible(False)
fig.add_axes(axis)
axis.axis["x"] = axis.new_floating_axis(0, 0, axis_direction="bottom")
plt.xlim(0, N)

# create robots based on numbers, add their x and y to a list
robot_list = []
for i in range(ROBOT_NUMBER):
    robot_list.append(r.Robot(chr(ord('A') + i), random.randint(1, N), 0))
robots_x = [i.x for i in robot_list]
robots_y = [i.y for i in robot_list]

robot_points = []
for i in range(len(robot_list)):
    robot_points.append(axis.plot(robots_x[i], robots_y[i], 'o', color='blue')[0])

for i in robot_list:
    i.ano = axis.annotate(i.name, xy=(i.x, i.y),
                          xytext=(i.x, i.y + 5),
                          textcoords="data",
                          )


def get_two_random_robots():
    return random.sample(robot_points, 2)


# function update for matlibplot animation, it will move r1 to a random position in every frame

def line_update():
    to_move_positions = []
    for robot in robot_points:
        robot1, robot2 = get_two_random_robots()
        distance_to_r1 = abs(robot1.get_xdata() - robot.get_xdata())
        distance_to_r2 = abs(robot2.get_xdata() - robot.get_xdata())
        if distance_to_r1 < distance_to_r2:
            to_move_positions.append(robot1.get_xdata())
        else:
            to_move_positions.append(robot2.get_xdata())

    for m in range(len(robot_points)):
        robot_points[m].set_xdata(to_move_positions[m])


def is_finished():
    for i in range(len(robot_points)):
        if robot_points[i].get_xdata()[0] != robot_points[0].get_xdata()[0]:
            return False
    return True


t = 0


def update(n):
    global t
    t += 1
    line_update()
    for m in range(len(robot_list)):
        robot_list[m].ano.set_position((robot_points[m].get_xdata(), robot_points[m].get_ydata()[0]))
    if is_finished():
        print("done")
        print(t)
        ani.pause()
    return robot_points


ani = FuncAnimation(fig, update, interval=2, frames=60)
plt.show()
