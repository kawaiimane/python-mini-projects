from flask import Flask, request, render_template
from anime_suggestions import search, get_recommendations

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def get_anime():
    title = request.args['Anime']
    mal_id = search(title)
    recs = get_recommendations(mal_id)

    return render_template('results.html', recs=recs, title=title)


if __name__ == '__main__':
    app.run()
