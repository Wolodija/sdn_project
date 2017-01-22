class Host(object):
    def __init__(self):
        self.mac = None
        self.ipv4 = None
        self.ports = {}

    @property
    def id(self):
        return self.mac

    def get_path_to_host(self, host):
        self.switches = set()
        self.return_value = []
        from models.floodlight import Floodlight
        Floodlight.get_aggregats()

        start_port = self.ports[0].link.otherside(self.ports[0])
        end_port = host.ports[0].link.otherside(host.ports[0])

        start_switch = start_port.switch
        end_switch = end_port.switch

        stats = -1

        for port in start_switch.ports.values():
            if port != start_port and port.link.otherside(port).switch not in {self}:
                if stats == -1 or port.get_stats() < stats:
                    out_port = port
                    stats = port.get_stats()

        self.return_value.append({
            "switch": start_switch,
            "in_port": start_port,
            "out_port": out_port
        })

        start_port2 = out_port.link.otherside(out_port)
        start_switch2 = start_port2.switch

        if start_switch2 == host:
            return self.return_value

        out_port2 = None
        for port in start_switch2.ports.values():
            if not out_port2 and port != start_port2 and port.link.otherside(port).switch not in {self, start_switch}:

                out_port2 = port
            if port.link.otherside(port).switch == end_switch:
                out_port2 = port
                end_in_port = port.link.otherside(port)


        self.return_value.append({
            "switch": start_switch2,
            "in_port": start_port2,
            "out_port": out_port2
        })

        self.return_value.append({
            "switch": end_switch,
            "in_port": end_in_port,
            "out_port": end_port
        })

        return self.return_value
