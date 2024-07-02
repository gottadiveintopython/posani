from random import shuffle
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button


KV_CODE = r'''
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'shuffle'
        on_press: app.shuffle()
        size_hint_y: None
        height: '50dp'
    GridLayout:
        id: grid
        cols: 3
        padding: 20
        spacing: 20
'''


class SampleApp(App):
    def build(self):
        return Builder.load_string(KV_CODE)

    def on_start(self):
        from kivy_garden.posani import activate
        grid = self.root.ids.grid
        for i in range(grid.cols ** 2):
            button = Button(text=str(i), opacity=0.7, font_size=50)
            activate(button)
            grid.add_widget(button)

    def shuffle(self):
        grid = self.root.ids.grid
        children = grid.children[:]
        shuffle(children)
        grid.clear_widgets()
        for child in children:
            grid.add_widget(child)


if __name__ == '__main__':
    SampleApp().run()
