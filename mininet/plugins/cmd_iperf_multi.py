from mininet.log import info, error, debug, output, warn

import random
from time import sleep

cmd = {
    "name": "iperfmulti",
    "func_name": "iperfMulti",
}


def net(self, bw, period=60):
    base_port = 5001
    server_list = []
    client_list = [h for h in self.hosts]
    host_list = []
    host_list = [h for h in self.hosts]

    cli_outs = []
    ser_outs = []

    _len = len(host_list)
    for i in range(0, _len):
        client = host_list[i]
        server = client
        while server == client:
            server = random.choice(host_list)
        server_list.append(server)
        self.iperfSingle(
            hosts=[client, server], udpBw=bw, period=period, port=base_port
        )
        sleep(0.05)
        base_port += 1

    sleep(period)
    info("test has done")


def cli(self, line):
    """Multi iperf UDP test between nodes"""
    args = line.split()
    if len(args) == 1:
        udpBw = args[0]
        self.mn.iperfMulti(udpBw)
    elif len(args) == 2:
        udpBw = args[0]
        period = args[1]
        err = False
        self.mn.iperfMulti(udpBw, float(period))
    else:
        error(
            "invalid number of args: iperfmulti udpBw period\n"
            + "udpBw examples: 1M 120\n"
        )
