from kivy.lang import Builder
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from math import inf


Builder.load_file('main.kv')


def get_min(R, U):
    rm = (-1, -1, inf)
    for v in U:
        rr = min(R, key=lambda x: x[2] if (x[0] == v or x[1] == v) and (x[0] not in U or x[1] not in U) else inf)
        if rm[2] > rr[2]:
            rm = rr
    return rm


class Matrix(App):
    def __init__(self, n=0):
        super().__init__()
        self.n = n
        self.n_vertex = TextInput(text=str(self.n))
        self.n_vertex.bind(text=self.changing_matrix)
        self.find_out_btn = Button(text="Расчёт")
        self.find_out_btn.bind(on_press=self.find_out)
        self.back_to_main_menu_btn = Button(text="В меню")
        self.matrix_box = GridLayout(cols=self.n)
        self.app_box = BoxLayout(orientation='vertical')
        self.input_menu_box = BoxLayout(size_hint=(1, .2))
        self.tree_label = Label(valign="middle", halign="center", color=[0, 1, 0, 1], text="Jndtb", size_hint=(1, .2))
        self.matrix = list()

    # добавление эл-тов в массив матрицы
    def create_matrix(self, *args):
        for i in range(self.n):
            self.matrix.append(list())
            for i2 in range(self.n):
                if i == i2:
                    self.matrix[i].append(Label())
                else:
                    self.matrix[i].append(TextInput())
                    if i2 > i:
                        self.matrix[i][i2].bind(text=self.sim_rule0)
                    else:
                        self.matrix[i][i2].bind(text=self.sim_rule1)

    # удаление матрицы с matrix_box
    def remove_matrix(self, *args):
        for i in range(self.n):
            for i2 in range(self.n):
                self.matrix_box.remove_widget(self.matrix[i][i2])

    # добавление матрицы в matrix_box
    def add_matrix(self):
        self.matrix_box.cols = self.n
        for i in range(self.n):
            for i2 in range(self.n):
                self.matrix_box.add_widget(self.matrix[i][i2])

    # расширение массива матрицы
    def expand_matrix(self, t):
        for i in range(self.n):
            for i2 in range(t - self.n):
                self.matrix[i].append(TextInput())
                self.matrix[i][-1].bind(text=self.sim_rule0)
        for i in range(t - self.n):
            self.matrix.append(list())
            for i2 in range(t):
                if self.n + i == i2:
                    self.matrix[-1].append(Label())
                else:
                    self.matrix[-1].append(TextInput())
                    if i2 > self.n + i:
                        self.matrix[i][-1].bind(text=self.sim_rule0)
                    else:
                        self.matrix[i][-1].bind(text=self.sim_rule1)

    # сужение массива матрицы
    def compression_matrix(self, t):
        for i in range(self.n):
            for i2 in range(t - self.n):
                del self.matrix[i][-1]
        for i in range(t - self.n):
            del self.matrix[-1]

    # Забинден на n_vertex. Обработка массива matrix и добавение его на matrix_box, в зависимости от введённых значений
    def changing_matrix(self, *args):
        x = self.n_vertex.text
        if x.isnumeric():
            x = int(x)
            self.remove_matrix()
            if x < self.n:
                self.compression_matrix(x)
            elif (x > self.n) and (self.n != 0):
                self.expand_matrix(x)
            else:
                self.n = x
                self.create_matrix()
            self.n = int(x)
            self.matrix_box.cols = self.n
            self.add_matrix()

    # Правило заполнения матрицы
    def sim_rule0(self, *args):
        for i in range(self.n):
            for i2 in range(self.n):
                self.matrix[i2][i].text = self.matrix[i][i2].text

    def sim_rule1(self, *args):
        for i in range(self.n):
            for i2 in range(self.n):
                self.matrix[i][i2].text = self.matrix[i2][i].text

    def get_ribs(self):
        ribs = [(-1, -1, inf)]
        f = True
        for i in range(self.n):
            for i2 in range(i, self.n):
                if self.matrix[i][i2].text.isnumeric() and f:
                    ribs.append((i, i2, int(self.matrix[i][i2].text)))
                elif self.matrix[i][i2].text not in (" ", "x", "х", "-"):
                    self.matrix[i][i2].background_color = (1, 0, 0, 1)
        if f:
            return ribs
        return -1

    def set_tree(self):
        pass

    def find_out(self, *args):
        ribs = self.get_ribs()
        if ribs != -1:
            return 0
        m_o_union_vertex = {1}  # множество соединенных вершин
        ost_rib = []  # список ребер остова

        while len(m_o_union_vertex) < self.n:
            r = get_min(ribs, m_o_union_vertex)  # ребро с минимальным весом
            if r[2] == inf:  # если ребер нет, то остов построен
                break

            ost_rib.append(r)  # добавляем ребро в остов
            m_o_union_vertex.add(r[0])  # добавляем вершины в множество U
            m_o_union_vertex.add(r[1])

        print(m_o_union_vertex)
        print(ost_rib)
        print(ribs)
        self.tree_label.text = ''
        for i in range(len(ost_rib)):
            self.tree_label.text += str(ost_rib[i][0]+1) + "->" + str(ost_rib[i][1]+1)
            if len(ost_rib) > i+1:
                self.tree_label.text += "; "

    def build(self, *args):
        self.input_menu_box.add_widget(self.back_to_main_menu_btn)
        self.input_menu_box.add_widget(self.n_vertex)
        self.input_menu_box.add_widget(self.find_out_btn)
        self.app_box.add_widget(self.input_menu_box)
        self.app_box.add_widget(self.matrix_box)
        self.app_box.add_widget(self.tree_label)
        return self.app_box


if __name__ == "__main__":
    Matrix().run()
