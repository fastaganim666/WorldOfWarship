from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class BoardException(Exception):
    pass


class BoardWrongShipException(BoardException):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Вы стреляете за пределы поля'


class BoardUsedException(BoardException):
    def __str__(self):
        return 'Вы уже стреляли сюда'


class Ship:
    def __init__(self, l, nose, d):
        self.nose = nose
        self.d = d
        self.live = l
        self.l = l

    @property
    def dots(self):
        cur_x = self.nose.x
        cur_y = self.nose.y
        ship_dots = []
        for i in range(self.l):
            if self.d == 1:
                ship_dots.append(Dot(cur_x + i, cur_y))
            elif self.d == 0:
                ship_dots.append(Dot(cur_x, cur_y + i))
        return ship_dots


class Board:
    def __init__(self, size=6, hid=False):
        self.size = size
        self.hid = hid
        self.count = 0
        self.busy = []
        self.ships = []
        self.field = [['o'] * size for _ in range(size)]

    def __str__(self):
        res = ''
        res += '  1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            res += f' \n{i+1} ' + ' | '.join(row) + ' |'
        if self.hid is True:
            res = res.replace('■', 'o')
        return res

    def out(self, d):
        return not((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contur(self, ship, verb=False):
        NEAR = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (0, 1),
                (1, -1), (1, 0), (1, 1),
                ]
        for d in ship.dots:
            for dx, dy in NEAR:
                cur = Dot(d.x + dx, d.y + dy)
                if (cur not in self.busy) and not(self.out(cur)):
                    self.busy.append(cur)
                    if verb:
                        self.field[cur.x][cur.y] = '.'

    def add_ship(self, ship):
        for d in ship.dots:
            if d in self.busy or self.out(d):
                raise BoardWrongShipException
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)

        self.ships.append(ship)
        self.contur(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException
        if d in self.busy:
            raise BoardUsedException
        self.busy.append(d)
        for ship in self.ships:
            if d in ship.dots:
                ship.live -= 1
                if ship.live == 0:
                    print('Корабль уничтожен!')
                    self.count += 1
                    self.contur(ship, verb=True)
                    self.field[d.x][d.y] = 'x'
                    return False
                if ship.live != 0:
                    print('Корабль ранен!')
                    self.field[d.x][d.y] = 'x'
                    return True
        self.field[d.x][d.y] = 'T'
        print('Мимо!')

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход пк: {d.x + 1}{d.y + 1}')
        return d


class User(Player):
    def ask(self):
        while True:
            coords = input('Ваш ход:').split()
            if len(coords) != 2:
                print('Введите 2 координаты!')
                continue
            x, y = coords
            if not(x.isdigit()) or not(y.isdigit()):
                print('Введите чила!')
                continue
            x, y = int(x), int(y)
            return Dot(x-1, y-1)


class Game:
    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2020:
                    return None
                try:
                    ship = Ship(l, Dot(randint(0, self.size-1), randint(0, self.size-1)), randint(0, 1))
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        pc = self.random_board()
        pc.hid = True

        self.ai = AI(pc, pl)
        self.us = User(pl, pc)

    def greet(self):
        print("-------------------------")
        print("     Приветсвуем вас     ")
        print("         в игре          ")
        print("       морской бой       ")
        print("-------------------------")
        print("    формат ввода: x y    ")
        print("    x - номер строки     ")
        print("    y - номер столбца    ")

    def loop(self):
        num = 0
        while True:
            print("-------------------------")
            print("Доска пользователя: ")
            print(self.us.board)
            print("---------------------")
            print("Доска компьютера: ")
            print(self.ai.board)
            if num % 2 == 0:
                print("Ходит пользователь: ")
                repeat = self.us.move()
            else:
                print("Ходит компьютер: ")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.board.count == 7:
                print("-------------------------")
                print('Пользователь выиграл!')
                break
            if self.us.board.count == 7:
                print("-------------------------")
                print('Компьютер выиграл!')
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()