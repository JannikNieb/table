from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask import Flask, render_template, flash, request
import uuid


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '1234'


class ReusableForm(Form):
    value = StringField('Value:', validators=[validators.required()])
    key = StringField('Key:', validators=[validators.required()])


def add_data(key, value):
    print([{"id": str(uuid.uuid1()), key: float(value)}, key])
    return[{"id": str(uuid.uuid1()), key: float(value)}, key]


@app.route('/', methods=['GET', 'POST'])
def read_data():
    form = ReusableForm(request.form)
    if request.method == 'POST':
        value = request.form['value']
        key = request.form['key']
        if form.validate():
            flash('Key: ' + key + " and Value: " + value + " have been added to your table!")
            add_data(key, value)

    return render_template('table_input.html', form=form)




if __name__ == '__main__':
    app.run(port=4000, debug=True)