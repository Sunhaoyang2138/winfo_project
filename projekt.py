import streamlit as st       
import pandas as pd    

st.title("Daten Analyse")

st.write("""
eine kurze Beschreibung der Analyse
""")

dataset_name = st.selectbox("Select Dataset", ("Sollfahrtdaten", "Istfahrtdaten"))
st.write(dataset_name)
