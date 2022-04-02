# Импорт всех классов
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# Глобальные настройки
Window.size = (250, 200)
Window.clearcolor = (255 / 255, 186 / 255, 3 / 255, 1)
Window.title = "Конвертер"


# class Section(TextInput):
#     def __init__(self, flag_x, flag_y, text=''):
#         super().__init__(text=text)
#         self.flag_x = flag_x
#         self.flag_y = flag_y


class MyApp(App):
    # Создание всех виджетов (объектов)
    def __init__(self, n):
        super().__init__()
        self.n = n
        self.matrix = list(list() for i in range(n))

        self.tree = Label()
        
        for i in range(n):
            for i2 in range(n):
                if i == i2:
                    self.matrix[i].append(Label())
                else:
                    self.matrix[i].append(TextInput(multiline=False, text=""))

        for i in range(n):
            for i2 in range(n):
                if i != i2:
                    print(type(self.matrix[i][i2]))
                    self.matrix[i][i2].bind(text=self.on_text)

    # Получаем данные и производит их конвертацию
    def on_text(self, *args):
        for i in range(self.n):
            for i2 in range(self.n):
                if i != i2:
                    data = self.matrix[i][i2].text

                    if data.isnumeric() or data == "":
                        if data != self.matrix[i2][i].text:
                            self.matrix[i2][i].text = data
                            print(data)
                    else:
                        self.matrix[i][i2].text = ""

    # Основной метод для построения программы
    def build(self):
        # Все объекты будем помещать в один общий слой
        box = GridLayout(cols=self.n)
        box2 = BoxLayout(orientation='vertical')
        for i in range(self.n):
            for i2 in range(self.n):
                box.add_widget(self.matrix[i][i2])
        box2.add_widget(box)
        box2.add_widget(self.tree)
        return box2


# Запуск проекта
if __name__ == "__main__":
    MyApp(3).run()