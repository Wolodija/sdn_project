import random


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

    def get_stats(self):
        print("refresh stats")
        # return random.randint(0, 600)
        #
        new_stats = {
            'receiveBytes': 0,
        }
        old_stats = {
            'receiveBytes': 0,
        }

        from models.network import Network
        for port in Network.new_stats.get(self.switch.id).get('port_reply', [dict()])[0].get('port', []):
            if port['portNumber'] == self.id:
                new_stats = port

        for port in Network.old_stats.get(self.switch.id).get('port_reply', [dict()])[0].get('port', []):
            if port['portNumber'] == self.id:
                old_stats = port

        print("return stats")
        return int(new_stats['receiveBytes']) - int(old_stats['receiveBytes'])
