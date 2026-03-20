# Digital Clock

## What does this program do?
This program displays a live digital clock in a small centered window that 
updates every second in 12 hour format with AM/PM.

## Libraries used
I imported `time` and `tkinter`. `time` gives us access to `time.strftime()` 
to get the current local time. `tkinter` allows us to create a desktop window 
and display the clock as a label.

## How it works
A tkinter window is created and a label is placed inside it as a placeholder. 
The `clock()` function uses `label.config()` to update the label's text with 
the current time using `time.strftime("%I:%M:%S %p")`, where `%I` is 12 hour 
time, `%M` is minutes, `%S` is seconds, and `%p` is AM/PM. `window.after(1000, clock)` 
calls the function again every 1000 milliseconds, creating a continuous update loop. 
Note that `clock` is passed without parentheses — writing `clock` passes the function 
itself to be called later, while writing `clock()` would call it immediately and pass 
the result instead.

The window is centered by first calling `window.update_idletasks()` to force 
tkinter to finish all pending calculations before taking measurements. The 
window's width and height are then stored in variables using `winfo_width()` 
and `winfo_height()`. The correct x and y coordinates are calculated by taking 
half the monitor's dimensions using `winfo_screenwidth()` and 
`winfo_screenheight()` and subtracting half the window's dimensions, placing 
it exactly in the center. `//` is used instead of `/` to return a whole number 
instead of a float. 

Finally `window.geometry()` sets both the size and position 
in one call using an f-string. `window.withdraw()` hides the window during this 
setup and `window.deiconify()` reveals it already centered, preventing a visual 
flash.

## What I learned
- How to create a basic desktop window using `tkinter`
- How to use `time.strftime()` to get and format the current local time
- How `window.after()` works to repeatedly call a function without blocking the program
- How to calculate screen coordinates to center a window
- How to use `withdraw()` and `deiconify()` to prevent a visual flash on startup
