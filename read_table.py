import urllib.request
import re
from flask import Flask, jsonify
import pandas as pd


app = Flask(__name__)
@app.route('/retrive_data', methods=['GET'])

def read_data():
    df = read_table()
    result = df.to_json(orient="list")
    return jsonify(result)

def read_table():
    url = "https://www.anl.gov/sites/www/files/2021-05/mass_1.mas20.txt"
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    lines = data.splitlines()[36:]
    columns_with_numbers = []
    N_values = []
    A_values = []
    mass_excess_values = []
    for line in lines:
        if not line.strip():
            continue
        
        if line.startswith('0'):
            line = line[1:]
        
        columns = re.findall(r"[-+]?[\d.]+(?:[eE][-+]?\d+)?", line)
        columns_with_numbers.append([float(column) for column in columns])
        A_values.append(int(columns[3]))
        N_values.append(int(columns[2]))
        mass_excess_values.append(float(columns[4]))

    data = {
        'A': A_values,
        'N': N_values,
        'Mass Excess': mass_excess_values,
    }
    df = pd.DataFrame(data)
    return df
