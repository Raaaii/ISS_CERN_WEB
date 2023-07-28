from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
import urllib.request
import re
import math

app = Flask(__name__)
CORS(app)





#READING THE TABLE FROM THE WEBSITE
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





df = read_table()

#EXTRACTING THE MASS EXCESS VALUES FROM THE TABLE

def extract_mass_excess(df, A, N):
    
    filtered_df = df.loc[(df['A'] == A) & (df['N'] == N), 'Mass Excess']
    
    if filtered_df.empty:
        return None  # or some other placeholder/error message
    
    return filtered_df.values[0]



#CALCUATE THE MASS EXCESS VALUES

def calculate_mass_excess():
    data = request.get_json()
    mass_excess_values = {}

    print(data)

    for particle in data:
        A = int(particle['a'])
        N = int(particle['z'])
        mass_excess = extract_mass_excess(df, A, N)
        
        # Handle potential None value
        if mass_excess is None:
            mass_excess_values[particle['particle']] = "Data not found"
        else:
            mass_excess_values[particle['particle']] = mass_excess

    return jsonify(mass_excess_values)




def calculate_v3(m1, m2, m3, E_x, T_i):
    m1 = float(m1)
    m2 = float(m2)
    m3 = float(m3)
    E_x = int(E_x)
    T_i = int(T_i)
    print("DATA: ",m1,m2,m3,E_x, T_i)
    T_1 = (m2 / (m1 + m2)) * T_i
    Q = (m1 + m2) - (m3 + m1)
    numerator = 2 * m1 * (T_1 + Q - E_x)
    denominator = m3 * (m3 + m1)
    #print("+++++++++++++++++++++++++",numerator, denominator)
    v3 = math.sqrt(abs(numerator) / abs(denominator))
    return v3
