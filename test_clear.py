import os
import time
import tkinter as tk
from tkinter import messagebox

# print("LINE 1")
# print("LINE 2") 
# print("LINE 3")
# print("Waiting 2 seconds...")
# time.sleep(2)

# # Test ANSI clear
# print("\033[2J\033[H", end="")

# print("AFTER CLEAR - do you see lines 1-3 above this?")

class Confirmations():

    def __init__(self, tk_title, tk_type, message):
        self.tk_title = tk_title
        self.tk_type = tk_type
        self.message = message

    def window(self):

        root = tk.Tk()
        root.title("Confirm")
        root.geometry("1x1+600+500") # make main window small, move window close to center screen
        root.attributes('-topmost', True)  # bring to front
        root.update()

        method = getattr(messagebox, self.tk_type)
        result = method(self.tk_title, self.message, parent=root)
        
        root.destroy()
        return result


confirm_action = Confirmations("Confirm", "askyesno", "Are you sure you want to pause the timer?")

print(confirm_action.window())
