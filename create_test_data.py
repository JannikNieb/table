import json
import random
import uuid


KEYS = ['id']
KEYS_OPTIONAL = ['val1', 'val2', 'val3', 'val4', 'val5']


def create_data():
    out = dict(id=str(uuid.uuid1()))
    for j in range(len(KEYS_OPTIONAL)):
        out[random.choice(KEYS_OPTIONAL)] = random.random()
    return out


def save_json_files(n):
    for j in range(0, n):
        filename = f'table_flask/data/score{j}.json'
        print(f"Writing data to file: {filename}")
        with open(filename, 'w') as file:
            json.dump(create_data(), file)


if __name__ == "__main__":
    save_json_files(n=10)