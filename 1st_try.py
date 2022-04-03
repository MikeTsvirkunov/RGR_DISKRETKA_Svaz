# Импорт всех классов
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
import math

# Глобальные настройки
# Window.size = (250, 200)
Window.clearcolor = (255 / 255, 186 / 255, 3 / 255, 1)
Window.title = "Конвертер"


# class Section(TextInput):
#     def __init__(self, flag_x, flag_y, text=''):
#         super().__init__(text=text)
#         self.flag_x = flag_x
#         self.flag_y = flag_y


class Matriza(App):
    # Создание всех виджетов (объектов)
    def __init__(self, n=0):
        super().__init__()
        self.matrix = list()
        self.n = n
        self.btn = Button()
        self.btn.bind(on_press=self.rasch)
        self.tree = Label(text='', markup=True)
        self.tree.disabled_color = (0 / 255, 186 / 255, 3 / 255, 1)
        self.tree.texture_update()
        self.n_vertex = TextInput(text=str(n))
        self.n_vertex.bind(text=self.init_n)
        self.box = GridLayout(cols=self.n)
        self.box2 = BoxLayout(orientation='vertical')
        self.create_map()

    # дефолтное создание матрицы
    def create_map(self, *args):
        for i in range(self.n):
            self.matrix.append(list())
            for i2 in range(self.n):
                if i == i2:
                    self.matrix[i].append(Label(size=(20, 20)))
                elif i < i2:
                    self.matrix[i].append(TextInput(multiline=False, text="", size=(20, 20)))
                    self.matrix[i][i2].bind(text=self.on_text)
                else:
                    self.matrix[i].append(TextInput(multiline=False, text="", size=(20, 20)))
                    self.matrix[i][i2].bind(text=self.on_text1)

    def rem_map(self):
        for i in range(self.n):
            for i2 in range(self.n):
                self.box.remove_widget(self.matrix[i][i2])

    # Получаем данные и производит их конвертацию
    def init_n(self, *args):
        n_v = self.n_vertex.text
        if n_v.isnumeric():
            n_v = int(n_v)
            self.box.cols = n_v
            self.box2.remove_widget(self.box)
            self.box2.remove_widget(self.btn)
            self.box2.remove_widget(self.tree)
            if n_v < 0:
                pass

            elif self.n == 0:
                self.n = n_v
                self.create_map()

            elif self.n < n_v:
                self.rem_map()
                for i in range(n_v):
                    if i < self.n:
                        for i2 in range(n_v):
                            if i2 >= self.n:
                                self.matrix[i].append(TextInput(multiline=False, text="", size=(20, 20)))
                                self.matrix[i][i2].bind(text=self.on_text)
                    else:
                        self.matrix.append(list())
                        for i2 in range(n_v):
                            if i == i2:
                                self.matrix[i].append(Label(size=(20, 20), color="000000"))
                            elif i < i2:
                                self.matrix[i].append(TextInput(multiline=False, text="", size=(20, 20)))
                                self.matrix[i][i2].bind(text=self.on_text)
                            else:
                                self.matrix[i].append(TextInput(multiline=False, text="", size=(20, 20)))
                                self.matrix[i][i2].bind(text=self.on_text1)

            elif self.n > n_v:
                self.rem_map()
                for i in range(n_v, self.n):
                    del self.matrix[-1]
                for i in range(n_v):
                    for i2 in range(n_v, self.n):
                        del self.matrix[i][-1]

            self.n = n_v
            for i in range(self.n):
                for i2 in range(self.n):
                    self.box.add_widget(self.matrix[i][i2])
                    print(*list(i2.text for i2 in self.matrix[i]))
            self.box2.add_widget(self.box)
            self.box2.add_widget(self.btn)
            self.box2.add_widget(self.tree)

    def on_text(self, *args):
        for i in range(self.n):
            for i2 in range(self.n):
                if i != i2:
                    data = self.matrix[i][i2].text

                    if data.isnumeric() or data == "":
                        if data != self.matrix[i2][i].text:
                            self.matrix[i2][i].text = data
                            self.matrix[i2][i].color = (0 / 255, 0 / 255, 0 / 255, 1)
                    else:
                        self.matrix[i][i2].text = ""

    def on_text1(self, *args):
        for i in range(self.n):
            for i2 in range(self.n):
                if i != i2:
                    data = self.matrix[i2][i].text

                    if data.isnumeric() or data == "":
                        if data != self.matrix[i][i2].text:
                            self.matrix[i][i2].text = data
                            print(data)
                    else:
                        self.matrix[i2][i].text = ""

    def rasch(self, *args):
        R = [(-1, -1, math.inf)]
        for i in range(self.n-1):
            for i2 in range(i+1, self.n - i):
                if self.matrix[i][i2].text.isnumeric():
                    R.append((i, i2, int(self.matrix[i][i2].text)))

        U = {1}  # множество соединенных вершин
        T = []  # список ребер остова

        while len(U) < self.n:
            r = get_min(R, U)  # ребро с минимальным весом
            if r[2] == math.inf:  # если ребер нет, то остов построен
                break

            T.append(r)  # добавляем ребро в остов
            U.add(r[0])  # добавляем вершины в множество U
            U.add(r[1])
        print(T)
        for i in T:
            self.tree.text += str(i[0]) + "->" + str(i[1]) + "; "


    # Основной метод для построения программы
    def build(self):
        # Все объекты будем помещать в один общий слой
        self.box2.add_widget(self.n_vertex)
        if len(self.matrix) > 0:
            for i in range(self.n):
                for i2 in range(self.n):
                    self.box.add_widget(self.matrix[i][i2])
        self.box2.add_widget(self.box)
        self.box2.add_widget(self.btn)
        self.box2.add_widget(self.tree)
        return self.box2


def get_min(R, U):
    rm = (-1, -1, math.inf)
    for v in U:
        rr = min(R, key=lambda x: x[2] if (x[0] == v or x[1] == v) and (x[0] not in U or x[1] not in U) else math.inf)
        if rm[2] > rr[2]:
            rm = rr
    return rm


# Запуск проекта
if __name__ == "__main__":
    Matriza(0).run()