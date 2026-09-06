from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "some password that no one knows"

# Form class
class AddItemForm(FlaskForm):
    item_name = StringField('Item name', validators=[DataRequired()])
    item_count= IntegerField('Item count', validators=[DataRequired()])
    days_to_exp = IntegerField('Days to expire', validators=[DataRequired()])
    item_location = StringField('Item location', validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')
def index():
    return render_template("display_list.html")

@app.route('/Add_Item', methods=['GET', 'POST'])
def add_Item():
    item_name = None
    item_count = None
    days_to_exp = None
    item_location = None
    form = AddItemForm()
    return render_template("add_item.html", form=form)

if __name__ in "__main__":
    app.run(debug=True)