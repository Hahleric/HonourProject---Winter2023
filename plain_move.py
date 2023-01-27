import numpy
import numpy as np
import mpl_toolkits.axisartist as ax
import Robot as r
import random
import matplotlib.pyplot as plt
import matplotlib
import argparse
from matplotlib.animation import FuncAnimation

matplotlib.use("TkAgg")
# figure for line, 15*5 is the size of the figure
PLAIN_FIGURE_SIZE = (15, 5)
# number of robots we have in figure
ROBOT_NUMBER = 20
# length of the line
N = 32768
# random pick number
RANDOM_PICK_NUMBER = 4


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
    plt.xlim(-N, N)
    plt.ylim(-N, N)

    return fig, axis


# create robots based on numbers and annotate them on axis, add their x and y to a list
def create_robots(axis, manual_flag):
    # create robots based on numbers, add their x and y to a list
    if manual_flag:
        robot_list = []
        robot_points = []
        for i in range(ROBOT_NUMBER):
            name = input("Please input robot name: ")
            x = int(input("Please input robot x: "))
            y = int(input("Please input robot y: "))
            robot = r.Robot(name, x, y)
            robot_list.append(robot)
            robot_points.append(axis.plot(x, y, 'o', color='blue')[0])
            robot.ano = axis.annotate(name, xy=(x, y),
                                      xytext=(x, y),
                                      textcoords="data",
                                      )

    else:
        robot_list = []
        for i in range(ROBOT_NUMBER):
            robot_list.append(r.Robot(str(1 + i), random.randint(-N, N), random.randint(-N, N)))

        # print([m.name for m in robot_list], [(m.x, m.y) for m in robot_list])
        robots_x = [i.x for i in robot_list]
        robots_y = [i.y for i in robot_list]

        robot_points = []
        for i in range(len(robot_list)):
            robot_points.append(axis.plot(robots_x[i], robots_y[i], '.', color='red')[0])

        for i in robot_list:
            i.ano = axis.annotate(i.name, xy=(i.x, i.y),
                                  xytext=(i.x, i.y),
                                  textcoords="data",
                                  )
    return robot_list, robot_points


def get_random_robots(robot_points):
    random_robots = []
    for i in range(RANDOM_PICK_NUMBER):
        random_robots.append(random.choice(robot_points))
    return random_robots


def line_update(robot_points, robot_list):
    to_move_positions = []
    for robot in robot_points:
        random_r = get_random_robots(robot_points)
        distance = np.array([], dtype='longlong')
        for i in random_r:
            # get the distance between robot and random robot
            distance = np.append(distance,
                                 ((int(robot.get_xdata()[0])
                                   - int(i.get_xdata()[0])) ** 2 +
                                  (int(robot.get_ydata()[0]) -
                                   int(i.get_ydata()[0])) ** 2))
        # get the indices of minimum distance
        min_indices = np.where(distance == np.amin(distance))
        min_index = np.random.choice(min_indices[0])
        # get the position of minimum distance
        min_position = random_r[min_index].get_xdata(), random_r[min_index].get_ydata()
        to_move_positions.append(min_position)
    # print([m.name for m in robot_list], [m for m in to_move_positions])
    for m in range(len(robot_points)):
        x, y = to_move_positions[m]
        robot_points[m].set_markersize(6.0)
        robot_points[m].set_xdata(x)
        robot_points[m].set_ydata(y)


def is_finished(robot_points):
    for i in range(len(robot_points)):
        if robot_points[i].get_xdata() != robot_points[0].get_xdata() or robot_points[i].get_ydata() != robot_points[0].get_ydata():
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

    # increase the size of point based on the number of robots on that point
    for i in range(len(robot_points)):
        for j in range(i, len(robot_points)):
            if robot_points[i].get_xdata() == robot_points[j].get_xdata() and robot_points[i].get_ydata() == robot_points[j].get_ydata():
                size = robot_points[i].get_markersize()
                robot_points[i].set_markersize(size + 3)
                robot_points[j].set_markersize(size + 3)
    if is_finished(robot_points):
        print("done")
        print(t)
        ani.pause()
    # return robot_points


def move_till_finished(robot_list, robot_points):
    count = 0
    while not is_finished(robot_points):
        count += 1
        line_update(robot_points, robot_list)
        for m in range(len(robot_list)):
            robot_list[m].ano.set_position((robot_points[m].get_xdata(), robot_points[m].get_ydata()))
    return count


def plain_move(robot_list, robot_points):
    n = 0
    lst = []
    while n < 1000:
        count = move_till_finished(robot_list, robot_points)
        n += 1
        # random reset the position of robots
        for i in range(len(robot_points)):
            robot_points[i].set_xdata(np.array([random.randint(-N, N)]))
            robot_points[i].set_ydata(np.array([random.randint(-N, N)]))

        lst.append(count)
        print(n)


    print(lst)
    lst = np.array(lst)
    print("largest", np.amax(lst))
    print("smallest", np.amin(lst))
    print("average: ", np.average(lst))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--manual", help="manual mode", action="store_true")
    args = parser.parse_args()
    fig, axis = create_plain()

    r_list, r_points = create_robots(axis, args.manual)
    print(r_list)
    print(r_points)
    ani = FuncAnimation(fig, update, interval=1000, frames=60, fargs=(r_list, r_points))
    plt.show(block=True)
    # plain_move(r_list, r_points)
