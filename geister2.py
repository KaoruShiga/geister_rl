# added by Kaoru Shiga
import copy
import _pickle as cPickle
from geister import Geister


class Geister2(Geister):
    def __init__(self, info=None):
        self._turn = 0
        if info is None:
            super().__init__()
        else:
            super().__init__(info)

    # raise error. and change direct: d=0:'E', d=1:'S', d=2:'W', d=3:'N'
    def move(self, i, direct):
        self.history.append("{}{},{}".format(i, direct, self.toString()))
        if not (0 <= i < 8):
            raise NameError("i is not valid. i = " + str(i))
        self._turn += 1
        targetIndex = i
        x, y = self.units[targetIndex].x, self.units[targetIndex].y
        if(direct == 0):
            x += 1
        elif(direct == 1):
            y += 1
        elif(direct == 2):
            x -= 1
        elif(direct == 3):
            y -= 1
        else:
            raise NameError("direction is not valid. direct = " + str(direct))
        for i in range(16):
            if self.units[i].x == x and self.units[i].y == y:
                self.units[i].x, self.units[i].y = 9, 9
        self.units[targetIndex].x, self.units[targetIndex].y = x, y
        if x == -1 or x == 6:
            self.units[targetIndex].x, self.units[targetIndex].y = 8, 8

    # d: 0->3, 1->0, 2->2, 3->1
    # so, d=0:'E', d=1:'S', d=2:'W', d=3:'N'
    def legalMoves(self):
        colorField = [[None] * 6 for _ in range(6)]
        for u in [u for u in self.units if u.x < 6]:
            colorField[u.y][u.x] = u.color
        legalMoves = [(i, d) for i, u in [(i, u) for i, u in enumerate(self.units[0:8]) if u.x < 6] for d in range(4) if (d != 3 or u.y != 0) and (d != 1 or u.y != 5) and (d != 0 or u.x != 5 or (u.y == 0 and u.color == 0)) and (d != 2 or u.x != 0 or u.y == 0 and u.color == 0) and (
            d == 0 and ((u.x == 5 and u.y == 0 and u.color == 0) or u.x != 5 and (colorField[u.y][u.x + 1] == None or colorField[u.y][u.x + 1] % 2))
            or d == 2 and (u.x == 0 and u.y == 0 and u.color == 0 or u.x != 0 and (colorField[u.y][u.x - 1] == None or colorField[u.y][u.x - 1] % 2))
            or d == 3 and (colorField[u.y - 1][u.x] == None or colorField[u.y - 1][u.x] % 2)
            or d == 1 and (colorField[u.y + 1][u.x] == None or colorField[u.y + 1][u.x] % 2)
        )]
        return legalMoves

    def setState(self, state):
        self.state = state.decode()
        for i in range(16):
            self.units[i].x = int(self.state[i * 3])
            self.units[i].y = int(self.state[i * 3 + 1])
            self.units[i].color = Geister.colorIndex[self.state[i * 3 + 2]]
            if int(self.state[i * 3 + 1]) > 5:
                self.units[i].taken = True
                continue

    def on_action_number_received(self, index):
        moves = self.legalMoves()
        move = moves[index]
        i, dir = move
        self.move(i, dir)

    "side_list[0, 1] is the number of taken blue,red owned by the opponent"
    "side_list[2, 3] is the number of taken blue,red owned by the observer"
    "side_list[4, 5] is take_flg,exit_flg"
    def crr_state(self):
        crr_state = [[0 for _ in range(6*7)] for _ in range(3)]
        side_list = [0, 0, 0, 0, 0, 0]
        for unit in self.units:
            # colorIndex = {'B': 0, 'b': 1, 'R': 2, 'r':3} 大文字は味方
            if unit.x == 9 and unit.y == 9:  # 取られた駒
                if unit.color == 0:    # BLUE(味方の青)
                    side_list[2] += 1
                if unit.color == 2:    # RED(味方の赤)
                    side_list[3] += 1
                if unit.color == 1:    # b(敵の青)
                    side_list[0] += 1
                if unit.color == 3:    # r(敵の赤)
                    side_list[1] += 1
            elif unit.x == 8 and unit.y == 8:   # 脱出駒
                side_list[5] = 1
            elif unit.color == 0:    # BLUE(味方の青)
                crr_state[0][unit.x+6*unit.y] = 1
            elif unit.color == 2:    # RED(味方の赤)
                crr_state[1][unit.x+6*unit.y] = 1
            else:                    # 敵駒
                crr_state[2][unit.x+6*unit.y] = 1
        for i in range(len(side_list)):
            side_num = side_list[i]
            if side_num > 0:
                if side_num > 3:
                    print("side_list's element is over 4, side_list=", side_list)
                crr_state[side_num-1][6*6 + i] = 1
        return crr_state

    def after_states(self):
        crr_state = self.crr_state()
        moves = self.legalMoves()
        dst = []
        for move in moves:
            i, d = move                        # N:d=0, E:d=1, S:d=3, W:d=2
            # copy(crr_state) の速度を向上させたもの
            state = cPickle.loads(cPickle.dumps(crr_state, -1))
            unit = self.units[i]
            x, y = unit.x, unit.y
            color = 1 if (unit.color == 0) else (      # BLUE(味方の青)
                    2 if (unit.color == 2) else "n")   # RED(味方の赤)
            state[color-1][x+y*6] = 0
            if(d == 0):    # 'E'
                x += 1
            elif(d == 1):  # 'S'
                y += 1
            elif(d == 2):  # 'W'
                x -= 1
            elif(d == 3):  # 'N'
                y -= 1
            if x == -1 or x == 6:           # exit_flg
                state[0][6*6 + 5] = 1
            elif state[2][x+y*6] == 1:        # take_flg
                state[0][6*6 + 4] = 1
                state[2][x+y*6] = 0
                state[color-1][x+y*6] = 1
            else:
                state[color-1][x+y*6] = 1
            dst.append(state)
        return dst

    def init_states(self):
        arrs = []
        for x in range(8):
            arr = [1, 1, 1, 1, 1, 1, 1, 1]
            arr[x] = 2
            for y in range(x+1, 8):
                arr[y] = 2
                for z in range(y+1, 8):
                    arr[z] = 2
                    for t in range(z+1, 8):
                        arr[t] = 2
                        arrs.append(arr.copy())
                        arr[t] = 1
                    arr[z] = 1
                arr[y] = 1
            arr[x] = 1
        _ = "_"
        state = [
            0, 3, 3, 3, 3, 0,
            0, 3, 3, 3, 3, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, _, _, _, _, 0,
            0, _, _, _, _, 0,
            0, 0, 0, 0, 0, 0
        ]
        states = []
        for arr in arrs:
            state[25:29] = arr[0:4]
            state[31:35] = arr[4:8]
            states.append(state.copy())
        state_1ht = [[[(1 if (a-1 == i) else 0) for a in state]
                     for i in range(3)] for state in states]
        return state_1ht

    def is_ended(self):
        return self.checkResult() != 0

    def print_states(self, states):
        for state in states:
            pre = [0 for _ in range(6*7)]
            for y in range(7):
                for x in range(6):
                    for k in range(3):
                        if state[k][x+y*6] == 1:
                            pre[x+y*6] = k+1
                print(pre[y*6:y*6+6])
            print("00000000000000000")

    def view_of_states(self, states):
        dst = []
        for state in states:
            list = [0 for _ in range(6*7)]
            for y in range(7):
                for x in range(6):
                    for k in range(3):
                        if state[k][x+y*6] == 1:
                            list[x+y*6] = k+1
            dst.append(list)
        return dst

    def real_state(self):
        state = [0 for _ in range(6*6)]
        side_list = [0, 0, 0, 0, 0, 0]
        for unit in self.units:
            # colorIndex = {'B': 0, 'b': 1, 'R': 2, 'r':3} 大文字は味方
            if unit.x == 9 and unit.y == 9:  # 取られた駒
                if unit.color == 0:    # BLUE(味方の青)
                    side_list[2] += 1
                if unit.color == 2:    # RED(味方の赤)
                    side_list[3] += 1
                if unit.color == 1:    # b(敵の青)
                    side_list[0] += 1
                if unit.color == 3:    # r(敵の赤)
                    side_list[1] += 1
            elif unit.x == 8 and unit.y == 8:   # 脱出駒
                side_list[5] = 1
            elif unit.color == 0:    # BLUE(味方の青)
                state[unit.x+6*unit.y] = "B"
            elif unit.color == 2:    # RED(味方の赤)
                state[unit.x+6*unit.y] = "R"
            elif unit.color == 1:     # b(敵の青)
                state[unit.x+6*unit.y] = "b"
            else:                     # r(敵の赤)
                state[unit.x+6*unit.y] = "r"
        return state+side_list


