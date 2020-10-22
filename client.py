#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import random
import argparse
import tcpClient


def run(player, port, host="localhost"):
    cl = tcpClient.Client(host, port)

    red = "SET:" + str(player.init_red()) + "\r\n"
    print(red)
    cl.send(red.encode('utf-8'))

    res = b""

    while res[0:3] != b"MOV":
        try:
            res = cl.recv()
        except Exception:
            cl.close()
            cl.reconnect()
            cl.send(b"SET:ABCD\r\n")

    while res[0:3] != b"WON" and res[0:3] != b"LST" and res[0:3] != b"DRW":
        # MOV?99r99r50R54R99b01B99b99b99r55u99r04u99b99b99b00u
        # 脱出した駒がrかbになってしまう現象は仕様．異論は認める．

        print(res[4:4+3*8].upper() + res[4+3*8:])
        hand = player.get_hand(res[4:4+3*8].upper() + res[4+3*8:])
        print(hand)
        cl.move(hand[0], hand[1])
        res = cl.recv()
        while res[0:3] != b"MOV":
            res = cl.recv()
            if res[0:3] == b"WON" or res[0:3] == b"LST" or res[0:3] == b"DRW":
                break
    score = {"WON": 1, "LST": 0, "DRW": 0.1}
    return score[res[0:3].decode()]


# for # DEBUG:
class CmdPlayer:
    def init_red(self):
        return "ABCD"

    def get_hand(self, opp):
        print(opp)
        return ["A", "N"]


if __name__ == "__main__":
    port = 10000
    player = RndPlayer([args.player])
    run(player, port)
