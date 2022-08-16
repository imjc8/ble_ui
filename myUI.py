import tkinter as tk

# constants
WIDTH = 1000
HEIGHT = 600

root = tk.Tk()
root.title('Potentiostat Software')

# label
myLabel1 = tk.Label(root, text="Select Device")

# canvas
canvas = tk.Canvas(root, width=1000, height=1000)

print("hello world")


root.mainloop()