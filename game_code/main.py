import tkinter as tk
from game import TravelGame

if __name__ == "__main__":
    root = tk.Tk()
    game = TravelGame(root)
    root.mainloop()