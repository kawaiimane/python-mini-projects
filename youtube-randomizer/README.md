# YouTube Video Randomizer

## Why I built this
I wanted to watch some of my favorite YouTubers' older videos while waiting for them to upload again, but I never knew which one to pick. So I built a randomizer that grabs every video from a channel and gives you 10 random links to watch. This was also my first time working with an API, which was a cool experience.

The only current limitation is that it doesn't separate YouTube Shorts from full length videos, so you may occasionally get a Short.

## Libraries used
* `build` from `googleapiclient.discovery` — the main function used to connect to any Google API. You pass in the API name, version, and your key to build a service object that lets you make API calls
* `load_dotenv` from `dotenv` — reads the `.env` file so your API key can be accessed securely without being hardcoded into your script
* `random` — built into Python, used to pick random videos from the full list
* `os` — built into Python, used to read environment variables from the `.env` file with `os.getenv()`

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
pip install google-api-python-client python-dotenv
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

### `get_videos(playlist_id)`
Takes the uploads playlist ID and returns every video in it. The API has a maximum of 50 results per request, so pagination is needed to get the full catalog.

Here's how it works:
1. An empty `all_videos` list is created to collect everything
2. `next_page_token` starts as `None` since there's no token yet
3. A `while True` loop keeps calling the API with `maxResults=50` and the current `pageToken`
4. Each response's items are added to `all_videos` using `.extend()`
5. If the response contains a `nextPageToken`, it updates the token and loops again
6. If there's no `nextPageToken`, the loop breaks and `all_videos` is returned

This continues until every page has been collected — for a large channel like CoryxKenshin this means 1,700+ videos across 35+ API calls.

### `get_random_video(videos)`
Takes the full list of videos and returns 10 random YouTube URLs. It loops 10 times using `range(10)`, picking a random video each time with `random.choice()` and appending the full URL to a list. The video ID is extracted by navigating the nested dictionary: `video['snippet']['resourceId']['videoId']`.

The `_` in `for _ in range(10)` is a Python convention meaning "I don't need the loop variable, I just want to repeat this 10 times."

### Chaining it all together
```python
username = input('Enter a YouTube username: ')
playlist_id = get_channel_id(f'@{username}')
videos = get_videos(playlist_id)
urls = get_random_video(videos)
for i, url in enumerate(urls, 1):
    print(f'{i}) {url}\n')
```
The `@` is hardcoded so the user doesn't have to remember to include it. Each function feeds into the next — the username gets the playlist ID, the playlist ID gets the videos, the videos get randomized into 10 URLs. `enumerate()` is used to number each URL starting from 1, and a blank line is added after each one for readability.

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

## Future improvements
* Filter out YouTube Shorts so only full length videos are returned
* Add error handling with `try/except` in case a channel isn't found
* Let the user input multiple channels and pick a random video from any of them
* Cache the video list so repeat searches don't make hundreds of API calls
