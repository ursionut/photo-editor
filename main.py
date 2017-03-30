__author__ = "6066886: Esma Toptas, 6167662: Ionut Petre Urs"
__copyright__ = "Copyright 2015/2016 – PRG1-Goethe-Uni"
__credits__ = "Prof. Dr. Visvanathan Ramesh and Trainer Andres Fernandez"
__email__ = "topes.14@hotmail.de, ursionut@live.com"


import tkinter as tk
from editor import Editor


def main():
    """
    this function runs the program
    """
    root = tk.Tk()
    app = Editor(root)
    root.title("PyPhoto Editor")
    # sets a minim resolution for the main frame
    root.minsize(width=500, height=500)
    # returns the screen width
    width_size = root.winfo_screenwidth()
    # returns the screen width
    height_size = root.winfo_screenheight()
    # starts the main frame in fullscreen
    root.geometry("{0}x{1}+0+0".format(width_size, height_size))
    root.configure()
    root.mainloop()

# runs the program
if __name__ == '__main__':
    main()
