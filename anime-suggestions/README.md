# HTML, CSS & Flask Notes

---

## HTML

### What is HTML?
HTML (HyperText Markup Language) is the structure of a webpage. It defines what content exists on the page — text, images, forms, links, etc. CSS then styles that content and Flask serves it to the browser.

### Tags and Elements
Everything in HTML is written with **tags** — words inside angle brackets like `<div>`, `<p>`, `<form>`. Most tags have an opening and closing version. The forward slash in `</p>` signals the closing tag. The full thing — opening tag, content, and closing tag — is called an **element**.

### Basic Document Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
</head>
<body>
    <!-- visible content goes here -->
</body>
</html>
```
- `<!DOCTYPE html>` — tells the browser this is modern HTML5. Without it browsers go into "quirks mode" and render things inconsistently. It matters
- `<head>` — metadata about the page. Not displayed to the user. Contains the title, character encoding, and CSS styles
- `<body>` — everything visible on the page goes here
- `<!-- comment -->` — how you write comments in HTML

### Common Tags
- `<div>` — short for division. A container box with no visual meaning on its own. Used to group elements for layout and styling
- `<p>` — paragraph. Displays a block of text
- `<form>` — groups input elements and defines where to send data when submitted. Does not create a new page
- `<input>` — a field where the user types. `type="text"` is a text box
- `<button>` — a clickable button
- `<img src="">` — displays an image. `src` stands for source — the URL or file path of the image
- `<a href="">` — anchor tag, creates a clickable link. `href` is the destination URL. The text between `<a>` and `</a>` is what the user clicks

### Parents and Children
Elements nest inside each other. The outer element is the **parent**, inner elements are **children**:
```html
<div class="card">        <!-- parent -->
    <img src="...">       <!-- child -->
    <p>Title</p>          <!-- child -->
    <a href="...">Link</a> <!-- child -->
</div>
```
This matters for CSS — `.card a` targets only links inside `.card`, while `a` targets every link on the page.

### Forms — GET vs POST
- **GET** — puts data in the URL (e.g. `?anime=naruto`). Visible and bookmarkable, not for sensitive data
- **POST** — sends data in the request body, hidden from the URL. Better for forms. Note: POST alone doesn't encrypt — that requires HTTPS

```html
<form action="/search" method="post">
    <input type="text" name="Anime" placeholder="Hunter x Hunter">
    <button type="submit">Search</button>
</form>
```
- `action` — URL the form sends data to
- `name` — how Flask identifies this input with `request.form['Anime']`
- `placeholder` — hint text shown before the user types

### onerror
A JavaScript attribute that runs if something fails:
```html
<img src="image.jpg" onerror="this.src='placeholder.jpg'">
```
If the image fails to load it swaps to the placeholder. VS Code may grey it out but it still works.

---

## CSS

### What is CSS?
CSS (Cascading Style Sheets) is entirely about styling HTML — colors, sizes, spacing, fonts, and layout. It lives inside a `<style>` tag in the `<head>` or in a separate `.css` file.

### Syntax
```css
selector {
    property: value;
    property: value;
}
```
Every rule ends with a semicolon. Think of it like a Python dictionary but with colons and semicolons.

### Selectors
- `body` — targets the `<body>` tag directly (no dot)
- `form` — targets all `<form>` tags
- `.card` — dot means targeting a **class**. Targets any element with `class="card"`
- `.card img` — targets `<img>` elements that are children of `.card`
- `.card a` — targets `<a>` elements inside `.card` only

### Padding vs Margin
- **Padding** — space *inside* an element between content and border. Breathing room inside a button
- **Margin** — space *outside* an element between it and other elements
- `4px 0` — shorthand for 4px top/bottom, 0 left/right

### Common Properties
- `background-color` — background color
- `color` — text color
- `font-family: Arial, sans-serif` — Arial is preferred, `sans-serif` is the fallback if Arial isn't on the user's device
- `font-size` — text size
- `width` / `height` — dimensions
- `border: 1px solid #444` — `1px` thickness, `solid` style, `#444` color
- `border: none` — removes border
- `cursor: pointer` — hand cursor on hover, signals clickable
- `px` — pixels

### Grid Layout
```css
.grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
}
```
- `display: grid` — activates grid layout
- `repeat(5, 1fr)` — 5 columns, each taking 1 equal fraction (`fr`) of available width
- `gap` — space between grid items. Rows add automatically as more items fill the grid

### Flexbox
```css
.card {
    display: flex;
    flex-direction: column;
    align-items: center;
}
```
- `display: flex` — activates flexbox
- `flex-direction: column` — stacks children vertically
- `align-items: center` — centers children horizontally

### object-fit
```css
img {
    width: 200px;
    height: 280px;
    object-fit: cover;
}
```
`cover` scales the image to fill the box, cropping overflow while keeping proportions. Prevents stretching.

