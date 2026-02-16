import threading
import time
import os

def clear_screen():
    """Clears the terminal screen for Windows, Linux, and macOS."""
    # Check the operating system name
    if os.name == 'nt':
        # Command for Windows
        _ = os.system('cls')
    else:
        # Command for Linux/macOS (posix is the name for non-Windows systems)
        _ = os.system('clear')

# Call the function to clear the screen


def do_something():
    print("Sleeping 1 second...")
    time.sleep(1)
    print("Done Sleeping...")
    

t1 = threading.Thread(target=do_something)
t2 = threading.Thread(target=do_something)

t1.start()
t2.start()

clear_screen()

import tkinter as tk
from time import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Timer App")
        
        self.elapsed_time = 0
        self.running = False
        self.start_time = None
        
        # Title
        title_label = tk.Label(root, text="Study Timer", font=("Arial", 24, "bold"))
        title_label.pack(padx=20, pady=(20, 10))
        
        # Timer display
        self.timer_label = tk.Label(root, text="00:00", font=("Arial", 48))
        self.timer_label.pack(padx=20, pady=(0, 20))
        
        # Button frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        # Buttons
        self.start_button = tk.Button(button_frame, text="Start", command=self.start, 
                                       font=("Arial", 14), width=8)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop, 
                                      font=("Arial", 14), width=8, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)
        
        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset, 
                                       font=("Arial", 14), width=8)
        self.reset_button.grid(row=0, column=2, padx=5)
        
        self.update_timer()
    
    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
    
    def stop(self):
        if self.running:
            self.running = False
            self.elapsed_time += time() - self.start_time
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.start_time = None
        self.timer_label.config(text="00:00")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def update_timer(self):
        if self.running:
            total_time = self.elapsed_time + (time() - self.start_time)
        else:
            total_time = self.elapsed_time
        
        minutes, seconds = divmod(int(total_time), 60)
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        self.root.after(100, self.update_timer)

root = tk.Tk()
app = TimerApp(root)
root.mainloop()