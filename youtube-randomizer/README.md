# YouTube Video Randomizer

## Why I built this
I wanted to watch some of my favorite YouTubers' older videos while waiting for them to upload again, but I never knew which one to pick. So I built a randomizer that grabs every video from a channel and displays 10 random clickable thumbnails in a dark mode GUI. This was also my first time working with an API and building a desktop GUI, which was a cool experience.

The only current limitation is that it doesn't separate YouTube Shorts from full length videos, so you may occasionally get a Short.

## Libraries used
* `build` from `googleapiclient.discovery` — the main function used to connect to any Google API. You pass in the API name, version, and your key to build a service object that lets you make API calls
* `load_dotenv` from `dotenv` — reads the `.env` file so your API key can be accessed securely without being hardcoded into your script
* `random` — built into Python, used to pick random videos from the full list
* `os` — built into Python, used to read environment variables from the `.env` file with `os.getenv()`
* `tkinter` — built into Python, used to build the desktop GUI window, buttons, labels, and input box
* `ImageTk` and `Image` from `PIL` (Pillow) — handles downloading, converting, and resizing the thumbnail images so tkinter can display them
* `BytesIO` from `io` — wraps the raw bytes from `requests.get()` into a file-like object so PIL's `Image.open()` can read it. PIL expects a file, not raw bytes
* `requests` — downloads the thumbnail image content from each thumbnail URL
* `webbrowser` — opens the YouTube video URL in a new browser tab when a thumbnail is clicked
* `json` — reads and writes the cache files so the video list can be saved and loaded without making API calls every time
* `datetime` and `timedelta` from `datetime` — used to track when the cache was created and check if it is older than 24 hours

## Setup

