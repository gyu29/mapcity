from flask import Flask, render_template
from threading import Thread
import cryptography

app = Flask(__name__)


@app.route('/')
def index():
  return "Alive"


def run():
  app.run(host='0.0.0.0', port=8080, ssl_context="adhoc")


def keep_alive():
  t = Thread(target=run)
  t.start()
