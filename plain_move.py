import numpy
import numpy as np
import mpl_toolkits.axisartist as ax
from numpy import sort

import Robot as r
import random
import matplotlib.pyplot as plt
import matplotlib
import argparse
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
# figure for line, 15*5 is the size of the figure
PLAIN_FIGURE_SIZE = (15, 5)
# number of robots we have in figure
ROBOT_NUMBER = 10
# length of the line
N = 32768
# random pick number
RANDOM_PICK_NUMBER = 2


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

        # set only one robot to Broken
        robot_list[0].set_status(True)

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
    index = 0
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
        if robot_list[index].broken:
            to_move_positions.append((robot.get_xdata(), robot.get_ydata()))
        else:
            to_move_positions.append(min_position)
        index += 1
    # print([m.name for m in robot_list], [m for m in to_move_positions])
    for m in range(len(robot_points)):
        x, y = to_move_positions[m]
        robot_points[m].set_markersize(6.0)
        robot_points[m].set_xdata(x)
        robot_points[m].set_ydata(y)
    to_move_positions = np.array(to_move_positions)
    return len(np.unique(to_move_positions, axis=0))


def is_finished(robot_points):
    for i in range(len(robot_points)):
        if robot_points[i].get_xdata() != robot_points[0].get_xdata() or robot_points[i].get_ydata() != robot_points[
            0].get_ydata():
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
    print("here?")
    # increase the size of point based on the number of robots on that point
    for i in range(len(robot_points)):
        for j in range(i, len(robot_points)):
            if robot_points[i].get_xdata() == robot_points[j].get_xdata() and robot_points[i].get_ydata() == \
                    robot_points[j].get_ydata():
                size = robot_points[i].get_markersize()
                robot_points[i].set_markersize(size + 3)
                robot_points[j].set_markersize(size + 3)

    if is_finished(robot_points):
        print("done")
        print(t)
        ani.pause()
    return robot_points


def move_till_finished(robot_list, robot_points):
    count = 0
    number_of_positions = []
    while not is_finished(robot_points):
        count += 1
        number_of_positions.append(line_update(robot_points, robot_list))

        for m in range(len(robot_list)):
            robot_list[m].ano.set_position((robot_points[m].get_xdata(), robot_points[m].get_ydata()))
    return count, number_of_positions


def plain_move(robot_list, robot_points):
    n = 0
    lst = []
    positions = []
    while n < 1000:
        count, number_of_positions = move_till_finished(robot_list, robot_points)
        n += 1
        # random reset the position of robots
        for i in range(len(robot_points)):
            robot_points[i].set_xdata(np.array([random.randint(-N, N)]))
            robot_points[i].set_ydata(np.array([random.randint(-N, N)]))
        positions.append(number_of_positions)
        lst.append(count)
        print(n)

    print(lst)
    lst = np.array(lst)
    # if the length of the element is smaller than the largest length element, add 2's to the end of the list till it
    # is the same length
    for i in range(len(positions)):
        if len(positions[i]) < len(positions[np.argmax(lst)]):
            positions[i] = np.append(positions[i], np.full(len(positions[np.argmax(lst)]) - len(positions[i]), 1))
    positions = np.array(positions)

    # get average number of positions of robots in each step
    print(positions)
    positions = np.array(positions, dtype='longlong')

    positions = np.mean(positions, axis=0)
    plt.subplot(1, 2, 2)

    lst = sort(lst)
    print(lst)
    plt.plot(lst)
    plt.show(block=False)
    print("largest", np.amax(lst))
    print("smallest", np.amin(lst))
    print("average: ", np.average(lst))
    return np.average(lst)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--manual", help="manual mode", action="store_true")
    args = parser.parse_args()
    fig, axis = create_plain()
    r_list, r_points = create_robots(axis, args.manual)
    print(r_list)
    print(r_points)
    # ani = FuncAnimation(fig, update, interval=1000, frames=300, fargs=(r_list, r_points))
    # writer = PillowWriter(fps=60)
    # ani.save('2d_with_broken_4.gif', writer=writer)
    # t = 0
    # avgs = []
    # while t < 20:
    #     avg = plain_move(r_list, r_points)
    #     avgs.append(avg)
    #     t += 1
    # plt.plot(avgs)
    # plt.show()
    plain_move(r_list, r_points)

