import time
from art import *
import sys
from contextlib import redirect_stdout
import io
import threading
import os
import tkinter as tk
from tkinter import messagebox
# ==============================================================================================

# | Welcome to the Pomodoro Timer! This Pomodoro Timer helps you focus using timed   |
# | work and break sessions.       
# | Enter 'Start' to begin the timer:     
# 

def clear_screen():
    # Check the operating system name
    if os.name == 'nt':
        # for Windows
        _ = os.system('cls')
    else:
        #  Linux/macOS
        _ = os.system('clear')

def replace_previous_block(lines):
    if lines <= 0:
        return
    print(f"\033[{lines}A", end="")

    # clear each line, moving down through the block
    for i in range(lines):
        print("\033[2K\r", end="")          # clear whole line + carriage return
        if i < lines - 1:
            print("\033[1B", end="")       # move down 1 line

    # Go back up to the top of the cleared block
    if lines > 1:
        print(f"\033[{lines - 1}A", end="")


def count_printed_lines(func):
    # create an in-memory text buffer
    captured_output = io.StringIO()

    # redirect stdout to the buffer while the function runs
    with redirect_stdout(captured_output):
        func()

    # get the entire value printed to the buffer as a string
    output_string = captured_output.getvalue()

    # Close the buffer 
    captured_output.close()
    
    # Handle the case where the function prints nothing
    if output_string == "":
        return 0
        
    return len(output_string.splitlines())

line = line(length=94, height=1, char="=")
lineWidth = 94

def welcomeScreen():
    welcome = text2art(" Pomodoro Timer ")

    print(line)
    print(welcome.rstrip('\n'))
    print(line)

    print("| Welcome to the Pomodoro Timer! This Pomodoro Timer helps you focus using timed             |")
    print("| work and break sessions.                                                                   |")
    print("|                                                                                            |")
    print("| 1. Start Work Session                                                                      |")
    print("| 2. Settings / Help / About                                                                 |")
    print("| 3. Quit                                                                                    |")
    print(line)

line_count = count_printed_lines(welcomeScreen)

welcomeScreen()

def workSession(timeStr):
    clear_screen()
    workTitle = text2art(" Work Session ")
    if workTitle.endswith("\n"):
        workTitle = workTitle[:-1]
    centerTitle = "\n".join(line.center(lineWidth) for line in workTitle.split("\n"))
    print(line)
    print(centerTitle)
    print(line)
    print(f"| Enter the corresponding number to select!".ljust(lineWidth-1) + "|")
    print(f"|".ljust(lineWidth - 1) + "|")
    print(f"| State: RUNNING".ljust(lineWidth-1) + "|")
    print(f"| Time Remaining: {timeStr}".ljust(lineWidth-1) + "|")
    print(f"|".ljust(lineWidth - 1) + "|")
    print(f"| Session x of x".ljust(lineWidth - 1) + "|")
    print(f"| 1. Pause".ljust(lineWidth - 1) + "|")
    print(f"| 2. Home".ljust(lineWidth - 1) + "|")
    print(f"| 3. Help ".ljust(lineWidth - 1) + "|")
    print(line)

def pauseSession(timeStr):
    clear_screen()
    pauseTitle = text2art(" Paused ")

    if pauseTitle.endswith("\n"):
        pauseTitle = pauseTitle[:-1]

    centerPauseTitle = "\n".join(line.center(lineWidth) for line in pauseTitle.split("\n"))
    print(line)
    print(centerPauseTitle)
    print(line)
    print(f"| Enter the corresponding number to select!".ljust(lineWidth-1) + "|")
    print(f"|".ljust(lineWidth - 1) + "|")
    print(f"| State: PAUSED".ljust(lineWidth-1) + "|") 
    print(f"| Time Remaining: {timeStr}".ljust(lineWidth-1) + "|")
    print(f"|".ljust(lineWidth - 1) + "|")
    print(f"| Session x of x".ljust(lineWidth - 1) + "|")
    print(f"| 1. Resume".ljust(lineWidth - 1) + "|")
    print(f"| 2. Home".ljust(lineWidth - 1) + "|")
    print(f"| 3. Help ".ljust(lineWidth - 1) + "|")
    print(line)
            

