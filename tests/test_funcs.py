from table import list_files, get_data, get_dict_keys, clean_data


# checking if a correct inout leads to an correct output
def test_list_files_true():
    assert len(list_files('/home/jniebling/Python/Praktikum/ml_model_fe/tests/demo_data')) == 5


def test_get_data_true():
    assert get_data(list_files('/home/jniebling/Python/Praktikum/ml_model_fe/tests/demo_data')) == [{'id': '5', 'val3': 7, 'val2': 4, 'val1': 9}, {'id': '1', 'val4': 7, 'val1': 2, 'val2': 7}, {'id': '2', 'val3': 3, 'val4': 5}, {'id': '3', 'val2': 10, 'val3': 8, 'val5': 3, 'val4': 0}, {'id': '4', 'val1': 1, 'val3': 2, 'val4': 5, 'val5': 4}]


def test_get_dict_keys_true():
    assert get_dict_keys(get_data(list_files('/home/jniebling/Python/Praktikum/ml_model_fe/tests/demo_data')), list_files('/home/jniebling/Python/Praktikum/ml_model_fe/tests/demo_data')) == ['id', 'val1', 'val2', 'val3', 'val4', 'val5']


def test_clean_data_true():
    assert clean_data(['id', 'val1', 'val2', 'val3', 'val4', 'val5'], get_data(list_files('/home/jniebling/Python/Praktikum/ml_model_fe/tests/demo_data'))) == {'id': ['5', '1', '2', '3', '4'], 'val1': [9, 2, '-', '-', 1], 'val2': [4, 7, '-', 10, '-'], 'val3': [7, '-', 3, 8, 2], 'val4': ['-', 7, 5, 0, 5], 'val5': ['-', '-', '-', 3, 4]}


# checking if an incorrect input in foldername leads to an incorrect output

#create_table()