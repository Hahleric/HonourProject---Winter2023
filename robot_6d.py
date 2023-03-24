class Robot_6d:

    def __init__(self, name, x, y, z, t, p, q):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.t = t
        self.p = p
        self.q = q

    def get_name(self):
        return self.name

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def get_t(self):
        return self.t

    def get_p(self):
        return self.p

    def get_q(self):
        return self.q

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_z(self, z):
        self.z = z

    def set_t(self, t):
        self.t = t

    def set_p(self, p):
        self.p = p

    def set_q(self, q):
        self.q = q

    def set_name(self, name):
        self.name = name

    def move_to(self, x, y, z, t, p, q):
        self.set_x(x)
        self.set_y(y)
        self.set_z(z)
        self.set_t(t)
        self.set_p(p)
        self.set_q(q)
