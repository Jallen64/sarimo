from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
import pandas as pd


app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        df = pd.read_csv(request.files.get('file'))
        return render_template('graph.html', shape=df.to_json(orient='values'))
    return render_template('upload.html')

@app.route("/graph")
def graph():
    return render_template("graph.html")

@app.route("/index")
def index():
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)