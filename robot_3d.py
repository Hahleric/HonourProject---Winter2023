class Robot_3d:

    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

    def get_name(self):
        return self.name

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_z(self, z):
        self.z = z

    def set_name(self, name):
        self.name = name

    def move_to(self, x, y, z):
        self.set_x(x)
        self.set_y(y)
        self.set_z(z)
