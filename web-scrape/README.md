# Web Scraper
## What does this program do?
This program scrapes book data from [books.toscrape.com](https://books.toscrape.com) across all 50 pages and saves the results to a CSV file. It collects the title, price, star rating, and availability of every book on the site.

## Libraries used
I installed `requests` and `beautifulsoup4` to access these imports:
* `requests` — fetches the raw HTML of a webpage by sending an HTTP GET request to a URL. A successful response returns status code `200`
* `BeautifulSoup` from `bs4` — parses the raw HTML and makes it navigable so you can search and extract specific elements. It requires a parser, in this case Python's built-in `html.parser`. For sites that rely heavily on JavaScript to load content, BeautifulSoup won't work since it can only read static HTML — tools like Selenium or Playwright are needed instead
* `csv` — built into Python, no install needed. Used to create and write to CSV (Comma-Separated Values) files

## How it works

### Setup
Four empty lists are created at the top to act as collection buckets — `titles`, `prices`, `ratings`, and `availability`. These are filled up as the scraper loops through all 50 pages. They are defined before the functions so the loop at the bottom can access and extend them.

### `scrape_web(url)`
A custom function that takes a URL and returns all the book data from that page. It sends a GET request, parses the HTML with BeautifulSoup, then uses `find_all()` to locate specific HTML elements. Tags like `<h3>` are unique enough to search by tag alone, but common tags like `<p>` require a class name to narrow down the results — for example `class_='price_color'` — since `<p>` is used everywhere on a page.

Star ratings are stored in the class attribute itself as a second class name, for example `<p class="star-rating Three">`. Accessing `element["class"]` returns a list like `['star-rating', 'Three']`, so `[1]` is used to grab just the rating word.

The function returns all four lists together as a tuple — a bundle of multiple values packed into one return statement.

### `save_csv(books, filename)`
A custom function that takes the collected data and a filename, then writes everything to a CSV file. The `books` tuple is unpacked at the start into four separate lists so the function can work with them individually.

`with open(filename, mode='w', newline='', encoding='utf-8') as file` opens a file for writing. Here is what each argument does:
* `mode='w'` — write mode, creates the file if it doesn't exist
* `newline=''` — specific to CSV files, prevents blank lines from appearing between rows on Windows
* `encoding='utf-8'` — the most common text encoding, ensures special characters are handled correctly
* `as file` — gives the open file a name so it can be referenced inside the `with` block, for example in `csv.writer(file)`

`csv.writer(file)` creates the writer object that handles formatting the data as CSV. `writerow()` writes one row at a time — first the header row, then each book inside the loop. It takes a list `[]` where each item becomes a separate column.

`zip()` is used to loop through all four lists simultaneously, pairing each title with its corresponding price, rating, and availability by index.

### The page loop
The site has 50 pages, each following the URL pattern `https://books.toscrape.com/catalogue/page-{n}.html`. A `for` loop using `range(1, 51)` generates page numbers 1 through 50 — `range(1, 51)` is used instead of `range(50)` because Python's range stops one short of the end value.

For each page, `scrape_web(url)` is called and the result is unpacked into four `page_` variables. Each is then added to the main collection lists using `.extend()`, which merges one list into another. This is different from `.append()` which would add the entire list as a single item instead of combining them.

### Function definitions vs function calls
Both functions are defined before being called. This follows Python convention — `def` only registers the function in memory, it does not run it. The function only runs when it is called later in the script. This means all function definitions can sit at the top and all execution can happen at the bottom, which keeps the code clean and readable.

## What I learned
* How to use `requests` to fetch a webpage and check for a successful response
* How BeautifulSoup parses HTML and how to extract elements by tag and class
* Why common tags like `<p>` require a class to narrow down results
* How class attributes can store data, not just styling, as seen with star ratings
* How `with open()` works and what each argument does when creating a file
* How `csv.writer` and `writerow()` format and write data to a CSV file
* How `zip()` loops through multiple lists simultaneously
* The difference between `.append()` and `.extend()` when combining lists
* How to build dynamic URLs with f-strings inside a loop
* How Python function definitions are separate from function calls

## Future improvements
* Add `time.sleep()` between requests to avoid being rate limited or blocked by the site
* Add `try/except` error handling so the script doesn't crash if a page fails to load
* Allow user input for the URL and output filename
* Support custom save directories for the CSV file
* Refactor to store each book as a dictionary instead of four separate lists, which is cleaner and easier to manage
