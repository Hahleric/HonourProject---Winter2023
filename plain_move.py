import numpy as np
import mpl_toolkits.axisartist as ax
import Robot as r
import random
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation

matplotlib.use("TkAgg")
# figure for line, 15*5 is the size of the figure
PLAIN_FIGURE_SIZE = (15, 5)
# number of robots we have in figure
ROBOT_NUMBER = 20
# length of the line
N = 200
# random pick number
RANDOM_PICK_NUMBER = 5


# creating a cartesian coordinate system
def create_plain():
    fig = plt.figure(figsize=PLAIN_FIGURE_SIZE)
    axis = ax.Subplot(fig, 111)
    axis.axis[:].set_visible(False)
    fig.add_axes(axis)
    axis.axis["x"] = axis.new_floating_axis(0, 0, axis_direction="bottom")
    axis.axis["y"] = axis.new_floating_axis(1, 0, axis_direction="left")
    axis.axis["x"].set_axisline_style("->", size=1.0)
    axis.axis["y"].set_axisline_style("->", size=1.0)
    plt.xlim(0, N)
    plt.ylim(0, N)

    return fig, axis


# create robots based on numbers and annotate them on axis, add their x and y to a list
def create_robots(axis):
    # create robots based on numbers, add their x and y to a list
    robot_list = []
    for i in range(ROBOT_NUMBER):
        robot_list.append(r.Robot(chr(ord('A') + i), random.randint(1, N), random.randint(1, N)))

    print([m.name for m in robot_list], [(m.x, m.y) for m in robot_list])
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
    return robot_list, robot_points


def get_random_robots(robot_points):
    return random.sample(robot_points, RANDOM_PICK_NUMBER)


def line_update(robot_points, robot_list):
    to_move_positions = []
    for robot in robot_points:
        random_r = get_random_robots(robot_points)

        for i in random_r:
            # get the distance between robot and random robot
            distance = np.sqrt((robot.get_xdata() - i.get_xdata()) ** 2 + (robot.get_ydata() - i.get_ydata()) ** 2)
        # get the index of minimum distance
        min_index = np.argmin(distance)
        # get the position of minimum distance
        min_position = random_r[min_index].get_xdata(), random_r[min_index].get_ydata()
        to_move_positions.append(min_position)
    print([m.name for m in robot_list], [m for m in to_move_positions])
    for m in range(len(robot_points)):
        x, y = to_move_positions[m]
        robot_points[m].set_xdata(x)
        robot_points[m].set_ydata(y)


def is_finished(robot_points):
    for i in range(len(robot_points)):
        if robot_points[i].get_xdata()[0] != robot_points[0].get_xdata()[0]:
            return False
    return True


t = 0
def update(n, robot_list, robot_points):
    for m in range(len(robot_list)):
        robot_list[m].ano.set_position((robot_points[m].get_xdata(), robot_points[m].get_ydata()))
    global t
    t += 1
    line_update(robot_points, robot_list)
    for m in range(len(robot_list)):
        robot_list[m].ano.set_position((robot_points[m].get_xdata(), robot_points[m].get_ydata()))
    if is_finished(robot_points):
        print("done")
        print(t)
        ani.pause()
    return robot_points


if __name__ == "__main__":
    fig, axis = create_plain()

    r_list, r_points = create_robots(axis)
    print(r_list)
    print(r_points)
    ani = FuncAnimation(fig, update, interval=1000, frames=60, fargs=(r_list, r_points))
    plt.show(block=True)
