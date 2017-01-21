class Port(object):
    def __init__(self, switch, port):
        """

        :param switch(Switch):
        :param port(int):
        :return:

        """
        self.switch = switch
        self.id = port
        self.switch.ports[port] = self
        self.link = None
