from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("base.html")

@app.route('/hello')
def hello():
    return 'Hello, World'

if __name__ in "__main__":
    app.run(debug=True)