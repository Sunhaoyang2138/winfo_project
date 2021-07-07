import streamlit as st     
import csv as csv  
import pandas as pd  
import numpy as np  
from sqlalchemy import create_engine

st.title("Projekt")

st.write("""
eine kurze Beschreibung der Analyse
""")

dataset_name = st.selectbox("Select Dataset", ("Sollfahrtdaten", "Istfahrtdaten"))
st.write(dataset_name)

def get_dataset(dataset_name):
    if dataset_name == "Sollfahrtdaten":
        csv = pd.read_csv ('592M_expected.csv', sep=";")

    else :
        csv = pd.read_csv('592M_actual.csv', sep=";")
    return csv
df = get_dataset(dataset_name)

df.sort_values('Date', ascending = True, inplace = True)

#st.dataframe(df, 500, 480)

st.write('Zusammenführung der Datensätze')
#cd = combine datasets
df1 = pd.read_csv('592M_expected.csv', sep=";")
df2 = pd.read_csv('592M_actual.csv', sep=";")
cd = [df1, df2]
result = pd.concat(cd)
result.sort_values('Date', ascending = True, inplace = True)
result.to_csv('/Users/tlobry/Desktop/winfo_project/unser_csv.csv',sep=';', index = False, quoting=csv.QUOTE_NONNUMERIC)
#st.dataframe(result)
#verspötungen von normal verlaufenden fahrten ermitteln
#sql_result = result[result.TripType == 'expected']
sql_result = result.groupby('Date')

st.dataframe(sql_result)
