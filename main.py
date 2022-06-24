from kivy.app import App
from kivy.uix.button import Button
from module.Tree import BPlusTree


class Test01App(App):
    def build(self):
        return Button(text='Click Me!')


def main():
    # Test01App().run()
    bpt = BPlusTree(order=4)
    bpt.insert(10, 20)
    bpt.insert(22, 20)
    bpt.insert(45, 20)
    bpt.insert(26, 20)
    bpt.insert(12, 20)
    bpt.insert(8, 20)
    bpt.insert(7, 20)
    bpt.insert(6, 20)
    bpt.insert(9, 20)
    bpt.insert(4, 20)
    bpt.insert(5, 20)
    # bpt.delete(26)
    # bpt.delete(6)

    bpt.printTree()
    # bpt.showAllData()


if __name__ == "__main__":
    main()