---

## Flask

### What is Flask?
A Python web framework for building web apps. Handles routing URLs, processing form data, and serving HTML to the browser.

### Creating the App
```python
from flask import Flask
app = Flask(__name__)
```
Flask is a class. `app` is your instance — your web application object. `__name__` tells Flask the current module name so it knows where to find templates and static files.

### Routes and Decorators
```python
@app.route('/')
def index():
    return render_template('index.html')
```
`@app.route('/')` is a **decorator** — tells Flask "when someone visits this URL, run the function below." You can make any path like `/search`, `/home`. In the browser: `yourdomain.com/search`.

Tip: adding a trailing slash (e.g. `/search/`) prevents 404 errors on some setups.

### Handling POST Requests
```python
@app.route('/search', methods=['POST'])
def get_anime():
    title = request.form['Anime']
```
- `methods=['POST']` — tells Flask this route accepts POST requests
- `request.form['Anime']` — gets the value from the input named `Anime` in the form. The name must match exactly

### render_template
```python
return render_template('results.html', recs=recs)
```
Returns an HTML file to the browser. Templates go in a `templates` folder in your project. Keyword arguments like `recs=recs` pass Python data into the template.

### Running the App
```python
if __name__ == '__main__':
    app.run(debug=True)
```
- `if __name__ == '__main__'` — only runs the server when this file is run directly
- `debug=True` — auto-reloads on save. Never use in production

With this at the bottom just run `python app.py` instead of the long `flask run` command.

### Virtual Environments
Isolates project dependencies so they don't conflict with other projects.
```bash
python -m venv venv          # create
venv\Scripts\activate        # activate (Windows)
pip install flask requests   # install inside venv
pip freeze > requirements.txt # save dependencies
```
`requirements.txt` lists every library your project needs. Anyone can run `pip install -r requirements.txt` to install exactly what's required — important for deployment.

Add to `.gitignore`:
```
venv
__pycache__
```
`__pycache__` is auto-created by Python to store compiled code for faster execution. Safe to ignore.

---

## Jinja2 Templating

Flask's built in templating engine. Lets you use Python-like logic inside HTML files.

### Two Tag Types
- `{% %}` — **logic tags** for loops, if statements. Nothing displayed
- `{{ }}` — **output tags** for displaying a value on the page

### Example
```html
{% for item in recs %}
<div class="card">
    <img src="{{ item['entry']['images']['jpg']['image_url'] }}"
         onerror="this.src='placeholder.jpg'">
    <p>{{ item['entry']['title'] }}</p>
    <a href="{{ item['entry']['url'] }}">MAL Link</a>
</div>
{% endfor %}
```
- `{% for item in recs %}` — loops through `recs` passed from Flask
- `{{ item['entry']['title'] }}` — outputs the value to the page
- `{% endfor %}` — closes the loop. Jinja2 requires explicit closing tags

The nested dictionary navigation inside `{{ }}` is identical to regular Python.

---

## request.args vs request.form vs request.values

- `request.form['key']` — reads data sent via **POST** (from the request body)
- `request.args['key']` — reads data sent via **GET** (from the URL parameters e.g. `?Anime=naruto`)
- `request.values['key']` — checks both POST and GET automatically. Cleaner shortcut when you don't care which method was used

If you need to handle both methods separately:
```python
if request.method == 'POST':
    title = request.form['Anime']
else:
    title = request.args['Anime']
```

---

## HTML Headings

`<h1>` through `<h6>` are heading tags. **H** stands for heading:
- `<h1>` — biggest, most important heading. Usually the page title. Only one per page
- `<h2>` — subheading, slightly smaller
- `<h3>` through `<h6>` — progressively smaller headings

Think of it like an outline — `<h1>` is the main topic, `<h2>` are sections, `<h3>` are subsections. Search engines also use headings to understand page structure.

Style headings with CSS like any other element:
```css
h2 {
    text-align: right;
    margin: 0;
    padding: 10px;
    color: #C4C4C4;
}
```

---

## HTML Order = Display Order

**This is critical:** HTML is read top to bottom and elements render in the order they appear. Put something first in the HTML and it shows up first on the page. Put it last and it shows up last.

This is similar to Python being read top to bottom, but with one key difference:
- **Python** — executes line by line at runtime
- **HTML** — renders elements in document order. Position in the file = position on the page
- **CSS** — does NOT work top to bottom the same way. All CSS applies at once. However if two rules target the same element, the one that appears **later** in the file wins. This is the "Cascading" part of CSS (Cascading Style Sheets)

Practical example — if your `<h2>Results for: {{ title }}</h2>` appears after the grid div in your HTML, it will render below the grid on the page. Move it above the grid div in the HTML and it will appear above it.