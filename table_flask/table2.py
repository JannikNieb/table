from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, TextInput
from bokeh.io import output_file, show
from bokeh.embed import components
from flask import Flask, render_template, request
from bokeh.resources import INLINE

app = Flask(__name__)

id_list=[]
value1_list=[]
value2_list=[]

dicts = [
            {
                'id': 1,
                'value_1': 0.7,
                'value_2': 3
            },
            {
                'id': 2,
                'value_1': 0.5,
                'value_2': 2.3
            },
            {
                'id': 3,
                'value_1': 0.6,
                'value_2': 3
            },
            {
                'id': 4,
                'value_1': 0.89,
                'value_2': 32
            }
           ]

for i in dicts:
    id_list.append(i['id'])
    value1_list.append(i['value_1'])
    value2_list.append(i['value_2'])

data = dict(id=id_list,
            value_1=value1_list,
            value_2=value2_list,)

source = ColumnDataSource(data)

@app.route('/')
def create_table():
    columns = [
            TableColumn(field="id", title="id"),
            TableColumn(field="value_1", title="value_1"),
            TableColumn(field="value_2", title="value_2"),
        ]
    data_table = DataTable(source=source, columns=columns, width=800, height=400)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(data_table)
    return render_template("table2.html", script=script, div=div, js_resources=js_resources, css_resources=css_resources, )

if __name__ == '__main__':
    app.run(port=5000, debug=True)
