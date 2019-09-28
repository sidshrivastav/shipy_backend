from flask import Flask, render_template, request
from requests import get
from json import loads
app = Flask(__name__)


@app.route('/<order_id>')
def index(order_id):
    r = get('http://0.0.0.0:71/api/order?order_id='+order_id)
    data = (loads(r.text))[0]
    return render_template('index.html', data=data)


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=61)