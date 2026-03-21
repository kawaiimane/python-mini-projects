from pathlib import Path
import shutil

locate_folder = Path(r'C:\Users\cmveg\Desktop\test folder\test')

extensions = {
    '.mp3': 'music',
    '.mp4': 'video',
    '.jpg': 'image',
    '.txt': 'text',
    '.csv': 'source',
    '.pdf': 'document'
}

for file in locate_folder.iterdir():

    file_type = extensions.get(file.suffix, 'misc')

    destination = locate_folder / file_type
    destination.mkdir(parents=True, exist_ok=True)

    shutil.move(file, destination)
