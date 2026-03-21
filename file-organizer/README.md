# File Organizer

## What does this program do?
This program automatically organizes files in a folder by moving them into 
subfolders based on their file type. For example, `.mp3` files go into a 
`music` folder, `.jpg` files go into an `image` folder, and so on. Any file 
with an unrecognized extension gets moved into a `misc` folder.

## Libraries used
- `Path` from `pathlib` — defines and works with folder and file paths. 
  The `/` operator joins path segments together, making it easy to build 
  destination paths.
- `shutil` — handles the actual moving of files into their respective folders 
  using `shutil.move()`.
- `sys` — allows the folder path to be passed in from the terminal as a 
  command line argument, making the program usable by anyone without 
  modifying the code.

## How to run
```bash
python file_organizer.py "C:\Users\yourname\Desktop\your-folder"
```

## How it works
`sys.argv` is a list of everything typed in the terminal when running the 
script. `sys.argv[0]` is always the script name itself, and `sys.argv[1]` 
is the folder path passed in after it. This is wrapped in `Path()` to convert 
it into a proper path object.

A dictionary maps file extensions to folder names. The key is the extension 
and the value is the destination folder name, for example `'.mp3': 'music'`.

The `for` loop uses `.iterdir()` to go through every item in the folder one 
at a time — think of it as opening the folder and handing each file to the 
loop one by one.

For each file, `file.suffix` gets its extension and `extensions.get(file.suffix, 'misc')` 
looks it up in the dictionary. The `.get()` method is used instead of directly 
indexing the dictionary so that if the extension is not found, it defaults to 
`'misc'` instead of crashing with a `KeyError`.

The destination path is built by joining the source folder path with the folder 
name using the `/` operator. `destination.mkdir(parents=True, exist_ok=True)` 
creates the subfolder if it doesn't already exist — `exist_ok=True` prevents 
a crash if the folder is already there, and `parents=True` creates any missing 
parent folders along the way.

Finally `shutil.move(file, destination)` moves the current file into its 
destination folder.

## What I learned
- How to work with file paths using `pathlib` and the `Path` object
- How to use `sys.argv` to accept command line arguments for more flexible, 
  reusable code
- How to use a dictionary to map file extensions to folder names
- How `.iterdir()` loops through files in a folder
- How `.get()` on a dictionary provides a default value instead of crashing 
  on unknown keys
- How `shutil.move()` moves files between directories
- How `mkdir(exist_ok=True)` safely creates folders without crashing if they 
  already exist
