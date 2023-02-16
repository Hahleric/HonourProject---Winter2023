import robot_3d as r
import random
import numpy as np
import argparse

ROBOT_NUMBER = 100
# length of the line
N = 32768
# random pick number
RANDOM_PICK_NUMBER = 5


def create_robots(manual):
    robot_list = []
    for i in range(ROBOT_NUMBER):
        if manual:
            name = input("name: ")
            x = int(input("x: "))
            y = int(input("y: "))
            z = int(input("z: "))
        else:
            name = "robot_" + str(i)
            x = random.randint(-N, N)
            y = random.randint(-N, N)
            z = random.randint(-N, N)
        robot = r.Robot_3d(name, x, y, z)
        robot_list.append(robot)
    return robot_list


def get_random_robots(robot_list):
    random_robots = []
    for i in range(RANDOM_PICK_NUMBER):
        random_robots.append(random.choice(robot_list))
    return random_robots


def line_update(robot_list):
    to_move_positions = []
    for robot in robot_list:
        random_r = get_random_robots(robot_list)
        distance = np.array([], dtype='longlong')
        for i in random_r:
            # get the distance between robot and random robot
            distance = np.append(distance,
                                 ((int(robot.get_x())
                                   - int(i.get_x())) ** 2 +
                                  (int(robot.get_y())
                                   - int(i.get_y())) ** 2 +
                                  (int(robot.get_z())
                                   - int(i.get_z())) ** 2))
        # print(distance)
        min_indices = np.where(distance == np.amin(distance))
        # get the robot with the shortest distance
        min_index = np.argmin(min_indices)
        min_position = random_r[min_index].get_x(), random_r[min_index].get_y(), random_r[min_index].get_z()
        to_move_positions.append(min_position)
    for i in range(len(robot_list)):
        robot_list[i].move_to(to_move_positions[i][0], to_move_positions[i][1], to_move_positions[i][2])


def is_finished(robot_points):
    for i in range(len(robot_points)):
        if robot_points[i].get_x() != robot_points[0].get_x() or \
                robot_points[i].get_y() != robot_points[0].get_y() or \
                robot_points[i].get_z() != robot_points[0].get_z():
            return False
    return True


def move_till_finished(robot_l):
    count = 0
    while not is_finished(robot_l):
        count += 1
        line_update(robot_l)
    return count


def plain_move(robot_list):
    n = 0
    lst = []
    while n < 1000:
        count = move_till_finished(robot_list)
        n += 1
        # random reset the position of robots
        for i in range(len(robot_list)):
            robot_list[i].set_x(np.array([random.randint(-N, N)]))
            robot_list[i].set_y(np.array([random.randint(-N, N)]))
            robot_list[i].set_z(np.array([random.randint(-N, N)]))

        lst.append(count)
        print(n)


    print(lst)
    lst = np.array(lst)
    print("largest", np.amax(lst))
    print("smallest", np.amin(lst))
    print("average: ", np.average(lst))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--manual", help="manual input", action="store_true")
    args = parser.parse_args()
    robot_list = create_robots(args.manual)
    plain_move(robot_list)
