from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, TextInput
from bokeh.io import output_file, show
from bokeh.embed import components
from flask import Flask, render_template, request
from bokeh.resources import INLINE
from os.path import isdir
from os import scandir
import json

app = Flask(__name__)


def list_files(foldername):
    """
    gets names of all the files in the folder
    Args:
        foldername: (string)

    Returns:
        files: (list)
    """
    return [x for x in scandir(foldername) if x.is_file()]


def get_data(files):
    """Get data as dict from folder

    load all file information from all json-files in folder "foldername"

    Args:
        files: (list)

    Returns:
        list[dict]: (list of dictionaries) containing the information from loaded json-files
    """
    dicts = []

    for filename in files:
        with open(filename, 'r') as file:
            dicts.append(json.load(file))
    return dicts


def get_dict_keys(data, files):
    """
    filters all the keys out of data
    Args:
        data: (list of lists of dictionaries)
        files: (list)

    Returns:
        keys: (list) set of keys contained in data
    """
    key_list = []

    for i in range(len(data)):
        data_file = data[i]  # iterating over the dicts- list (extracting the essence again)
        key_list.append(list(data_file))

    keys = []

    for n in range(len(files)):
        for i in range(len(key_list[n])):
            keys.append(key_list[n][i])
    keys = list(set(keys))

    return sorted(keys)


def clean_data(keys, data, default="-"):
    """
    cleans the data in order to archive the correct format
    Args:
        data:
        keys: (list)
        default: (any character)

    Example:
        >>> clean_data([{'keybla': 1}, {'keybums': 2}], ['keybla', 'keybums'])
        ... = {'keybla': 1, 'keybums': default}, {'keybla': default, 'keybums': 2}

    Returns:
        cleaned_data: (dictionary of lists)
    """
    lists = [[] for x in range(len(keys))]

    for i in range(len(keys)):
        for n in range(len(data)):
            if keys[i] in list(data[n]):
                lists[i].append(data[n][keys[i]])
            else:
                lists[i].append(default)

    data = {}

    for i in range(len(lists)):
        data[keys[i]] = lists[i]

    return data


def render_table(cleaned_data, keys):
    """
    creates the visual bokeh- table
    Args:
        cleaned_data: (dictionary of lists)

    Returns:
        DataTable
    """
    source = ColumnDataSource(cleaned_data)

    columns = []

    for i in keys:
        columns.append(TableColumn(field=str(i), title=str(i)))

    data_table = DataTable(source=source, columns=columns, width=800, height=400)

    return data_table


@app.route('/')
def create_table():

    files = list_files('data')
    data = get_data(files)
    keys = get_dict_keys(data, files)
    cleaned_data = clean_data(keys, data)
    bokeh_table = render_table(cleaned_data, keys)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(bokeh_table)
    return render_template("table2.html", script=script, div=div, js_resources=js_resources, css_resources=css_resources,)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
