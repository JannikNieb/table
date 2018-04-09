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
dicts=[]

''''dicts = [
            {
                'id': 1,
                'value_1': 0.7,
                'value_2': 3
            },
            {
                'id': 2,
                'value_1': 0.5,
                'value_2': 2.3
            }
           ]'''

def collect_data(n):
    for j in range(0,n):
        filename = f'data/score{j}.json'
        with open(filename, 'r') as file:
            print(file)
            essence=file.read()
            essence=essence.split()
            list(essence)
            dicts.append(essence)

collect_data(n=10)
print(dicts)


for i in range(len(dicts)):
    data_file=dicts[i]
    id_list.append(data_file[1])

data = dict(id=id_list)

source = ColumnDataSource(data)

@app.route('/')
def create_table():
    columns = [
            TableColumn(field="id", title="id"),
            #TableColumn(field="value_1", title="value_1"),
            #TableColumn(field="value_2", title="value_2"),
        ]
    data_table = DataTable(source=source, columns=columns, width=800, height=400)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(data_table)
    return render_template("table2.html", script=script, div=div, js_resources=js_resources, css_resources=css_resources, )

if __name__ == '__main__':
    app.run(port=5000, debug=True)
