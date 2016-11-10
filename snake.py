from random import choice
from tkinter import *
from time import sleep

root = Tk()
fr = Frame(root)
xr, yr, R = '1920', '1040', 10
root.geometry(xr + 'x' + yr)
canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)
big_set = set()
intxr, intyr = int(xr), int(yr)
for i in range(0, intxr, R):
    for j in range(0, intyr, R):
        big_set.add((i, j))


class Block:
    def __init__(self, x=0, y=0):
        self.len, self.x, self.y, self.color = R, x, y, 'red'
        self.id = canv.create_rectangle(self.x, self.y, self.x + self.len, self.y + self.len, fill=self.color)
        self.renew(True)

    def renew(self, born=False):
        if not born:
            self.color = 'black'
        canv.coords(self.id, self.x, self.y, self.x + self.len, self.y + self.len)
        canv.itemconfig(self.id, fill=self.color)

    def remove(self, blocks=None, cords=set(), del_id=True):
        if del_id:
            canv.delete(self.id)
        cords.discard((self.x, self.y))
        if type(blocks) == list:
            blocks.pop(0)


class Snake:
    def __init__(self, direction=0):
        self.xsn, self.ysn, self.blocks = 0, 0, [] #intxr//6, intyr//2, []
        self.direction, self.cords = direction, set()
        self.create()

    def lose(self, screen):
        canv.itemconfig(screen, text='Game over')
        mainloop()

    def create(self):
        self.cords.add((self.xsn, self.ysn))
        self.blocks.append(Block(self.xsn, self.ysn))

    def clash_test(self, foods=None):
        if foods != None:
            if (self.xsn, self.ysn) == (foods.x, foods.y):
                return 0
        if (self.xsn, self.ysn) in self.cords or not (0 <= self.xsn < intxr and 0 <= self.ysn < intyr):
            return 1
        return None

    def change_direction(self, button):
        self.direction += button

    def move(self, screen, foods, to_cut=True):
        self.do(self.direction % 4)
        if self.clash_test(foods) == 0:
            to_cut = False
            foods.new(self)
        elif self.clash_test(foods) == 1:
            print(self.xsn, self.ysn)
            self.lose(screen)
        self.blocks[-1].renew()
        self.create()
        if to_cut:
            self.blocks[0].remove(self.blocks, self.cords)

    def do(self, num, n=R):
        if num == 0:
            self.xsn += n
        elif num == 1:
            self.ysn += n
        elif num == 2:
            self.xsn -= n
        elif num == 3:
            self.ysn -= n

    def return_cords(self):
        return self.cords

    def robot(self):
        if (self.clash_test() == 1 and self.direction == 4) or self.ysn == R * intyr//R:
            self.direction = 0
        if self.direction == 0:
            if self.ysn == 0:
                self.direction = 1
            else:
                self.direction = 4


class Food(Block):
    def __init__(self):
        super(Food, self).__init__()

    def create(self, snk):
        self.randomise(snk.return_cords())
        self.color = 'green'
        self.renew(True)

    def randomise(self, snak):
        point = choice(list(big_set - snak))
        self.x, self.y = point[0], point[1]

    def new(self, snak):
        self.remove(None, set(), False)
        self.create(snak)


def game():
    screen = canv.create_text(intxr/2, intyr/2, text='', font='28')
    sn, fd = Snake(), Food()
    fd.create(sn)
    s = 0
    while sn:
        sn.robot()
        canv.focus_set()
        canv.bind("<KeyPress>", movement_handler)
        canv.update()
        if s != k:
            sn.change_direction(direction)
            s = k
        sn.move(screen, fd)
        sleep(0.05)
    canv.itemconfig(screen, text='')
    canv.delete(sn, fd)

direction, k = 0, 0


def movement_handler(event):
    global direction, k
    if event.keysym == "Left":
        direction = -1
        k += 1
    elif event.keysym == "Right":
        direction = 1
        k += 1

game()
mainloop()