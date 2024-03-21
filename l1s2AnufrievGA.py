from time import sleep
import math
from os import system


class Scene:
    def __init__(self):
        self._figures = []

    def add_figures(self, obj):
        self._figures.append(obj)

    def render(self, width, height, lines, columns, x=0, y=0):
        scene = [['..' for _ in range(columns)] for _ in range(lines)]

        cx, cy = width / columns, height / lines

        for i in range(lines):
            for j in range(columns):
                dw = x + j * cx
                dh = y + i * cy

                for f in self._figures:
                    if f.contain(dw, dh):
                        scene[i][j] = '##'
                        break

        return scene


class Polygon:
    def __init__(self, x0, y0, r, n, coord=None):
        self.x0 = x0
        self.y0 = y0
        self.r = r
        self.n = n
        self.coord = coord

    def recalc(self, phi):
        return [
            (self.x0 + self.r * math.cos(phi + 2 * math.pi * i / self.n),
             self.y0 + self.r * math.sin(phi + 2 * math.pi * i / self.n))
            for i in range(0, self.n + 1)
        ]

    def contain(self, x, y):
        points = self.recalc(self.coord._angle)
        c = 0
        for i in range(len(points)):
            if (((points[i][1] <= y < points[i - 1][1]) or (points[i - 1][1] <= y < points[i][1])) and
                    (x > (points[i - 1][0] - points[i][0]) * (y - points[i][1]) / (points[i - 1][1] - points[i][1]) +
                     points[i][0])):
                c = 1 - c
        return c


class MovingObject:
    def __init__(self,
                 obj,
                 v,
                 g=None,
                 top=None,
                 bottom=None,
                 left=None,
                 right=None
                 ):
        self._obj = obj
        self._vx = v
        self._vy = 0
        self._g = g
        self._top = top
        self._bottom = bottom
        self._left = left
        self._right = right
        self._x = self._obj.x0 + self._obj.r
        self._y = self._obj.y0 + self._obj.r

    def recalc(self, dt):
        self._x += self._vx * dt
        self._obj.x0 = self._x

        if self._vx >= 0:
            if self._right is not None and self._obj.x0 + self._obj.r > self._right:
                self._vx *= -1
                self._x = self._right - self._obj.r
                self._obj.x0 = self._x
        else:
            if self._left is not None and self._obj.x0 - self._obj.r < self._left:
                self._vx *= -1
                self._x = self._left + self._obj.r
                self._obj.x0 = self._x

        vy = self._vy
        self._vy += self._g * dt
        self._y += (vy + self._vy) / 2 * dt
        self._obj.y0 = self._y

        if self._vy >= 0:
            if self._bottom is not None and self._obj.y0 + self._obj.r > self._bottom:
                self._vy *= -1
                self._y = self._bottom - self._obj.r
                self._obj.y0 = self._y
        else:
            if self._top is not None and self._obj.y0 - self._obj.r < self._top:
                self._vy *= -1
                self._y = self._top + self._obj.r
                self._obj.y0 = self._y

        if self._obj.coord._angle >= 0:
            self._obj.coord._angle += math.pi / 90
        else:
            self._obj.coord._angle -= math.pi / 90


def draw(plt):
    print('\n'.join(''.join(i) for i in plt))


class Coord:
    def __init__(self, dx, dy, angle, parent=None):
        self._dx = dx
        self._dy = dy
        self._angle = angle
        self._parent = parent

    def map_to_parents(self, x, y):
        return (
            x * math.cos(self._angle) - y * math.sin(self._angle) + self._dx,
            (x * math.sin(self._angle)) + y * math.cos(self._angle) + self._dy
        )

    def map_to_abs(self, x, y):
        if self._parent:
            return self._parent.map_to_abs(*self.map_to_parents(x, y))
        else:
            return self.map_to_parents(x, y)


sc = Scene()
c1 = Coord(0, 0, math.pi / 4)
c2 = Coord(0, 0, math.pi / 3, c1)
c3 = Coord(0, 0, 0)
p_4 = Polygon(10, 10, 5, 4, c1)
p_3 = Polygon(20, 5, 7, 3, c2)
p_6 = Polygon(40, 20, 6, 6, c3)
sc.add_figures(p_4)
sc.add_figures(p_3)
sc.add_figures(p_6)
mv = [MovingObject(p_4, 10, 10, 0, 50, 0, 50), MovingObject(p_3, 2, 10, 0, 50, 0, 50),
      MovingObject(p_6, -8, 10, 0, 50, 0, 50)]
while True:
    plot = sc.render(50, 50, 50, 50)
    draw(plot)
    for each in mv:
        each.recalc(0.05)
    sleep(0.01)
    system('cls')
