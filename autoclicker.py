import tkinter as tk, pyautogui, asyncio

class main():
    def __init__(self):
        self.VERSION = "V1.0"

        self.window = tk.Tk()
        self.window.title(f"AutoClicker {self.VERSION}")
        self.window.minsize(450, 325)
        self.window.maxsize(450, 325)
        self.window.geometry("300x300+50+50")

        self.clicking = False
        self.totalClickingTime = 0
        self.x = 0
        
        self.setup()

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
        self.millisecondsEntry.insert(0, "0")

        millisecondsLabel = tk.Label(clickingIntervalFrame, text="milliseconds")
        millisecondsLabel.place(relx=0.87, rely=0.5, anchor=tk.CENTER)

        self.startClickerButton = tk.Button(self.window, text="Start", width=25, height=2, bg="white", command=lambda: self.startClicking(self.hoursEntry.get(), self.minsEntry.get(), self.secsEntry.get(), self.millisecondsEntry.get()))
        self.startClickerButton.place(relx=0.25, rely=0.75, anchor=tk.CENTER)

        self.stopClickerButton = tk.Button(self.window, text="Stop", width=25, height=2, bg="white", command=self.stopClicking)
        self.stopClickerButton.place(relx=0.75, rely=0.75, anchor=tk.CENTER)
        self.stopClickerButton.config(state=tk.DISABLED, bg="#F9F9F9", fg="black")

    def validateInput(self, input_value):
            if input_value.isdigit():
                return True
            else:
                return False

    def startClicking(self, hours=0, mins=0, secs=0, milli=0):
        self.clicking = True
        self.startClickerButton.config(state=tk.DISABLED, bg="#F9F9F9", fg="black")
        self.stopClickerButton.config(state=tk.NORMAL, bg="#FFFFFF", fg="black")
        
        hours = int(hours) if hours.isdigit() else 0
        mins = int(mins) if mins.isdigit() else 0
        secs = int(secs) if secs.isdigit() else 0
        milli = int(milli) if milli.isdigit() else 0

        self.totalClickingTime = (hours * 3600000) + (mins * 60000) + (secs * 1000) + milli
        
        if self.totalClickingTime < 0:
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


main()
