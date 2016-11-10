from random import uniform as rnd, choice
from numpy import sqrt
from tkinter import *
import time

root = Tk()
fr = Frame(root)
# print('Enter the width of the field along the horizontal axis:')
xr = '2560'
# print('Enter the width of the field along the vertical axis:')
yr = '1440'
root.geometry(xr + 'x' + yr)
canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)


class Vector:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __str__(self):
        return str(self.x) + ' ' + str(self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        return other - self

    def __isub__(self, other):
        return self - other

    def __mul__(self, other):
        if type(other) == Vector:
            return self.x * other.x + self.y * other.y
        elif type(other) == float or int:
            return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self * other

    def rad(self):
        return sqrt(self * self)

    def __truediv__(self, other):
        return Vector(self.x/other, self.y/other)

    def __itruediv__(self, other):
        return self/other

    def returned(self, arg):
        if arg == 0:
            return self.x
        if arg == 1:
            return self.y


class Atom:
    def __init__(self, axel=0, resist=0):
        # self.m = choice([1])
        # if self.m == 1:
        #     self.r = 1
        # else:
        #     self.r = 3
        self.m = rnd(1,70)
        self.r = self.m ** 0.7 * rnd(9, 12)/10
        global xr, yr
        self.a, self.b = int(xr), int(yr)
        self.r1 = int(self.r + 1)
        self.x, self.y = rnd(self.r1, self.a - self.r1), rnd(self.r1, self.b - self.r1)
        self.resist, self.axel = resist, axel
        self.vx, self.vy = rnd(-100, 100), rnd(-100, 100)
        # self.vx, self.vy = rnd(-10, 10), rnd(-10, 10)
        k = 10
        for i in ['gray', 'blue', 'green', 'black', 'brown', 'pink', 'red']:
            if 0 < self.m <= k:
                self.color = i
                break
            k += 10
        self.id = canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color)

    def set_coords(self):
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

    def move(self):
        if self.r <= self.y <= self.b - self.r:
            self.vy -= self.axel + self.vy * self.resist
        elif self.y > self.b - self.r and self.vy < 0:
                self.vy = -self.vy
        elif self.r > self.y and self.vy > 0:
            self.vy = -self.vy
        if self.r <= self.x <= self.a - self.r:
            self.vx -= self.vx * self.resist
        elif self.x > self.a - self.r and self.vx > 0:
            self.vx = -self.vx
        elif self.r > self.x and self.vx < 0:
            self.vx = -self.vx
        self.y -= self.vy
        self.x += self.vx
        self.set_coords()

    def clashtest(self, ob):
        a, b, c = self.r + ob.r, self.x - ob.x, self.y - ob.y
        if a*a >= b*b + c*c:
            return True
        return False

    def reverse(self, ob):  # a task of the mutual clashes of two firm balls
        v1, v2 = Vector(self.vx, self.vy), Vector(ob.vx, ob.vy)
        r1, r2, mass = Vector(self.x, self.y), Vector(ob.x, ob.y), self.m + ob.m
        alpha = r2 - r1
        delta = alpha.rad()
        alpha = alpha / delta
        v1p, v2p = v1 * alpha, v2 * alpha  # these quantities will be changed
        v1t, v2t = v1 - v1p * alpha, v2 - v2p * alpha  # these quantities are saving
        mass_centre = (self.m * v1p + ob.m * v2p)/mass
        v1p, v2p = v1p - mass_centre, v2p - mass_centre
        v1p, v2p = v2p * ob.m / self.m, v1p * self.m / ob.m
        v1p, v2p = (v1p + mass_centre) * alpha, (v2p + mass_centre) * alpha
        v1, v2 = v1p + v1t, v2p + v2t
        delta = self.r + ob.r - delta
        r2 += alpha * delta * self.m/mass
        r1 -= alpha * delta * ob.m/mass
        oby, selfy = ob.y, self.y
        self.x, self.y = r1.returned(0), r1.returned(1)
        ob.x, ob.y = r2.returned(0), r2.returned(1)
        self.vx, self.vy = v1.returned(0), v1.returned(1) + (selfy - self.y) * self.axel
        ob.vx, ob.vy = v2.returned(0), v2.returned(1) + (oby - ob.y) * self.axel
        global f
        f += 1

    def energy(self):
        return self.m * (self.vx * self.vx + self.vy * self.vy)

    # def nonrnd(self):
    #     self.m, self.r, self.color = 20, 10, 'red'
    #     self.id = canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color)
    #     canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
    #     self.set_coords()
    # It isnt done!! For some (unknown) reason, colored balls still remain in the mode of the random selection of the mass and radius.


def new_game(n=1, rand=True, event=''):
    global f
    balls, e, k, f, it = [Atom() for i in range(n)], 0, 1, 0, 0
    screen1 = canv.create_text(400, 300, text='', font='28')
    # if not rand:
    #     for i in balls:
    #         i.nonrnd()
    while True:
        it += 1
        for b in balls:
            b.move()
            for i in balls[k:]:
                if b.clashtest(i):
                    b.reverse(i)
            k += 1
            e += b.energy()
        canv.itemconfig(screen1, text='Temperature: '+str(e/n)+'\nMutual clashes: '+str(f)+'\nIterations: '+str(it))
        e, k, f = 0, 1, 0
        canv.update()
        # time.sleep(0.000000001)
    root.after(750, new_game)

# print('Input the number of atoms:')
K = 200
new_game(K)

mainloop()