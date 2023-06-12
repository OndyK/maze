class Node:
    def __init__(self, value):
        self.pos = value
        self.parent = None

class Memory:
    def __init__(self, lvl):
        self.memory = []
        self.queue = []
        self.way = []
        self.lvl = lvl
    def find_way(self, position):
            for x in [1,-1]:
                try:
                    if position.pos[0] == 0 and x == -1:
                        continue
                    elif self.lvl[position.pos[1]][position.pos[0]+x] != "1":
                        way = Node([position.pos[0]+x, position.pos[1]])
                        way.parent = position
                        if way.pos not in self.memory:
                            self.memory.append(way.pos)
                            self.queue.append(way)
                except IndexError:
                    continue
            for y in [1,-1]:
                try:
                    if position.pos[1] == 0 and y == -1:
                        continue
                    elif self.lvl[position.pos[1]+y][position.pos[0]] != "1":
                        way = Node([position.pos[0],position.pos[1]+y])
                        way.parent = position
                        if way.pos not in self.memory:
                            self.memory.append(way.pos)
                            self.queue.append(way)
                except IndexError:
                    continue
            
            if self.lvl[position.pos[1]][position.pos[0]] == "2":
                knot = position
                self.way.append(knot.pos)
                while knot.parent != None:
                    self.way.append(knot.parent.pos)
                    knot = knot.parent
            return self.queue