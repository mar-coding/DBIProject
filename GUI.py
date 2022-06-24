from tkinter import Listbox, Label, scrolledtext

from module.Tree import BPlusTree

import subprocess as sp
import tkinter as tk

INFILENAME = "static/input.txt"
NUMBERS = []


def main():
    master = tk.Tk()
    master.title('BPlusTree Implementation')
    width, height = 2470, 800
    xcord = master.winfo_screenwidth() / 2 - width / 2
    ycord = master.winfo_screenheight() / 2 - height / 2
    master.geometry("%dx%d+%d+%d" % (width, height, xcord, ycord))

    labelAlgo = Label(master, text="Algorithms")
    labelAlgo.grid(row=0, column=0)

    labelInput = Label(master, text="Input")
    labelInput.grid(row=0, column=1)

    labelOutput = Label(master, text="Output")
    labelOutput.grid(row=0, column=3)

    algoLbox = Listbox(master, width=30, height=20, borderwidth=5)
    algoLbox.insert(1, "B+ Tree")
    algoLbox.configure(justify='center')
    algoLbox.grid(row=1, column=0)

    def load():
        inputScrollText.delete(1.0, tk.END)
        fileName = INFILENAME
        with open(fileName, 'r') as Input:
            for line in Input:
                inputScrollText.insert('insert', line)
                for num in line.split(' '):
                    NUMBERS.append(num)
        print(NUMBERS)

    def perform():
        outputScrollText.delete(1.0, tk.END)
        ch = algoLbox.curselection()[0]
        output = None
        if ch == 0:
            print("aa")
            bptree = BPlusTree(4)

            for n in NUMBERS:
                # because its just test dont use real value
                bptree.insert(n, 20)
            output = bptree
            bptree.printTree()
        # outputScrollText.insert('insert', output)

    def clearall():
        inputScrollText.delete(1.0, tk.END)
        outputScrollText.delete(1.0, tk.END)

    def about():
        inputScrollText.delete(1.0, tk.END)
        outputScrollText.delete(1.0, tk.END)
        output = 'BPlusTree Implementation \nDesigned By Mohammad Amin Rahimi.\n'
        outputScrollText.insert('insert', output)

    algoFrame = tk.Frame(master, padx=5, pady=5)
    algoFrame.grid(row=2, column=0)
    aboutButton = tk.Button(algoFrame, text='About', width=10, command=about)
    aboutButton.grid(row=2, column=0)
    loadButton = tk.Button(algoFrame, text='Load', width=10, command=load)
    loadButton.grid(row=2, column=1)
    algoFrame.pack_slaves()

    inputScrollText = scrolledtext.ScrolledText(master, width=35, height=20, padx=5, pady=5)
    inputScrollText.grid(row=1, column=1)
    outputScrollText = scrolledtext.ScrolledText(master, width=83, height=20, padx=5, pady=5)
    outputScrollText.grid(row=1, column=3)

    inputFrame = tk.Frame(master, padx=5, pady=5)
    inputFrame.grid(row=2, column=1)
    performButton = tk.Button(inputFrame, text='Perform', width=10, command=perform)
    performButton.grid(row=0, column=1)

    buttonFrame = tk.Frame(master, padx=5, pady=5)
    buttonFrame.grid(row=2, column=3)
    clearallButton = tk.Button(buttonFrame, text='Clear All', width=10, command=clearall)
    clearallButton.grid(row=0, column=0)
    quitButton = tk.Button(buttonFrame, text='Quit', width=10, command=master.destroy)
    quitButton.grid(row=0, column=1)

    master.mainloop()


if __name__ == '__main__':
    main()
