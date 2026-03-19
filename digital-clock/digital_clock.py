import time
import tkinter as tk


window = tk.Tk()
window.withdraw()
window.geometry("150x30")

label = tk.Label(window, text="")
label.pack()


def clock():
    label.config(text=time.strftime("%I:%M:%S %p"))
    window.after(1000, clock)


clock()

window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry(f"{width}x{height}+{x}+{y}")
window.deiconify()
window.mainloop()
