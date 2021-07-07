import streamlit as st       
import pandas as pd  
import numpy as np  

csv = pd.read_csv('unser_csv_small.csv', sep=";")
#verspötungen von normal verlaufenden fahrten ermitteln
#sql_result = csv.groupby('Date')
#st.dataframe(sql_result)
st.dataframe(csv)

