from models.host import Host
from models.switch import Switch


class Network(object):
    switches = []
    hosts = []

    @classmethod
    def get_switch(cls, switch_id):
        for switch in cls.switches:
            if switch.id == switch_id:
                return switch

        switch = Switch(switch_id)
        cls.switches.append(switch)
        return switch

    @classmethod
    def get_hosts(cls):
        return_value = set()
        for switch in cls.switches:
            for port in switch.ports.values():
                if isinstance(port.link.otherside(port).switch, Host):
                    return_value.add(port.link.otherside(port).switch)

        return return_value
