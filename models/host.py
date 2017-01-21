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

        start_port = self.ports[0].link.otherside(self.ports[0])
        start_switch = start_port.switch

        for port in start_switch.ports.values():
            if port != start_port and port.link.otherside(port).switch not in {self}:
                out_port = port
                break

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
            if port.link.otherside(port).switch == host:
                out_port2 = port

        self.return_value.append({
            "switch": start_switch2,
            "in_port": start_port2,
            "out_port": out_port2
        })


        start_port3 = out_port2.link.otherside(out_port2)
        start_switch3 = start_port3.switch

        if start_switch3 == host:
            return self.return_value

        out_port3 = None
        for port in start_switch3.ports.values():
            if not out_port3 and port != start_port3 and port.link.otherside(port).switch not in {self, start_switch, start_switch2}:
                out_port3 = port
            if port.link.otherside(port).switch == host:
                out_port3 = port

        self.return_value.append({
            "switch": start_switch3,
            "in_port": start_port3,
            "out_port": out_port3
        })

        start_port4 = out_port3.link.otherside(out_port3)
        start_switch4 = start_port4.switch

        if start_switch4 == host:
            return self.return_value

        out_port4 = None
        for port in start_switch4.ports.values():
            if not out_port4 and port != start_port4 and port.link.otherside(port).switch not in {self, start_switch, start_switch2,
                                                                                start_switch3}:
                out_port4 = port
                break
            if port.link.otherside(port).switch == host:
                out_port4 = port

        self.return_value.append({
            "switch": start_switch4,
            "in_port": start_port4,
            "out_port": out_port4
        })

        start_port5 = out_port4.link.otherside(out_port4)
        start_switch5 = start_port5.switch

        for port in start_switch5.ports.values():
            if port != start_port5 and port.link.otherside(port).switch not in {self, start_switch, start_switch2,
                                                                                start_switch3, start_switch4}:
                out_port5 = port
            if port.link.otherside(port).switch == host:
                out_port5 = port

        self.return_value.append({
            "switch": start_switch5,
            "in_port": start_port5,
            "out_port": out_port5
        })

        start_port6 = out_port5.link.otherside(out_port5)
        start_switch6 = start_port6.switch

        for port in start_switch6.ports.values():
            if port != start_port6 and port.link.otherside(port).switch not in {self, start_switch, start_switch2,
                                                                                start_switch3, start_switch4,
                                                                                start_switch5}:
                out_port6 = port
            if port.link.otherside(port).switch == host:
                out_port6 = port

        self.return_value.append({
            "switch": start_switch6,
            "in_port": start_port6,
            "out_port": out_port6
        })

        start_port7 = out_port6.link.otherside(out_port6)
        start_switch7 = start_port7.switch

        for port in start_switch7.ports.values():
            if port != start_port7 and port.link.otherside(port).switch not in {self, start_switch, start_switch2,
                                                                                start_switch3, start_switch4,
                                                                                start_switch5, start_switch6}:
                out_port7 = port
                break

        self.return_value.append({
            "switch": start_switch7,
            "in_port": start_port7,
            "out_port": out_port7
        })

        return self.return_value