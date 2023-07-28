import urllib.request
import re
from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
from calculate_mass_excess import calculate_mass_excess
from calculate_mass_excess import calculate_v3

app = Flask(__name__)
CORS(app)


#APP ROUTE FOR MASS EXCESS CALCULATION
@app.route('/calculate_mass_excess', methods=['POST'])
def doCalculations():
    return calculate_mass_excess()



#calculating the velocity of the third particle
@app.route('/calculate_v3', methods=['POST'])
def doCalculationsforV3():
    data = request.get_json()

    result = calculate_v3(
        m1=data['mass1'], 
        m2=data['mass2'], 
        m3=data['mass3'], 
        E_x=data['E_x'], 
        T_i=data['T_i']
        )
    return jsonify(result)








if __name__ == '__main__':
    app.run(host='localhost', port=5500, debug=True)
    #check if the server is running
    print("Server is running!")

