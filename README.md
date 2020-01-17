# tick-tack-toe-ai
научно-исследовательская работа на тему "искусственный интеллект"

автор: Батятин Максим (DevMule)

github: https://github.com/DevMule/tick-tack-toe-ai

цель работы: исследовать процессы проектирования и создания автоматических систем для решения конкретных задач

Я пытался выбрать для проекта простую, знакомую каждому основу что позволит мне, разрабатывая ботов, 
долгое время не доходить до состояния нераспутываемого хаоса. Мой выбор пал на древнюю игру - "херики-оники".
Прежде чем начать разрабатывать ботов, необходимо создать основу для игры.

# Игровое поле
Это оказалось нетрудно, т.к. по сути игра представляет из себя массив со значениями для каждой ячейки и функцию проверки на победу.
Другое дело - я понятия не имел чем буду ограничиваться в будущем, ведь правил и видов крестиков-ноликов есть довольно большое количество, потому исходя из этого и имеющихся на данным момент привычек сделал систему "резиновой" - поле и условие победы может быть разных размеров
```python
class Desk:
    def __init__(self, w=3, h=3, win_row=3):
        self.w = w
        self.h = h
        # создать историю доски мне захотелось чуть позже, когда я начал учить бота на нейроисети
        self.history = self.__turn = self.desk = self.win_row = self.winner = None
        self.clear(w, h, win_row)

    def get_turn(self):
        # возвращает знак, который система ожидает получить: "X" или "0"
        # организован как геттер .turn

    # main funcs
    def clear(self, w=None, h=None, win_row=None):
        # обнуляет доску с новыми заданными или меющимися параметрами, если они не заданы

    def make_turn(self, x, y):
        # функция проверяет возможно ли сделать ход, 
        # если да, то ставит в указанных координатах соответствующий знак и возвращает True
        # иначе ничего не делает и возвращает False
```
Хорошо! Доска есть, теперь нужно сделать так, чтобы в неё можно было хотя бы играть. Нужно сделать реффери, который будет запрашивать ход у игроков и универсальный интерфейс от которого будут наследоваться игроки во имя полиморфизма!
# Реффери и Контроллер
```python
class Referee:
    def __init__(self, player_1, player_0, desk=Desk(3, 3, 3)):
        self.player_0 = player_0  # 0 - player
        self.player_1 = player_1  # X - player
        self.desk = desk

    def swap_players(self):
        # эта функция появилась позже, когда я начал обучать бота на нейросетях
        # ведь начинать первым или вторым - совершенно разный опыт

    def game_loop(self):
        # функция проверяет условие победы в доске, если игра закончилась 
        # то отправляет игрокам их состояние в игре "WIN", "LOSE" или "TIE"
        # если игра продолжается, то рекурсивно вызывает сама себя

    def ask_for_turn(self):
        # проверяет состояние доски и запрашивает ход у соответствующего игрока


class Controller:
    def __init__(self):
        return

    def make_turn(self, desk):
        return [0, 0]

    def game_ended(self, desk, state, my_figure):
        return
```
# Игроки
Под игроками я подразумеваю системы, которые будут взаимодействовать с игрой как игроки. Это боты и пользовательские интерфейсы, но никак не люди.
## рандомный бот
Просто расширяет у контроллера метод хода, выдаёт случайную свободную координату. Это самый скучный и самый лёгкий игрок, 
однако даже он иногда побеждает minimax бота :)
```python
def pick_random(desk, w, h):
    x = rand(0, w-1)
    y = rand(0, h-1)
    while desk[y][x] != -1:
        x = rand(0, w-1)
        y = rand(0, h-1)
    return [x, y]


class RandomBot(Controller):
    def make_turn(self, desk):
        return pick_random(desk.desk, desk.w, desk.h)
```
## minimax бот
Более комплексная машина, но тоже представляет из себя только расширение метода совершения хода
Суть его содержания [понятна уже из названия](https://www.youtube.com/watch?v=KU9Ch59-4vw).
Его победить довольно сложно, однако возможно, расставляя подобные ловушки:
> ![ловушка джокера](https://image.prntscr.com/image/cPHTPBs8TBq2sQ1GhqOfIA.png)

Хотя, как понятно из скриншота, minimax бот сам тоже умеет их расставлять :)
```python
class MiniMaxBot(Controller):
    def __init__(self):
        super().__init__()
        self.win_row = None

    def make_turn(self, desk):
        if first_step(desk.desk):
            return pick_random(desk.desk, desk.w, desk.h)

        cloned = clone_desk(desk.desk)
        figure = desk_consts[desk.turn]
        self.win_row = desk.win_row
        ways = self.calc_states_tree(cloned, figure, get_all_ways(cloned))
        for potential_way in ways:
            if potential_way[2] == 1:
                return potential_way
        for potential_way in ways:
            if potential_way[2] == 0:
                return potential_way
        return ways[0]

    def calc_states_tree(self, desk, figure, ways):
        for potential_way in ways:
            potential_way.append(self.get_value(desk, potential_way, figure))
            potential_way[2] *= -1  # swap weight
        return ways

    def get_value(self, desk, way, figure):
        # if we know value of this case, return value
        desk = clone_desk(desk)
        desk[way[1]][way[0]] = figure
        if check_win(way[0], way[1], desk, self.win_row):
            return -1  # it will be swapped later

        # if we need to go deeper, go deeper
        ways = get_all_ways(desk)
        if len(ways) > 0:
            valued_ways = self.calc_states_tree(desk, 1 - figure, ways)
            for potential_way in valued_ways:
                if potential_way[2] == 1:
                    return 1
            return 0

        # if we dont have any ways to go, return value = 0
        return 0
```
