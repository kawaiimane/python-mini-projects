# Anime Recommendation Engine

## Why I built this
I kept finishing anime I loved and had no idea what to watch next. I built this so I can type in any anime and get a list of similar recommendations with links to their MyAnimeList pages to read more about them.

## Libraries used
* `requests` — fetches data from the Jikan API by sending HTTP GET requests to a URL
* `time` — built into Python, used for `time.sleep(1)` which pauses the script for 1 second between API calls to avoid getting rate limited by Jikan

## API
This project uses the **Jikan API** (`https://api.jikan.moe/v4/`) — a free, open API for MyAnimeList data. No API key or account needed, which makes setup much simpler than APIs like YouTube's. The tradeoff is that Jikan rate limits requests, which is why `time.sleep(1)` is used after each call.

## How it works

### `search(title)`
Takes an anime title and returns its **MAL ID** — a unique number MyAnimeList assigns to every anime. This ID is needed to fetch recommendations in the next step.

It calls `requests.get()` with the search endpoint: `{base_url}anime?q={title}&limit=1`. The `limit=1` ensures only the closest match is returned.

`.json()` is a method from the `requests` library that converts the raw response into a Python dictionary so you can navigate it. The MAL ID is extracted by drilling into the nested dictionary: `response.json()['data'][0]['mal_id']`. The `[0]` grabs the first (and only) item in the results list since `limit=1` was used.

Error handling is done with `try/except`. If the anime isn't found, the API returns an empty list and accessing `[0]` raises an `IndexError`. The `except` block catches this and prints a friendly error message instead of crashing.

### `get_recommendations(mal_id)`
Takes the MAL ID and fetches a list of recommended anime from MyAnimeList.

The first thing it does is check if `mal_id is None` — this happens when `search()` fails and returns nothing. Without this check the function would keep running and crash with a confusing error. The `return` after the print is essential — without it Python would continue executing the rest of the function regardless of the print statement.

**Note:** Always use `is` when checking for `None` in Python, not `==`. There is only ever one `None` object in Python, so `is None` is the correct and conventional way to check for it.

It then calls the recommendations endpoint: `{base_url}anime/{mal_id}/recommendations`, which returns a list of similar anime for that specific MAL ID.

The for loop uses `enumerate()` to loop through the results with numbering. `enumerate()` returns two values for each item — the count and the item itself — so two variables are needed to unpack them: `for i, item in enumerate(data, 1)`. The `1` tells Python to start counting from 1 instead of 0.

Each recommendation prints two things:
- The anime title, accessed via `item['entry']['title']`
- The MAL URL, accessed via `item['entry']['url']`

A blank line `\n` is printed after the URL to keep the output clean and readable. The URL is printed on its own line so it's clearly paired with its title.

### The `while True` loop
Instead of running the script multiple times, the entire flow lives inside a `while True` loop. This is more efficient because:
- Function definitions at the top just register the functions in memory — they don't run yet
- All execution happens inside the loop, starting with asking for the anime title
- After showing recommendations, the user is asked if they want to search again
- If they answer anything other than `'y'`, `break` stops the loop and the script ends

Chaining the functions together: `mal_id = search(title)` gets the ID, then `get_recommendations(mal_id)` uses that ID to fetch and display recommendations. Each function feeds directly into the next.

## What I learned
* How to use a free API without an API key
* How `.json()` converts a raw API response into a navigable Python dictionary
* How to read and navigate nested JSON responses to extract specific data
* How `try/except` handles errors gracefully instead of crashing
* Why `return` is essential after error checks inside functions
* The difference between `is None` and `== None` and why `is` is correct
* How `enumerate()` works and why two variables are needed to unpack it
* How `while True` with `break` creates a clean reusable loop
* How function definitions and function calls are separate — functions only run when called

## Future improvements
* Search multiple anime at once and combine their recommendations
* Filter out duplicates when combining results from multiple searches
* Show additional info like genre, episode count, or rating alongside the title
* Add error handling for network failures or API downtime
