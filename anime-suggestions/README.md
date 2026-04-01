# Anime Recommendation Engine

## Why I built this
I built this so I can type in any anime and get a list of similar recommendations with links to their MyAnimeList pages. I later updated it with a Flask web interface so the recommendations display as a grid of thumbnails instead of plain terminal output.

## Libraries used

### Terminal version
* `requests` — fetches data from the Jikan API by sending HTTP GET requests
* `time` — used for `time.sleep()` between API calls to avoid rate limiting. Removed from `get_recommendations()` after finding it caused unnecessary slowdown — Jikan's rate limit of 60 requests per minute is generous enough for personal use

### Flask web app (additional)
* `flask` — Python web framework that handles routing URLs, processing form data, and serving HTML pages to the browser
* `render_template` from flask — returns HTML files to the browser. Templates live in a `templates` folder in the project directory

## API
This project uses the **Jikan API** (`https://api.jikan.moe/v4/`) — a free, open API for MyAnimeList data. No API key or account needed. Jikan has a rate limit of 60 requests per minute which is more than enough for personal use.

## Setup

### Install dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install flask requests
pip freeze > requirements.txt
```

## How it works

### `search(title)`
Takes an anime title and returns its MAL ID — a unique number MyAnimeList assigns to every anime. This ID is needed to fetch recommendations.

Calls the search endpoint with `limit=1`. `.json()` converts the raw response into a Python dictionary. The MAL ID is extracted by navigating the nested dictionary: `response.json()['data'][0]['mal_id']`.

Error handling with `try/except` catches an `IndexError` if the anime is not found.

### `get_recommendations(mal_id)`
Takes the MAL ID and fetches a list of recommended anime. First checks if `mal_id is None` — this happens when `search()` fails. Without this check the function would keep running and crash. The `return` after the print is essential — without it Python continues executing regardless.

Returns all results as a list so Flask can pass them to the HTML template.

Always use `is` when checking for `None` in Python, not `==`. There is only ever one `None` object so `is None` is the correct convention.

### Flask web app — `app.py`

Routes connect URLs to functions using the `@app.route()` decorator:

```python
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def get_anime():
    title = request.args['Anime']
    mal_id = search(title)
    recs = get_recommendations(mal_id)
    return render_template('results.html', recs=recs, title=title)
```

The search uses GET so the anime name appears in the URL (e.g. `?Anime=solo+leveling`) — useful for users to see what they searched. `request.args` reads URL parameters from GET requests. `request.form` is used for POST instead.

`render_template()` returns an HTML file to the browser. Keyword arguments like `recs=recs` pass Python data into the template.

Run with `python app.py`. `debug=True` enables auto-reload on save.

### Jinja2 templating
Flask uses Jinja2 to inject Python data into HTML. Two tag types:
* `{% for item in recs %}` / `{% endfor %}` — logic tags for loops and if statements
* `{{ item['entry']['title'] }}` — output tags that display a value on the page

### HTML and CSS
Results display in a 5-column CSS Grid. Each anime shows a thumbnail, title, and MAL link. Dark mode is applied with `background-color: #121212` on the body. `object-fit: cover` ensures all thumbnails are uniform without stretching. `onerror` on the image tag swaps in a placeholder if an image fails to load. The search form stays on the results page so users can search again without going back.

## What I learned
* How to use a free API without an API key
* How `.json()` converts a raw API response into a navigable Python dictionary
* How to navigate nested JSON to extract specific data
* How `try/except` handles errors gracefully instead of crashing
* Why `return` is essential after error checks inside functions
* The difference between `is None` and `== None`
* How Flask routes work and how decorators connect URLs to functions
* The difference between GET and POST and when to use each
* How `request.args` and `request.form` read data from different request types
* How Jinja2 passes Python data into HTML templates
* How CSS Grid creates a multi-column layout
* How `object-fit: cover` makes images uniform without stretching
* That removing an unnecessary `time.sleep()` can be a bigger performance fix than complex solutions like threading

## Future improvements
* Add error handling for when an anime is not found in the web app
* Deploy to a hosting platform like Railway or Render so others can use it
