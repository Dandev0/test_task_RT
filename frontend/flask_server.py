from flask import render_template
from config import *


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