if __name__ == "__main__":
    # # test for after_states
    game = Geister2()
    game.setRed(["E", "F", "G", "H"])
    game.changeSide()
    game.setRed(["E", "F", "G", "H"])
    after_states = game.after_states()
    game.printBoard()
    # print(game.crr_state())
    # print(after_states[0])
    # game.print_states(after_states)
    game.move(1, 3)
    game.move(1, 3)
    game.move(1, 3)
    game.move(1, 0)
    game.move(1, 0)
    # game.printBoard()
    game.move(1, 3)
    game.move(1, 0)
    game.move(0, 3)
    game.move(0, 3)
    # game.printBoard()
    after_states = game.after_states()
    # game.print_states(after_states)
    # game.print_states(after_states)
    # print(game.view_of_states(after_states))

    print()
    game.print_states(game.init_states())
    # test for moves and on_action_number_received
    # game = Geister2()
    # game.setRed(["E", "F", "G", "H"])
    # game.changeSide()
    # game.setRed(["E", "F", "G", "H"])
    # game.printBoard()
    # game.on_action_number_received(5)
    # game.printBoard()
    # game.move(0, 3)
    # game.printBoard()
    # game.move(0, 2)
    # game.printBoard()
    # game.move(0, 1)
    # game.printBoard()
    # game.move(0, 0)
    # game.printBoard()
