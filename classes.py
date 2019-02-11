class Message:
    def __init__(self, code, data):
        self.code = code
        self.data = data

    def __str__(self):
        return "Code: {}, Data: {}".format(self.code, self.data)

    def to_send(self):
        return "{},{}".format(self.code, self.data)


class Position:
    def __init__(self, x=None, y=None, angle=None):
        self.x = x
        self.y = y
        self.angle = angle

    def get_position(self):
        if self.x is None:
            return None
        return self.x, self.y, self.angle

    def set_position(self, position):
        self.x = position[0]
        self.y = position[1]
        self.angle = position[2]
        return

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x
        return

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y
        return

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        self.angle = angle
        return

    def is_none(self):
        return self.x is None and self.y is None and self.angle is None


class Player:
    def __init__(self, p_id):
        self._p_id = p_id
        self._pos = Position()
        self._health = 30
        self._alive = True

    def get_position(self):
        return self._pos.get_position()

    def get_string_position(self):
        pos = self._pos.get_position()
        if pos is None:
            return "None"
        return str(pos[0]) + "," + str(pos[1]) + "," + str(pos[2])

    def set_position(self, new_pos):
        self._pos.set_position(new_pos)
        return

    def get_angle(self):
        if not self._pos.is_none():
            return self._pos.get_angle()
        return None

    def set_angle(self, angle):
        if not self._pos.is_none():
            self._pos.set_angle(angle)
        return

    def get_x(self):
        if not self._pos.is_none():
            return self._pos.get_x()
        return None

    def set_x(self, x):
        if not self._pos.is_none():
            self._pos.set_x(x)
        return

    def get_y(self):
        if not self._pos.is_none():
            return self._pos.get_y()
        return None

    def set_y(self, y):
        if not self._pos.is_none():
            self._pos.set_y(y)
        return

    def delta_x(self, delta_x):
        self.set_x(self.get_x() + delta_x)
        return

    def delta_y(self, delta_y):
        self.set_y(self.get_y() + delta_y)
        return

    def get_health(self):
        return self._health

    def set_health(self, new_health):
        self._health = new_health
        print self._health
        if self._health <= 0:
            self.died()
            return True
        return False

    def is_alive(self):
        return self._alive

    def died(self):
        self._pos.set_position((None, None, None))
        self._alive = False
        return

    def get_p_id(self):
        return self._p_id


class Game:
    def __init__(self, pid, player):
        self._pid = pid
        self._player = player
        self._player_positions = []
        self._bullets = []
        self._collectibles = []
        self._messages = []
        self._shot = 0
        self._keys = [False, False, False, False]
        self._dead = False
        self._new = False

    def get_player(self):
        return self._player

    def set_player(self, player):
        self._player = player
