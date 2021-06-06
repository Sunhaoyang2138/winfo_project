import streamlit as st       
import pandas as pd  
import numpy as np  

st.title("kkkkkk")

st.write("""
eine kurze Beschreibung der Analyse
""")

dataset_name = st.selectbox("Select Dataset", ("Sollfahrtdaten", "Istfahrtdaten"))
st.write(dataset_name)

def get_dataset(dataset_name):
    if dataset_name == "Sollfahrtdaten":
        csv = pd.read_csv('592M_expected.csv')
    else :
        csv = pd.read_csv('592M_actual.csv')
    return csv
df = get_dataset(dataset_name)
# df['Date'] = pd.to_datetime(df.date, infer_datetime_format = True)
# df.sort_values(by='Date', ascending = True, inplace = True)
st.write(df.head())
df.sort_values(by = "date")