import logging

from flask import Flask, jsonify, request

from scraper import get_quotes

# Configurar logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/quotes', methods=['GET'])
def quotes():
    author = request.args.get('author')
    page = request.args.get('page', '1')
    try:
        quotes = get_quotes(author, page)
        return jsonify(quotes)
    except Exception as e:
        logging.error(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
