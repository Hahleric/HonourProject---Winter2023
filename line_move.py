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

# figure for line, 15*5 is the size of the figure
LINE_FIGURE_SIZE = (15, 5)
# number of robots we have in figure
ROBOT_NUMBER = 20
# length of the line
N = 32768
# random pick number
RANDOM_PICK_NUMBER = 3
# manually set the position of robots
MANUAL_POSITION = True

# creating an x-axis
fig = plt.figure(figsize=LINE_FIGURE_SIZE)
ind = np.arange(N)
axis = ax.Subplot(fig, 111)
axis.axis[:].set_visible(False)
fig.add_axes(axis)
axis.axis["x"] = axis.new_floating_axis(0, 0, axis_direction="bottom")
plt.xlim(-N, N)

# create robots based on numbers, add their x and y to a list
if MANUAL_POSITION:
    robot_list = []
    x_lst = [i for i in range(ROBOT_NUMBER)]
    for i in range(ROBOT_NUMBER):
        # name = input("Please input robot name: ")
        # x = int(input("Please input robot x: "))
        # x_lst.append(x)
        y = 0
        robot = r.Robot(x_lst[i], x_lst[i], y)
        robot_list.append(robot)
else:
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
    for m in range(len(robot_p)):
        x, y = to_move_positions[m]
        robot_p[m].set_markersize(6.0)
        robot_p[m].set_xdata(x)
        robot_p[m].set_ydata(y)


def is_finished(robot_points):
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
            if robot_points[i].get_xdata() == robot_points[j].get_xdata() and robot_points[i].get_ydata() == \
                    robot_points[j].get_ydata():
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

def move_till_finished(robot_list, robot_points):
    count = 0
    while not is_finished(robot_points):
        count += 1
        line_update(robot_points, robot_list)
        for m in range(len(robot_list)):
            robot_list[m].ano.set_position((robot_points[m].get_xdata(), robot_points[m].get_ydata()))
    final_position = robot_points[0].get_xdata()
    return count, final_position


def plain_move(robot_list, robot_points):
    n = 0
    lst = []
    positions = []
    original_list = robot_list.copy()
    original_poinrts = robot_points.copy()
    while n < 10000:
        count, final_position = move_till_finished(robot_list, robot_points)
        n += 1
        # random reset the position of robots
        if MANUAL_POSITION:
            for i in range(len(robot_points)):
                robot_points[i].set_xdata(np.array([x_lst[i]]))
        else:
            for i in range(len(robot_points)):
                robot_points[i].set_xdata(np.array([random.randint(-N, N)]))
                robot_points[i].set_ydata(np.array([random.randint(-N, N)]))
        positions.append(final_position)
        lst.append(count)
        print(n)

    print(lst)
    lst = np.array(lst)
    # count the count of integers in positions are between 0 and 6
    in_range_count = 0
    in_range_positions = []
    for i in range(len(positions)):
        if 0 <= positions[i] <= 7:
            in_range_count += 1
            in_range_positions.append(positions[i])

    # # if the length of the element is smaller than the largest length element, add 2's to the end of the list till it is the same length
    # for i in range(len(positions)):
    #     if len(positions[i]) < len(positions[np.argmax(lst)]):
    #         positions[i] = np.append(positions[i], np.full(len(positions[np.argmax(lst)]) - len(positions[i]), 1))
    # positions = np.array(positions)

    # get average number of positions of robots in each step
    # print(positions)
    # positions = np.array(positions, dtype='longlong')

    # positions = np.mean(positions, axis=0)
    # plt.subplot(1, 2, 2)
    # plt.plot(positions)
    # plt.show(block=False)
    # print(positions)
    print("number of picks", RANDOM_PICK_NUMBER)
    print("largest iteration number", np.amax(lst))
    print("smallest iteration number", np.amin(lst))
    print("average iterations to gather: ", np.average(lst))
    print("starting positions: ", x_lst)
    print("average of starting positions", np.average(x_lst))
    print("avarage of final positions: ", np.average(positions))
    print("how many final positions are in range(0, 7): ", in_range_count)
    print("average of final positions in range(0, 7): ", np.average(in_range_positions))
    # print all number of points landing on each position
    for i in range(ROBOT_NUMBER):
        print("number of times position", i, "is landed on: ", positions.count(i))

    point_counts = [positions.count(i) for i in range(ROBOT_NUMBER)]
    plt.subplot(1, 2, 2)
    plt.plot(point_counts)
    plt.show(block=False)


plain_move(robot_list, robot_points)
