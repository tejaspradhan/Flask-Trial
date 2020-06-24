from flask import Flask
import gensim
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"