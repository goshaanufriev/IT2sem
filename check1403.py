class Bottle:
    def __init__(self, v, vmax):
        self._v = v
        self._vmax = vmax

    def __len__(self):
        return self._v

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value):
        self._v = value

    @property
    def vmax(self):
        return self._vmax

    @vmax.setter
    def vmax(self, value):
        self._vmax = value

    def fill(self):
        self._v = self._vmax


class Backpack:
    def __init__(self):
        self.stuff = []

    def __len__(self):
        return len(self.stuff)

    def put_in(self, thing):
        if thing in self.stuff:
            print('This thing is already in the backpack')
        else:
            self.stuff.append(thing)

    def put_out(self, thing):
        if thing not in self.stuff:
            print("There's no this thing in the backpack")
        else:
            self.stuff.pop(self.stuff.index(thing))


class Item:
    def __init__(self, name):
        self.name = name


class Tourist:
    def __init__(self, backpack):
        self.backpack = backpack
        self.balance = 100

    def drink(self, btl):
        if btl in self.backpack.stuff:
            print('Put the bottle out')
            return None
        if btl.v <= 0.05:
            print('Fill the bottle!')
            return None
        if self.balance == 100:
            btl.v -= 0.1
        elif self.balance <= 100:
            btl.v -= 0.1
            self.balance += 1
            if self.balance >= 100:
                self.balance = 100
        while self.balance <= 85:
            if btl.v <= 0.05:
                print('Water is over! :(')
                break
            btl.v -= 0.1
            self.balance += 1


def balance_loss(backpack):
    return len(backpack) // 2


def example():
    bp = Backpack()
    tourist = Tourist(bp)
    btl1 = Bottle(1, 1)
    btl2 = Bottle(0.5, 0.8)
    item1 = Item("first aid kit")
    item2 = Item("cap")
    item3 = Item("matches")
    item4 = Item("raincoat")
    item5 = Item('sandwiches')
    items = [btl1, btl2, item1, item2, item3, item4, item5]
    for x in items:
        bp.put_in(x)

    s = 0
    while s < 2000:
        tourist.balance -= (2 + balance_loss(bp))
        if tourist.balance <= 20:
            print("Stop and drink water!!!")
            tourist.backpack.put_out(btl1)
            tourist.backpack.put_out(btl2)
            while tourist.balance <= 85:
                tourist.drink(btl1)
                tourist.drink(btl2)
                btl1.fill()
                btl2.fill()
            tourist.backpack.put_in(btl1)
            tourist.backpack.put_in(btl2)
            print(btl1.v, btl2.v, tourist.balance)
        s += 100
    tourist.drink(btl1)
    tourist.backpack.put_out(btl1)
    if tourist.balance <= 85:
        tourist.drink(btl1)
    else:
        for i in range(3):
            tourist.drink(btl1)
    tourist.backpack.put_out(btl1)
    tourist.backpack.put_in(btl1)
    print(btl1.v)


example()
