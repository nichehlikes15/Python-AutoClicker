import tkinter as tk
import pyautogui
import asyncio
import keyboard
import os
import sys

class main():
    def __init__(self):
        self.VERSION = "V1.1"

        self.window = tk.Tk()
        self.window.title(f"AutoClicker {self.VERSION}")
        self.window.minsize(450, 325)
        self.window.maxsize(450, 325)
        self.window.geometry("300x300")

        self.clicking = False
        self.totalClickingTime = 0
        self.x = 0

        self.hotkey = "f6"
        self.clicking_places = None
        
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

        self.instanceClickerButton = tk.Button(self.window, text="Multiple Clicker", width=25, height=2, bg="white", command=self.multiple_clicker)
        self.instanceClickerButton.place(relx=0.75, rely=0.92, anchor=tk.CENTER)


        clickingTypeFrame = tk.Frame(self.window, width=215, height=100, highlightbackground="grey", highlightthickness=0.5)
        clickingTypeFrame.pack(padx=10, pady=5, anchor="nw")

        clickingTypeLabel = tk.Label(self.window, text="Click Options")
        clickingTypeLabel.place(relx=0.13, rely=0.26, anchor=tk.CENTER)

        mouseButtonLabel = tk.Label(clickingTypeFrame, text="Mouse Button:")
        mouseButtonLabel.place(relx=0.23, rely=0.225, anchor=tk.CENTER)

        mouseButtonLabelOptions = tk.StringVar()
        self.mouseButtonDropDown = tk.OptionMenu(clickingTypeFrame, mouseButtonLabelOptions, 'Left', 'Right', 'Middle', command=self.mouseButtonDropDown)   
        mouseButtonLabelOptions.set('Left')
        self.mouseButtonDropDown.place(relx=0.6, rely=0.225, anchor=tk.CENTER)
    
    def mouseButtonDropDown(choice):
        print("Selected:", choice)

    def validateInput(self, input_value):
        return input_value.isdigit() or input_value == ""


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
            print(f"Running for {self.totalClickingTime} milliseconds")

            if self.clicking_places:
                for pos in self.clicking_places:
                    pyautogui.click(pos)
                    print(f"Clicked at {pos}")
            else:
                pyautogui.click(pyautogui.position())
                print(f"Clicked at current mouse position")

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

        key_label = tk.Label(hotkey_window,text=f"{self.hotkey.upper()}", width=13, height=2, bg="#F9F9F9", highlightbackground="grey", highlightthickness=0.5)
        key_label.place(relx=0.75, rely=0.25, anchor=tk.CENTER)

        # Define key_button before setting its command
        key_button = tk.Button(hotkey_window, text="Start / Stop", width=13, height=2, bg="white", command=set_hotkey)
        key_button.place(relx=0.25, rely=0.25, anchor=tk.CENTER)

        save_button = tk.Button(hotkey_window, text="Ok", width=5, height=1, bg="white", command=save_changes)
        save_button.place(relx=0.25, rely=0.7, anchor=tk.CENTER)

        cancel_button = tk.Button(hotkey_window, text="Cancel", width=5, height=1, bg="white", command=cancel_changes)
        cancel_button.place(relx=0.75, rely=0.7, anchor=tk.CENTER)

    def multiple_clicker(self):
        multiple_clicker = tk.Toplevel(self.window)
        multiple_clicker.title("Multiple Clicker Settings")

        self.window.update_idletasks()
        pos_x = self.window.winfo_x() + (self.window.winfo_width() // 2) - (225 // 2)
        pos_y = self.window.winfo_y() + (self.window.winfo_height() // 2) - (225 // 2)
        multiple_clicker.geometry(f"225x100+{pos_x}+{pos_y}")

        def save_changes():
            clicking_places = key_label.get()
            multiple_clicker.destroy()
            if int(clicking_places) > 0:
                self.set_clicking_places(clicking_places)

        def cancel_changes():
            multiple_clicker.destroy()

        vcmd = (self.window.register(self.validateInput), "%P")

        #self.minsEntry = tk.Entry(clickingIntervalFrame, width=7, justify="right", validate="key", validatecommand=vcmd)
        #self.minsEntry.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
        #self.minsEntry.insert(0, "0")

        #key_label = tk.Entry(hotkey_window, width=13, height=2, bg="#F9F9F9", highlightbackground="grey", highlightthickness=0.5, validatecommand=vcmd)
        key_label = tk.Entry(multiple_clicker, width=7, justify="center", validate="key", validatecommand=vcmd)
        key_label.place(relx=0.75, rely=0.25, anchor=tk.CENTER)
        key_label.insert(0, 2)
        key_label.focus()

        key_button = tk.Label(multiple_clicker, text="Number of\nplaces to click:", width=13, height=2, bg="white")
        key_button.place(relx=0.25, rely=0.25, anchor=tk.CENTER)

        save_button = tk.Button(multiple_clicker, text="Ok", width=5, height=1, bg="white", command=save_changes)
        save_button.place(relx=0.25, rely=0.7, anchor=tk.CENTER)

        cancel_button = tk.Button(multiple_clicker, text="Cancel", width=5, height=1, bg="white", command=cancel_changes)
        cancel_button.place(relx=0.75, rely=0.7, anchor=tk.CENTER)

    def set_clicking_places(self, places):
        place_number = 0
        self.clicking_places = []

        set_clicking_places_window = tk.Toplevel(self.window)
        set_clicking_places_window.title("Clicking Places")

        self.window.update_idletasks()
        pos_x = self.window.winfo_x() + (self.window.winfo_width() // 2) - (225 // 2)
        pos_y = self.window.winfo_y() + (self.window.winfo_height() // 2) - (225 // 2)
        set_clicking_places_window.geometry(f"225x100+{pos_x}+{pos_y}")

        self.new_hotkey = ""

        def set_hotkey():
            key_label.config(text="Set Location [C]")

            def on_key_press(e):
                if e.name == 'c':
                    position = pyautogui.position()
                    self.clicking_places.append(position)
                    key_label.config(text=position)
                    keyboard.unhook_all()

            keyboard.on_press(on_key_press)

        def save_changes():
            nonlocal place_number
            if self.clicking_places[place_number]:
                if place_number + 1 >= int(places):
                    set_clicking_places_window.destroy()
                else:
                    place_number += 1
                    key_label.config(text=f"Place {place_number+1}: Not Set")
                    key_button.config(text=f"Set Click Place {place_number + 1}")
                    #save_button.config(text=f"Set place {place_number+1}")
            else:
                print("clicking place has not been set yet!")

        def cancel_changes():
            set_clicking_places_window.destroy()

        key_label = tk.Label(set_clicking_places_window,text=f"Place {place_number+1}: Not Set", width=13, height=2, bg="#F9F9F9", highlightbackground="grey", highlightthickness=0.5)
        key_label.place(relx=0.75, rely=0.25, anchor=tk.CENTER)

        # Define key_button before setting its command
        key_button = tk.Button(set_clicking_places_window, text=f"Set Click Place {place_number + 1}", width=13, height=2, bg="white", command=set_hotkey)
        key_button.place(relx=0.25, rely=0.25, anchor=tk.CENTER)

        save_button = tk.Button(set_clicking_places_window, text=f"Ok", width=5, height=1, bg="white", command=save_changes)
        save_button.place(relx=0.25, rely=0.7, anchor=tk.CENTER)

        cancel_button = tk.Button(set_clicking_places_window, text="Cancel", width=5, height=1, bg="white", command=cancel_changes)
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

        self.startClickerButton.config(text=f"Start [{self.hotkey.upper()}]")
        self.stopClickerButton.config(text=f"Stop [{self.hotkey.upper()}]")

        print(f"Hotkey set: {self.hotkey} to toggle clicking")

main()
