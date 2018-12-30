class Message:
    def __init__(self, code, data):
        self.code = code
        self.data = data

    def __str__(self):
        return "Code: {}, Data: {}".format(self.code, self.data)

    def to_send(self):
        return "{},{}".format(self.code, self.data)


class Player:
    def __init__(self, p_id):
        self._p_id = p_id
        self._pos = None
        self._health = 30

    def get_position(self):
        return self._pos

    def set_position(self, new_pos):
        self._pos = new_pos
        return

    def get_angle(self):
        if self._pos is not None:
            return self._pos[2]
        return None

    def set_angle(self, angle):
        if self._pos is not None:
            self._pos[2] = angle
        return

    def get_health(self):
        return self._health

    def set_position(self, new_health):
        self._health = new_health
        return


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
