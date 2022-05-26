from kivy.app import App
from kivy.uix.button import Button

class Test01App(App):
    def build(self):
        return Button(text='Click Me!')



def main():
    Test01App().run()


if __name__ == "__main__":
    main()
