from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server

import pickle
import numpy as np
model = pickle.load(open('Loan.pkl', 'rb'))

app = Flask(__name__)

def predict():
    Dependents = select('Enter the number of dependents',['0','1','2','3+'])
    if (Dependents == '0'):
        Dependents = 345
    elif (Dependents == '1'):
        Dependents = 102
    elif (Dependents == '2'):
        Dependents = 101
    else:
        Dependents = 51

    ApplicantIncome = input('Income of Applicant:',type = FLOAT)

    CoapplicantIncome = input('Income of Coapplicant:',type = FLOAT)

    LoanAmount = input('Enter the Loan Amount:',type = FLOAT)

    LoanAmountTerm = input('Enter the Loan Term(In Days):',input = NUMBER)

    Credit_History = select('Whether the applicant had conducive credit history',['Yes','No'])
    if (Credit_History == 'Yes'):
        Credit_History = 1.0
    else:
        Credit_History = 0

    Married = select('Whether the applicant is married:',['Yes','No'])
    if (Married == 'Yes'):
        Married = 1
    else:
        Married = 0

    Self_Employed = select('Whether the applicant is Self Employed:',['Yes','No'])
    if (Self_Employed == 'Yes'):
        Self_Employed = 1.0
    else:
        Self_Employed = 0

    Gender = select('Enter the Gender',['Male','Female'])
    if (Gender == 'Male'):
        Gender = 1
    else:
        Gender =0

    PropertyArea = select('Where is the Property Located',['Urban','Semiurban','Rural'])
    if (PropertyArea == 'Urban'):
        Urban = 1
        Semiurban = 0
        Rural = 0
    if (PropertyArea == 'Semiurban'):
        Urban = 0
        Semiurban = 1
        Rural = 0
    if (PropertyArea == 'Rural'):
        Urban = 0
        Semiurban = 0
        Rural = 1

    prediction = model.predict([[Dependents,ApplicantIncome,CoapplicantIncome,LoanAmount,LoanAmountTerm,Credit_History,
                    Married,Self_Employed,Gender,Semiurban,Urban]])

    if (prediction == 1):
        put_text('Yes, the Loan can be granted to the applicant')
    else:
        put_text("No, the loan shouldn't be granted to the applicant")

app.add_url_rule('/tool', 'webio_view', webio_view(predict),
            methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(predict, port=args.port)

#app.run(host='localhost', port=80)

#visit http://localhost/tool to open the PyWebIO application.



