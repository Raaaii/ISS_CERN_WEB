import urllib.request
import re
from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Define df and extract_mass_excess at the global level
df = None

@app.route('/retrive_data', methods=['GET'])
def read_data():
    global df
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

def extract_mass_excess(df, A, N):
    mass_excess = df.loc[(df['A'] == A) & (df['N'] == N), 'Mass Excess'].values[0]
    return mass_excess

@app.route('/calculate_mass_excess', methods=['POST'])


def calculate_mass_excess():
    data = request.get_json()
    mass_excess_values = {}

    for particle in data:
        A = int(particle['a'])
        N = int(particle['z'])
        mass_excess = extract_mass_excess(df, A, N)
        mass_excess_values[particle['particle']] = mass_excess

    return jsonify(mass_excess_values)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
    #check if the server is running
    print("Server is running!")

