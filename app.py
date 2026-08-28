from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("display_list.html")

@app.route('/hello')
def add_Item():
    return render_template("add_item.html")

if __name__ in "__main__":
    app.run(debug=True)