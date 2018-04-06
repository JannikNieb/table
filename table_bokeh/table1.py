from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show
from flask import Flask, render_template, request


output_file("table.html")

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

columns = [
        TableColumn(field="id", title="id"),
        TableColumn(field="value_1", title="value_1"),
        TableColumn(field="value_2", title="value_2"),
    ]
data_table = DataTable(source=source, columns=columns, width=400, height=280)

show(data_table)
