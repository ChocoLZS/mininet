from mininet.log import info, error, debug, output, warn
from mininet.util import waitListening

import random
from time import sleep
import os

cmd = {
    "name": "iperfmulti",
    "func_name": "iperfMulti",
}


def net(self, bw, period=60, l4Type="TCP"):
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
            hosts=[client, server],
            udpBw=bw,
            l4Type=l4Type,
            period=period,
            port=base_port,
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
        self.mn.iperfMulti(
            bw=udpBw,
            l4Type="UDP",
        )
    elif len(args) == 2:
        udpBw = args[0]
        period = args[1]
        err = False
        self.mn.iperfMulti(bw=udpBw, l4Type="UDP", period=float(period))
    else:
        error(
            "invalid number of args: iperfmulti(UDP version) udpBw period\n"
            + "udpBw examples: 1M 120\n"
        )


def iperfSingle(self, hosts=None, l4Type="TCP", udpBw="10M", period=5, port=5001):
    """
    Run iperf between two hosts using UDP.
    hosts: list of hosts; if None, uses opposite hosts
    returns: results two-element array of server and client speeds
    """
    if not hosts:
        return
    else:
        assert len(hosts) == 2
    client, server = hosts
    filename = client.name[1:] + ".out"
    output("*** Iperf: testing bandwidth between ")
    output("%s and %s\n" % (client.name, server.name))
    iperfArgs = "iperf -p %d " % port
    bwArgs = ""
    if l4Type == "UDP":
        iperfArgs += "-u "
        bwArgs = "-b " + udpBw + " "
    elif l4Type != "TCP":
        raise Exception("Unexpected l4 type: %s" % l4Type)
    info("***start server***")
    os.makedirs("/tmp/mininet/log/", exist_ok=True)
    server.cmd(
        iperfArgs
        + "-s -i 1"
        + " > /tmp/mininet/log/"
        + "server"
        + server.name[1:]
        + ".out"
        + "&"
    )
    info("***start client***")
    if l4Type == "TCP":
        if not waitListening(client, server.IP(), port):
            raise Exception("Could not connect to iperf on port %d" % port)
    client.cmd(
        iperfArgs
        + "-t "
        + str(period)
        + " -c "
        + server.IP()
        + " "
        + bwArgs
        + " > /tmp/mininet/log/"
        + "client"
        + filename
        + "&"
    )
