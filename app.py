from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import List
from sqlalchemy import String, Integer, DateTime, func, select

app = Flask(__name__)
app.config["SECRET_KEY"] = "some password that no one knows"

# Database setup
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fridge.db"
db.init_app(app)



# Database model definition

class Item(db.Model):
    __tablename__ = "fridge_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str] = mapped_column(String(30))
    purchase_date: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    item_count: Mapped[int]
    days_to_exp: Mapped[int]
    item_location: Mapped[str] = mapped_column(String(15))

# Create model
with app.app_context():
    db.create_all()


# Form class
class AddItemForm(FlaskForm):
    item_name = StringField('Item name', validators=[DataRequired()])
    item_count= IntegerField('Item count', validators=[DataRequired()])
    days_to_exp = IntegerField('Days to expire', validators=[DataRequired()])
    item_location = StringField('Item location', validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')
def index():
    items = db.session.execute(db.select(Item)).scalars().all()
    return render_template("display_list.html", items=items)

@app.route('/Add_Item', methods=['GET', 'POST'])
def add_Item():
    item_name = None
    item_count = None
    days_to_exp = None
    item_location = None
    form = AddItemForm()

    if form.validate_on_submit() and request.method == 'POST':

        item = Item(
            item_name = form.item_name.data,
            item_count = form.item_count.data,
            days_to_exp = form.days_to_exp.data,
            item_location = form.item_location.data,
        )
        db.session.add(item)
        db.session.commit()

        # Clear form
        form.item_name.data = ''
        form.item_count.data = ''
        form.days_to_exp.data = ''
        form.item_location.data = ''

        flash("Item Added Succesfully")
    return render_template("add_item.html", form=form)


@app.route('/Edit_Item', methods=['GET', 'POST'])
def edit_Item():
    item_name = None
    item_count = None
    days_to_exp = None
    item_location = None
    form = AddItemForm()

    if form.validate_on_submit():
        flash("Item Edited Succesfully")
    return render_template("edit_item.html", form=form)

if __name__ in "__main__":
    app.run(debug=True)