from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, TextInput
from bokeh.io import output_file, show
from bokeh.embed import components
from flask import Flask, render_template, request
from bokeh.resources import INLINE
from os import scandir

app = Flask(__name__)


def get_file_amount(foldername):
    """
    gets the number of files in a given folder

    Args:
        foldername: (string)

    Returns:
        number_of_ files (integer)
    """
    return len([1 for x in list(scandir(foldername)) if x.is_file()])


def get_keys_amount(foldername, number_of_files):
    """
    gets the length of the longest json- files

    Args:
        foldername: (string)
        number_of_files: (integer)

    Returns:
        number_of_keys: (integer) length of the json-file
    """
    length=[]
    for i in range(number_of_files):
        length.append(len(set(open(foldername + f'/score{i}.json').read().split())))
    return max(length)


def get_data(foldername, number_of_files):
    """Get data as dict from folder

    load all file information from all json-files in folder "foldername"

    Args:
        foldername: (string)

    Returns:
        list[dict]: (list of dictionaries) containing the information from loaded json-files
    """
    dicts = []

    for j in range(0, number_of_files):
        filename = foldername + f'/score{j}.json'

        with open(filename, 'r') as file:  # extracting the data from the json- file
            essence = file.read()
            essence = essence.split()
            list(essence)  # storing it under the variablename "essence"
            dicts.append(essence)  # storing these values in the dicts- list
    return dicts


def get_dict_keys(data, number_of_files, number_of_keys):
    """

    Args:
        data: (list of lists of dictionaries)

    Returns:
        set[str]: (list of lists) set of keys in dicts contained in data
    """
    # return list(set([key for d in data for key in d]))

    key_list=[]
    for i in range(number_of_keys):
        key_list.append([] * (number_of_files+1))

    for i in range(len(data)):
        data_file = data[i]  # iterating over the dicts- list (extracting the essence again)
        key_list[i].append(data_file[1])
        for n in range(1, number_of_keys+1):  # extracting the defined values and storing them in lists
            if f'"val{n}":' in data_file:
                index = data_file.index(f'"val{n}":')
                key_list[i].append(data_file[index])
                key_list[i].append(data_file[index+1])
    return key_list


def clean_data(data, key_list, number_of_files, number_of_keys, default=0):
    """

    Args:
        data:
        key_list: (list of lists)
        default: (any character)

    Example:
        >>> clean_data([{'key1': 1}, {'key2': 2}], ['key1', 'key2'])
        ... = {'key1': 1, 'key2': default}, {'key1': default, 'key2': 2}

    Returns:

    """
    lists = []
    for i in range(len(key_list)):
        lists.append([default] * number_of_files)
    keys = ['id']

    for i in range(number_of_files):
        for n in range(1, (number_of_keys + 1)):
            if f'"val{n}":' in key_list[i]:
                lists[0][i] = (key_list[i][0])
                index = key_list[i].index(f'"val{n}":')
                value = (key_list[i][index+1])
                value = value[:len(value) - 1]
                (lists[n])[i] = value

    for u in range(1, number_of_keys):
        keys.append(f"value{u}")

    data = {key: lists[j] for j, key in enumerate(keys)}

    return data

def render_table(cleaned_data):
    """

    Args:
        cleaned_data: (list of lists of dictionaries)

    Returns:
        DataTable
    """
    source = ColumnDataSource(cleaned_data)

    columns = [
            TableColumn(field="id", title="id"),
            TableColumn(field="value1", title="value_1"),
            TableColumn(field="value2", title="value_2"),
            TableColumn(field="value3", title="value_3"),
            TableColumn(field="value4", title="value_4"),
            TableColumn(field="value5", title="value_5"),
        ]
    data_table = DataTable(source=source, columns=columns, width=800, height=400)

    return data_table


@app.route('/')
def create_table():

    foldername = 'data'

    number_of_files = get_file_amount(foldername)
    number_of_keys = get_keys_amount(foldername, number_of_files)
    data = get_data(foldername, number_of_files)
    keys = get_dict_keys(data, number_of_files, number_of_keys)
    data = clean_data(data, keys, number_of_files, number_of_keys)
    bokeh_table = render_table(data)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(bokeh_table)
    return render_template("table2.html", script=script, div=div, js_resources=js_resources, css_resources=css_resources,)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
