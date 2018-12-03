class Message:
    def __init__(self, code, data):
        self.code = code
        self.data = data

    def __str__(self):
        return "Code: {}, Data: {}".format(self.code, self.data)

    def to_send(self):
        return "{},{}".format(self.code, self.data)
