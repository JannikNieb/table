from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, TextInput
from bokeh.io import output_file, show
from bokeh.embed import components
from flask import Flask, render_template, request
from bokeh.resources import INLINE

app = Flask(__name__)

id_list=[]
value1_list=[0]*10
value2_list=[0]*10
value3_list=[0]*10
value4_list=[0]*10
value5_list=[0]*10
dicts=[]
n_list=[]

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
            essence=file.read()
            essence=essence.split()
            list(essence)
            dicts.append(essence)

collect_data(n=10)


for i in range(len(dicts)):
    data_file=dicts[i]
    id_list.append(data_file[1])
    for n in range(1, 5):
        if f'"val{n}":' in data_file:
            index = data_file.index(f'"val{n}":')
            value = data_file[index+1]
            if n==1:
                value1_list[i]=value
            elif n==2:
                value2_list[i]=value
            elif n==3:
                value3_list[i]=value
            elif n==4:
                value4_list[i]=value
            elif n==5:
                value5_list[i]=value

print(value1_list)

data = dict(
        id=id_list,
        value_1=value1_list,
        value_2=value2_list,
        value_3=value3_list,
        value_4=value4_list,
        value_5=value5_list,
            )

source = ColumnDataSource(data)

@app.route('/')
def create_table():
    columns = [
            TableColumn(field="id", title="id"),
            TableColumn(field="value_1", title="value_1"),
            TableColumn(field="value_2", title="value_2"),
            TableColumn(field="value_3", title="value_3"),
            TableColumn(field="value_4", title="value_4"),
            TableColumn(field="value_5", title="value_5"),
        ]
    data_table = DataTable(source=source, columns=columns, width=800, height=400)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(data_table)
    return render_template("table2.html", script=script, div=div, js_resources=js_resources, css_resources=css_resources, )

if __name__ == '__main__':
    app.run(port=5000, debug=True)