### Getting an API key
1. Go to [console.cloud.google.com](https://console.cloud.google.com) and create a new project
2. Search for **YouTube Data API v3** and enable it
3. Go to **Credentials** and create an API key
4. Copy the key — you'll need it in the next step

### Storing your API key
Never hardcode your API key directly in your script — anyone who sees your code can use it and burn through your quota.

Instead, create a `.env` file in your project folder:
```
API_KEY=your_api_key_here
```

Then create a `.gitignore` file in the same folder and add:
```
.env
```

This tells Git to never upload your `.env` file to GitHub. Your key stays local and private.

In the script, the key is loaded like this:
```python
load_dotenv()
api_key = os.getenv('API_KEY')
```
`load_dotenv()` reads the `.env` file and `os.getenv('API_KEY')` retrieves the value stored under that variable name.

### Install dependencies
```bash
pip install google-api-python-client python-dotenv pillow
```

## How it works

### Building the service
```python
service = build('youtube', 'v3', developerKey=api_key)
```
This creates the YouTube API service object. `'youtube'` is the API name, `'v3'` is the version, and `developerKey` is your API key. All API calls are made through this `service` object.

Note: Google APIs don't fire a request when you build the call — you have to call `.execute()` to actually send it. This applies to every API call in this project.

### `get_channel_id(username)`
Takes a YouTube handle and returns the channel's **uploads playlist ID**. Every YouTube channel has an uploads playlist automatically — it contains every video they've ever posted, which is more reliable than using the search endpoint.

The function calls `service.channels().list()` with two parts:
- `snippet` — basic channel info
- `contentDetails` — contains the uploads playlist ID nested inside `relatedPlaylists`

The response comes back as JSON — a nested dictionary. To get the uploads playlist ID you navigate through it like a file path: `response['items'][0]['contentDetails']['relatedPlaylists']['uploads']`

### `get_videos(playlist_id, username)`
Takes the uploads playlist ID and username, and returns every video in the channel. Before making any API calls it first checks for a valid cache by calling `load_cache(username)`. If the cache exists and is less than 24 hours old it returns the cached videos immediately without touching the API. If not, it makes the API calls as normal, saves the results with `save_cache()`, then returns the videos.

The API has a maximum of 50 results per request, so pagination is needed to get the full catalog:
1. An empty `all_videos` list is created to collect everything
2. `next_page_token` starts as `None` since there's no token yet
3. A `while True` loop keeps calling the API with `maxResults=50` and the current `pageToken`
4. Each response's items are added to `all_videos` using `.extend()`
5. If the response contains a `nextPageToken`, it updates the token and loops again
6. If there's no `nextPageToken`, the loop breaks, the results are cached, and `all_videos` is returned

For a large channel like CoryxKenshin this means 1,700+ videos across 35+ API calls — but only on the first search. After that it loads from cache instantly.

### `get_random_video(videos)`
Takes the full list of videos and returns 10 random picks. It loops 10 times using `range(10)`, picking a random video each time with `random.choice()`. For each pick it extracts three things from the video's `snippet` and appends them to separate lists:
- The YouTube URL built from the video ID
- The thumbnail URL using `'medium'` quality for better resolution
- The video title

All three lists are returned together as a tuple.

The `_` in `for _ in range(10)` is a Python convention meaning "I don't need the loop variable, I just want to repeat this 10 times."

### `save_cache(username, videos)`
Saves the full video list to a JSON file named after the YouTuber (e.g. `CoryxKenshin.json`) so the same data can be reused without calling the API again. The file stores two things — the videos and the current timestamp using `datetime.now().isoformat()`. The timestamp has to be converted to a string with `.isoformat()` because JSON can only store strings, not datetime objects.

`json.dump(data, file)` writes the dictionary directly to the file.

### `load_cache(username)`
Opens the YouTuber's JSON cache file and checks if it is still valid. It subtracts the saved timestamp from the current time to get how old the cache is. If it is less than 24 hours old it returns the cached videos. If it is expired or the file doesn't exist it returns `None`, which tells `get_videos()` to make fresh API calls.

`datetime.fromisoformat()` converts the timestamp string back into a datetime object so the math can be done on it. `timedelta(hours=24)` represents a 24 hour duration to compare against.

The cache file is never automatically deleted — it just gets overwritten with fresh data the next time an expired search is made.

### `window_gui()`
Builds and launches the dark mode GUI. `root = tk.Tk()` creates the main window. `root.overrideredirect(True)` removes the title bar since it didn't match the dark mode aesthetic. `root.attributes('-topmost', True)` keeps the window on top so it doesn't fall behind other windows. `root.geometry()` sets the size and position — the coordinates are manually calculated to center it on a 2560x1440 display.

The GUI uses `.grid()` for layout, which places widgets at specific row and column positions. `sticky='e'` and `sticky='w'` pin widgets to the east (right) or west (left) side of their cell.

A `tk.Frame` is used as a container for all the thumbnails and titles. When a new search is made the frame is destroyed and recreated with fresh content — this is why `nonlocal frame` is needed inside `load_thumbnails()`, to tell Python to update the outer `frame` variable instead of creating a new local one.

**`search_channel()`** is a nested function inside `window_gui()` so it has access to `user_input` and `frame`. It reads the YouTuber's name from the input box with `user_input.get()`, chains through `get_channel_id()`, `get_videos()`, and `get_random_video()` to get the new data, then calls `load_thumbnails()` to update the GUI.

**`load_thumbnails(urls, thumbnails, titles)`** is another nested function that destroys the old frame, creates a new one, and fills it with 10 thumbnail images and titles. For each thumbnail it downloads the image content with `requests.get(thumbnail).content`, converts the raw bytes to a PIL image using `BytesIO`, resizes it to 240x135 (YouTube's 16:9 ratio) using `Image.LANCZOS` for quality, then converts it to a tkinter-compatible image with `ImageTk.PhotoImage()`.

`thumbnail_label.image = convert_tk` keeps a reference to each image so Python's garbage collector doesn't delete them from memory — without this only the last image would show.

The grid positions are calculated mathematically:
- `row = (i // 5) * 2 + 1` — floor division keeps the first 5 in row 1 and the next 5 in row 3, with titles filling the even rows in between
- `col = i % 5` — modulo resets the column back to 0 after every 5 items

Each thumbnail is bound to a left click using `bind('<Button-1>', lambda event, u=urls[i]: webbrowser.open_new_tab(u))`. The `u=urls[i]` captures the correct URL at that moment in the loop — without it every thumbnail would open the last URL due to how Python handles loop variables in lambdas.

`root.mainloop()` keeps the window running and listening for events. Without it the window would open and immediately close.

## What I learned
* How to connect to and use a real API for the first time
* How to store and access API keys securely using `.env` and `.gitignore`
* How Google's API client works — building a call vs executing it
* How JSON responses are structured and how to navigate nested dictionaries
* How pagination works and how to loop through multiple pages of API results
* The difference between `forUsername` and `forHandle` for YouTube channels
* How to chain multiple functions together so each one feeds into the next
* How `enumerate()` numbers items in a list and why two variables are needed to unpack it
* The `_` convention for loop variables you don't need
* How to build a desktop GUI with tkinter including grid layout, buttons, labels, and input boxes
* How PIL handles image downloading, conversion, resizing, and display in tkinter
* Why `thumbnail_label.image = convert_tk` is needed to prevent garbage collection
* How `nonlocal` works and when you need it in nested functions
* How lambda functions work and why `u=urls[i]` is needed to capture loop variables correctly
* How to implement a file-based caching system using JSON and datetime comparison
* How `datetime.isoformat()` and `datetime.fromisoformat()` convert between datetime objects and strings

## Future improvements
* Filter out YouTube Shorts so only full length videos are returned
* Add error handling with `try/except` in case a channel isn't found
* Add a loading indicator while the API calls and thumbnails are downloading
* Use threading to load thumbnails simultaneously instead of one at a time for faster startup
* Support `customtkinter` for a fully themed dark mode including the title bar
