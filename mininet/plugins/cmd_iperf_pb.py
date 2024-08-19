from mininet.log import info, error, debug, output, warn

import random
from time import sleep

cmd = {
    "name": "iperfpb",
    "func_name": "iperfPb",
}


def net(self, bw, l4Type="TCP", period=60, i=1, j=4, k=64, pt=0.5, pa=0.3):
    def random_pick(_list, probabilities):
        x = random.uniform(0, 1)
        p = None
        cumulative_probability = 0.0
        for item, item_probability in zip(_list, probabilities):
            cumulative_probability += item_probability
            p = item
            if x < cumulative_probability:
                break
        return p

    base_port = 5001
    server_list = []
    client_list = []
    client_list = [h for h in self.hosts]
    cli_outs = []
    ser_outs = []
    host_list = []
    host_list = [h for h in self.hosts]
    pc = 1 - pt - pa
    p_list = [pt, pa, pc]
    _len = len(self.hosts)
    for key in range(_len):
        client = host_list[key]
        access_host = [
            host_list[(key + i) % _len],
            host_list[(key + j) % _len],
            host_list[(key + k) % _len],
        ]
        server = random_pick(access_host, p_list)
        server_list.append(server)
        self.iperfSingle(
            hosts=[client, server],
            l4Type=l4Type,
            udpBw=bw,
            period=period,
            port=base_port,
        )
        sleep(0.05)
    sleep(period)
    output("test has done")


def cli(self, line):
    """Multi iperf UDP test with probablity"""
    args = line.split()
    if len(args) == 1:
        udpBw = args[0]
        self.mn.iperfMulti(bw=udpBw, l4Type="UDP")
    elif len(args) == 2:
        udpBw = args[0]
        period = args[1]
        err = False
        self.mn.iperfPb(bw=udpBw, period=float(period), l4Type="UDP")
    else:
        error(
            "invalid number of args: iperpb(TCP version) udpBw period\n"
            + "udpBw examples: 1M 120\n"
        )
