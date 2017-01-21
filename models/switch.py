from models.port import Port


class Switch(object):
    def __init__(self, id):
        self.id = id
        self.ports = {}

    def get_port(self, id):
        try:
            return self.ports[id]
        except:
            Port(self, id)
            return self.ports[id]
