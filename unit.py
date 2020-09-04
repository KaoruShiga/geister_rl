#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Unit:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.taken = False

class OpUnit(Unit):
    def __init__(self, x, y, color, name):
        super().__init__(x, y, color, name)
        self.blue = 0.0