homeInput = (input("Enter the corresponding number to execute the action: "))
homeCommands = ["1", "2", "3"]

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

confirm_pause = Confirmations("Confirm", "askyesno", "Are you sure you want to pause the timer?")
confirm_unpause = Confirmations("Confirm", "askyesno", "Are you sure you want to uspause the timer?")
cmd_invalid = Confirmations("Input Invalid", "showerror", "That command does not exist. Please try again!") 

def handlePauseCommand(session):
    if not session.pause_event.is_set():  # currently running
        if confirm_pause.window():
            session.toggle_pause()
            with session.print_lock:
                clear_screen()
                pauseSession(session.format_time(session.remaining_seconds))
    else: 
        if confirm_unpause.window():
            session.toggle_pause()
            with session.print_lock:
                clear_screen()
                workSession(session.format_time(session.remaining_seconds))

class Session():
    
    def __init__(self, session_type, total_duration, status):
        self.session_type = session_type
        self.total_duration = int(total_duration) * 60 
        self.status = status

        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.print_lock = threading.Lock()  # NEW: "printing in progress" lock

        self.remaining_seconds = self.total_duration

    def info(self):
        return '{} {} {}'.format(self.session_type, self.total_duration, 
                                     self.status)


    def start(self):
        while self.remaining_seconds > 0 and not self.stop_event.is_set():
            if self.pause_event.is_set():
                time.sleep(0.5)
                continue

            formatted = self.format_time(self.remaining_seconds)
            timer_line = (f"| Time Remaining: {formatted}".ljust(lineWidth-1) + "|")
            status_line = (f"| State: {self.status}".ljust(lineWidth-1) + "|")

            if self.pause_event.is_set():
                continue
            
            # Acquire lock BEFORE printing - blocks pause from clearing
            with self.print_lock:
                print(f"\033[8A\r\033[2K", end="")
                print(status_line)
                print("\r\033[2K", end="")
                print(timer_line, end="", flush=True)
                print(f"\033[7B", end="", flush=True)
            # Lock automatically released here

            time.sleep(1)
            self.remaining_seconds -= 1

    def stop(self):
        self.stop_event.set()

    def toggle_pause(self):
        if self.pause_event.is_set():
            self.pause_event.clear()
            self.status = "RUNNING"
        else:
            self.pause_event.set()
            self.status = "PAUSED"

    def format_time(self, remaining_seconds):
        seconds = int(remaining_seconds % 60)
        minutes = int(remaining_seconds / 60) % 60
        hours = int(remaining_seconds / 3600)
        return (f"{hours:02}:{minutes:02}:{seconds:02}")


session_work = Session('WORK', '50', 'RUNNING')
session_break = Session('BREAK', '10', 'READY')

#print(session_work.info())
#print(session_break.info())

while homeInput not in homeCommands:
    if cmd_invalid.window():
        homeInput = (input("Enter the corresponding number to execute the action: "))
else:
    if homeInput == homeCommands[0]:
        clear_screen() 
        workSession(session_work.format_time(session_work.total_duration))
        
        # start timer in background thread
        timer_thread = threading.Thread(
            target=session_work.start,
            daemon=True
        )
        timer_thread.start()
        # Give the timer thread a moment to start
        time.sleep(1.1)

        while timer_thread.is_alive():
            print("\r\033[2K", end="")
            print("Enter the corresponding number to execute the action: ", end="", flush=True)
            
            cmd = input().strip()
            print("\033[1A\r\033[2K", end="", flush=True)  # Move up 1 to cancel Enter's newline, then clear
            print("\r\033[2K", end="")

            if cmd == "1":
                handlePauseCommand(session_work)
            elif cmd == "2":
                session_work.stop()
                break
            elif cmd == "3":
                print("Help: 1=pause/resume, 2=home, 3=help", flush=True)
                time.sleep(2)
            else:
                if cmd:
                    cmd_invalid.window()

    elif homeInput == homeCommands[1]:
        print("Settings / About / Help")
    else:
        print("Are you sure you want to quit?")
        
