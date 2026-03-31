from flask import Flask, request, render_template
from anime_suggestions import search, get_recommendations

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def get_anime():
    title = request.form['Anime']
    mal_id = search(title)
    recs = get_recommendations(mal_id)

    return render_template('results.html', recs=recs)


if __name__ == '__main__':
    app.run(debug=True)
