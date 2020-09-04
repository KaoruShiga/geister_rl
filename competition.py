#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import socket
import random
import geister
import execute
import argparse
import logging
import sys
import cProfile
# import numba

# @numba.jit
def match(first, second, logEnable, outputLevel, matchCount):
    results = []
    for cnt in range(matchCount):
        # first.send("init")
        # second.send("init")
        game = geister.Geister()
        red1 = first.send("red")#.upper()
        game.setRed(red1)
        game.changeSide()
        red2 = second.send("red")#.lower()
        game.setRed(red2)
        game.changeSide()
        if outputLevel > 2:
            game.printBoard()
        result = 0
        while result == 0:
            if outputLevel > 2:
                game.printBoard()
            msg = 'hand {}'.format(game.toString())
            hand = ''
            while hand == '':
                hand = first.send(msg)
            if outputLevel > 1:
                print('Hand,0,{}'.format(hand))
            unit, direct = hand.split(',')
            game.move(unit[0], direct[0])
            if outputLevel > 2:
                game.printBoard()
            result = game.checkResult()
            if(result):
                break
            game.changeSide()
            msg = 'hand {}'.format(game.toString())
            hand = ''
            while hand == '':
                hand = second.send(msg)
            if outputLevel > 1:
                print('Hand,1,{}'.format(hand))
            game.move(hand[0], hand[4])
            game.changeSide()
            result = game.checkResult()
        if outputLevel > 0:
            print("{}: {}".format(cnt, result))
        results.append(result)
    return results


parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')

parser.add_argument('player1')
parser.add_argument('player2')
parser.add_argument('-c', '--count', type=int, default=1)
parser.add_argument('-o', '--output', type=int, default=2, choices=[0,1,2,3])
parser.add_argument('-v', '--version')
parser.add_argument('-l', '--log', action='store_true')
if __name__ == "__main__":
    args = parser.parse_args()
    first = execute.Execute([args.player1])
    second = execute.Execute([args.player2])
    # print("1st {}".format(first.recieve()))
    # print("2nd {}".format(second.recieve()))
    results = match(first, second, logEnable=args.log, outputLevel=args.output, matchCount=args.count)
    # print(results)
    resultList = {1:0,2:0,3:0,-1:0,-2:0,-3:0,0:0}
    for r in results:
        resultList[r] += 1
    print(resultList)
    first.send("exit")
    second.send("exit")
