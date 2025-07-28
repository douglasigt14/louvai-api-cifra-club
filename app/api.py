"""API Module"""

import os
from flask import Flask, json
from cifraclub import CifraClub, CifraClubLink  # importar as duas classes
from urllib.parse import unquote

app = Flask(__name__)

@app.route('/')
def home():
    """Home route"""
    return app.response_class(
        response=json.dumps({'api': 'Cifra Club API'}),
        status=200,
        mimetype='application/json'
    )

@app.route('/artists/<artist>/songs/<song>')
def get_cifra(artist, song):
    """Get cifra by artist and song"""
    cifraclub = CifraClub()
    return app.response_class(
        response=json.dumps(cifraclub.cifra(artist, song), ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

@app.route('/link/<path:url>')
def get_cifra_by_link(url):
    """Get cifra by full Cifra Club URL"""
    url_decoded = unquote(url)
    link_handler = CifraClubLink()
    return app.response_class(
        response=json.dumps(link_handler.cifra(url_decoded), ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT', '8080'), debug=True)
