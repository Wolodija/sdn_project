import json

import requests
from models.host import Host
from models.link import Link
from models.network import Network
from models.port import Port
from models.switch import Switch


class Floodlight(object):
    old_stats = None
    new_stats = None

    @classmethod
    def get_switches(cls):
        result = requests.get('http://localhost:8080/wm/core/controller/switches/json')
        json_data = json.loads(result.text)

        return_value = []
        for switch in json_data:
            return_value.append(Switch(switch['switchDPID']))

        return return_value

    @classmethod
    def get_ports(cls, switches):
        result = requests.get('http://localhost:8080/wm/topology/links/json')
        json_data = json.loads(result.text)

        for link in json_data:
            for switch in switches:
                if switch.id == link['src-switch']:
                    src_port = Port(switch, int(link['src-port']))

                if switch.id == link['dst-switch']:
                    dst_port = Port(switch, int(link['dst-port']))
            Link(src_port, dst_port)

    @classmethod
    def get_hosts(self, switches):
        Network.hosts = []
        result = requests.get('http://localhost:8080/wm/device/')
        json_data = json.loads(result.text)

        return_value = []
        for host in json_data:
            if len(host['attachmentPoint']) != 1:
                continue
            app_host = Host()
            try:
                app_host.mac = host['mac'][0]
            except Exception:
                pass
            try:
                app_host.ip = host['ipv4'][0]
            except Exception:
                pass

            port = Port(app_host, 0)

            for switch in switches:
                if switch.id == host['attachmentPoint'][0]['switchDPID']:
                    # if host['attachmentPoint'][0]['port'] in switch.ports.keys():
                    #     break
                    new_port = Port(switch, host['attachmentPoint'][0]['port'])

                    Link(port, new_port)

            Network.hosts.append(app_host)

    @classmethod
    def get_aggregats(cls):
        Network.hosts = []
        result = requests.get('http://localhost:8080/wm/core/switch/all/port/json')
        json_data = json.loads(result.text)

        Network.old_stats = Network.new_stats
        Network.new_stats = json_data
