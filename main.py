import requests
import tornado.ioloop
import tornado.web

#192.168.56.1:8080/wm/staticflowpusher/list/all/json
#192.168.56.1:8080//wm/topology/links/json
#192.168.56.1:8080/wm/core/controller/switches/json
from models.floodlight import Floodlight
from models.network import Network


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
            # Floodlight.get_aggregats()
        # try:
            Network.switches = Floodlight.get_switches()
            Floodlight.get_ports(Network.switches)
            result = self.request.body.decode()
            msg_type = result[0:3]

            if msg_type in ("ICM", "ARP"):
                Floodlight.get_hosts(Network.switches)
                sender_hw, dst_mac, sender, dst_ip, in_port, switch_id = result[3:].split(";")
                switch = Network.get_switch(switch_id)
                port = switch.get_port(int(in_port))
                ether_type = 0x0800

                host = port.link.otherside(port).switch
                for host_ in Network.hosts:
                    if host_.ip == dst_ip:
                        dst_host = host_

                path = host.get_path_to_host(dst_host)

                for row in path:
                    data = {
                        "name": "ICMP: {0} {1} to {2}".format(row['switch'].id, sender_hw, dst_mac),
                        "switch": row['switch'].id,
                        "active": "true",
                        "eth_type": ether_type,
                        "in_port": str(row['in_port'].id),
                        "cookie": 0,
                        "priority": 40,
                        "ipv4_dst": dst_ip,
                        "ipv4_src": sender,
                        "ip_proto": 0x01,
                        "idle_timeout": 10,
                        "actions": "output={0}".format(row['out_port'].id)
                    }

                    requests.post("http://localhost:8080/wm/staticflowpusher/json", json=data)

                    data = {
                        "name": "ARP: {0} {1} to {2}".format(row['switch'].id, sender_hw, dst_mac),
                        "switch": row['switch'].id,
                        "active": "true",
                        "in_port": str(row['in_port'].id),
                        "eth_type": 0x0806,
                        "cookie": 0,
                        "priority": 30,
                        "idle_timeout": 10,
                        "actions": "output={0}".format(row['out_port'].id)
                    }

                    requests.post("http://localhost:8080/wm/staticflowpusher/json", json=data)

                    data = {
                        "name": "ICMP: {0} {1} to {2}".format(row['switch'].id, dst_mac, sender_hw),
                        "switch": row['switch'].id,
                        "active": "true",
                        "eth_type": ether_type,
                        "in_port": str(row['out_port'].id),
                        "cookie": 0,
                        "priority": 40,
                        "ipv4_dst": sender,
                        "ipv4_src": dst_ip,
                        "ip_proto": 0x01,
                        "idle_timeout": 10,
                        "actions": "output={0}".format(row['in_port'].id)
                    }

                    requests.post("http://localhost:8080/wm/staticflowpusher/json", json=data)

                    data = {
                        "name": "ARP: {0} {1} to {2}".format(row['switch'].id, dst_mac, sender_hw),
                        "switch": row['switch'].id,
                        "active": "true",
                        "in_port": str(row['out_port'].id),
                        "eth_type": 0x0806,
                        "cookie": 0,
                        "priority": 30,
                        "idle_timeout": 10,
                        "actions": "output={0}".format(row['in_port'].id)
                    }

                    requests.post("http://localhost:8080/wm/staticflowpusher/json", json=data)

            elif msg_type in ("IP4", ):
                Floodlight.get_hosts(Network.switches)
                sender, dst_ip, src_port, dst_port, in_port, switch_id = result[3:].split(";")
                switch = Network.get_switch(switch_id)
                port = switch.get_port(int(in_port))
                ether_type = 0x0800

                host = port.link.otherside(port).switch
                for host_ in Network.hosts:
                    if host_.ip == dst_ip:
                        dst_host = host_

                path = host.get_path_to_host(dst_host)

                for row in path:
                    data = {
                        "name": "IPv4: {0} {1}:{2} to {3}:{4}".format(row['switch'].id, sender, src_port,
                                                                      dst_ip, dst_port),
                        "switch": row['switch'].id,
                        "active": "true",
                        "eth_type": ether_type,
                        "in_port": str(row['in_port'].id),
                        "cookie": 0,
                        "priority": 40,
                        "ipv4_dst": dst_ip,
                        "ipv4_src": sender,
                        "ip_proto": 0x06,
                        "tcp_src": src_port,
                        "tcp_dst": dst_port,
                        "idle_timeout": 10,
                        "actions": "output={0}".format(row['out_port'].id)
                    }

                    requests.post("http://localhost:8080/wm/staticflowpusher/json", json=data)

                    data = {
                        "name": "IPv4: {0} {1}:{2} to {3}:{4}".format(row['switch'].id, dst_ip, dst_port, sender,
                                                                      src_port),
                        "switch": row['switch'].id,
                        "active": "true",
                        "eth_type": ether_type,
                        "in_port": str(row['out_port'].id),
                        "cookie": 0,
                        "priority": 40,
                        "ipv4_dst": sender,
                        "ipv4_src": dst_ip,
                        "ip_proto": 0x06,
                        "tcp_src": dst_port,
                        "tcp_dst": src_port,
                        "idle_timeout": 10,
                        "actions": "output={0}".format(row['in_port'].id)
                    }

                    requests.post("http://localhost:8080/wm/staticflowpusher/json", json=data)
            else:
                print("new")



def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":

    app = make_app()
    app.listen(4444)
    Network.switches = Floodlight.get_switches()
    Floodlight.get_ports(Network.switches)
    Floodlight.get_aggregats()
    Floodlight.get_aggregats()
    tornado.ioloop.IOLoop.current().start()