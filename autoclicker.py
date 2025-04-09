import tkinter as tk
import pyautogui
import asyncio
import keyboard
import os
import sys

class main():
    def __init__(self):
        self.VERSION = "V1.0"

        self.window = tk.Tk()
        self.window.title(f"AutoClicker {self.VERSION}")
        self.window.minsize(450, 325)
        self.window.maxsize(450, 325)
        self.window.geometry("300x300")

        self.clicking = False
        self.totalClickingTime = 0
        self.x = 0

        self.hotkey = "F6"
        
        self.setup()
        self.bind_hotkeys()

        self.window.mainloop()
    
    def setup(self):
        clickingIntervalFrame = tk.Frame(self.window, width=430, height=50, highlightbackground="grey", highlightthickness=0.5)
        clickingIntervalFrame.pack(padx=0, pady=15)

        clickingIntervalLabel = tk.Label(self.window, text="Clicking Interval")
        clickingIntervalLabel.place(relx=0.13, rely=0.05, anchor=tk.CENTER)

        vcmd = (self.window.register(self.validateInput), "%P")

        self.hoursEntry = tk.Entry(clickingIntervalFrame, width=7, justify="right", validate="key", validatecommand=vcmd)
        self.hoursEntry.place(relx=0.07, rely=0.5, anchor=tk.CENTER)
        self.hoursEntry.insert(0, "0")

        hoursLabel = tk.Label(clickingIntervalFrame, text="hours")
        hoursLabel.place(relx=0.18, rely=0.5, anchor=tk.CENTER)

        self.minsEntry = tk.Entry(clickingIntervalFrame, width=7, justify="right", validate="key", validatecommand=vcmd)
        self.minsEntry.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
        self.minsEntry.insert(0, "0")

        minsLabel = tk.Label(clickingIntervalFrame, text="mins")
        minsLabel.place(relx=0.4, rely=0.5, anchor=tk.CENTER)

        self.secsEntry = tk.Entry(clickingIntervalFrame, width=7, justify="right", validate="key", validatecommand=vcmd)
        self.secsEntry.place(relx=0.52, rely=0.5, anchor=tk.CENTER)
        self.secsEntry.insert(0, "0")

        secsLabel = tk.Label(clickingIntervalFrame, text="secs")
        secsLabel.place(relx=0.62, rely=0.5, anchor=tk.CENTER)

        self.millisecondsEntry = tk.Entry(clickingIntervalFrame, width=7, justify="right", validate="key", validatecommand=vcmd)
        self.millisecondsEntry.place(relx=0.72, rely=0.5, anchor=tk.CENTER)
        self.millisecondsEntry.insert(0, "100")

        millisecondsLabel = tk.Label(clickingIntervalFrame, text="milliseconds")
        millisecondsLabel.place(relx=0.87, rely=0.5, anchor=tk.CENTER)

        self.startClickerButton = tk.Button(self.window, text="Start", width=25, height=2, bg="white", command=lambda: self.startClicking(self.hoursEntry.get(), self.minsEntry.get(), self.secsEntry.get(), self.millisecondsEntry.get()))
        self.startClickerButton.place(relx=0.25, rely=0.75, anchor=tk.CENTER)

        self.stopClickerButton = tk.Button(self.window, text="Stop", width=25, height=2, bg="white", command=self.stopClicking)
        self.stopClickerButton.place(relx=0.75, rely=0.75, anchor=tk.CENTER)
        self.stopClickerButton.config(state=tk.DISABLED, bg="#F9F9F9", fg="black")

        self.hotkeyButton = tk.Button(self.window, text="Hotkey setting", width=25, height=2, bg="white", command=self.menu_hotkeys)
        self.hotkeyButton.place(relx=0.25, rely=0.92, anchor=tk.CENTER)


        clickingTypeFrame = tk.Frame(self.window, width=215, height=100, highlightbackground="grey", highlightthickness=0.5)
        clickingTypeFrame.pack(padx=10, pady=5, anchor="nw")

        clickingTypeLabel = tk.Label(self.window, text="Click Options")
        clickingTypeLabel.place(relx=0.13, rely=0.26, anchor=tk.CENTER)

        options = tk.StringVar()
        self.mouseButtonDropDown = tk.OptionMenu(clickingTypeFrame, options, 'Left', 'Right', 'Middle', command=self.mouseButtonDropDown)   
        options.set('Left')
        self.mouseButtonDropDown.place(relx=0.6, rely=0.3, anchor=tk.CENTER)

        mouseButtonLabel = tk.Label(clickingTypeFrame, text="Mouse Button:")
        mouseButtonLabel.place(relx=0.21, rely=0.3, anchor=tk.CENTER)
    
    def mouseButtonDropDown(choice):
        print("Selected:", choice)

    def validateInput(self, input_value):
        return input_value.isdigit()

    def startClicking(self, hours=0, mins=0, secs=0, milli=0):
        self.clicking = True
        self.startClickerButton.config(state=tk.DISABLED, bg="#F9F9F9", fg="black")
        self.stopClickerButton.config(state=tk.NORMAL, bg="#FFFFFF", fg="black")
        
        hours = int(hours) if hours.isdigit() else 0
        mins = int(mins) if mins.isdigit() else 0
        secs = int(secs) if secs.isdigit() else 0
        milli = int(milli) if milli.isdigit() else 0

        self.totalClickingTime = (hours * 3600000) + (mins * 60000) + (secs * 1000) + milli
        
        if self.totalClickingTime <= 0:
            print("Total clicking time cannot be 0 seconds!")
            self.startClickerButton.config(state=tk.NORMAL, bg="#FFFFFF", fg="black")
            self.stopClickerButton.config(state=tk.DISABLED, bg="#F9F9F9", fg="black")
        else:
            print(f"Total clicking time set to: {self.totalClickingTime} milliseconds.")
            self.x = 0
            self.click()

    def stopClicking(self):
        self.clicking = False
        self.startClickerButton.config(state=tk.NORMAL, bg="#FFFFFF", fg="black")
        self.stopClickerButton.config(state=tk.DISABLED, bg="#F9F9F9", fg="black")
        print("Stopped")

    def click(self):
        if self.clicking:
            self.x += 1
            print(f"{self.x} - Running for {self.totalClickingTime} milliseconds")
            pyautogui.click(pyautogui.position())
            self.window.after(self.totalClickingTime, self.click)

    def menu_hotkeys(self):
        hotkey_window = tk.Toplevel(self.window)
        hotkey_window.title("Hotkey Settings")

        self.window.update_idletasks()
        pos_x = self.window.winfo_x() + (self.window.winfo_width() // 2) - (225 // 2)
        pos_y = self.window.winfo_y() + (self.window.winfo_height() // 2) - (225 // 2)
        hotkey_window.geometry(f"225x100+{pos_x}+{pos_y}")

        self.new_hotkey = ""

        def set_hotkey():
            key_label.config(text="Please Key")

            def on_key_press(e):
                self.new_hotkey = e.name
                key_label.config(text=self.new_hotkey)
                keyboard.unhook_all()

            keyboard.on_press(on_key_press)

        def save_changes():
            if self.new_hotkey:
                self.hotkey = self.new_hotkey
            self.bind_hotkeys()
            hotkey_window.destroy()

        def cancel_changes():
            hotkey_window.destroy()

        key_label = tk.Label(hotkey_window,text=f"{self.hotkey}", width=13, height=2, bg="#F9F9F9", highlightbackground="grey", highlightthickness=0.5)
        key_label.place(relx=0.75, rely=0.25, anchor=tk.CENTER)

        # Define key_button before setting its command
        key_button = tk.Button(hotkey_window, text="Start / Stop", width=13, height=2, bg="white", command=set_hotkey)
        key_button.place(relx=0.25, rely=0.25, anchor=tk.CENTER)

        save_button = tk.Button(hotkey_window, text="Ok", width=5, height=1, bg="white", command=save_changes)
        save_button.place(relx=0.25, rely=0.7, anchor=tk.CENTER)

        cancel_button = tk.Button(hotkey_window, text="Cancel", width=5, height=1, bg="white", command=cancel_changes)
        cancel_button.place(relx=0.75, rely=0.7, anchor=tk.CENTER)


    def bind_hotkeys(self):
        try:
            keyboard.remove_hotkey(self.hotkey)
        except KeyError:
            pass

        def toggle_clicking():
            if not self.clicking:
                self.startClicking(self.hoursEntry.get(), self.minsEntry.get(), self.secsEntry.get(), self.millisecondsEntry.get())
            else:
                self.stopClicking()

        keyboard.add_hotkey(self.hotkey, toggle_clicking, suppress=True)

        self.startClickerButton.config(text=f"Start [{self.hotkey}]")
        self.stopClickerButton.config(text=f"Stop [{self.hotkey}]")

        print(f"Hotkey set: {self.hotkey} to toggle clicking")

main()
