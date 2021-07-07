import streamlit as st       
import pandas as pd  
import numpy as np  
import datetime

#read the files and conbine the datasets
df1 = pd.read_csv('592M_expected.csv', sep=";")
df2 = pd.read_csv('592M_actual.csv', sep=";")
cd = [df1, df2] #cd = combine datasets
result = pd.concat(cd)

st.title("Projekt")

st.text("eine kurze Beschreibung der Analyse")

dataset_name = st.selectbox("Select Dataset", ("Sollfahrtdaten", "Istfahrtdaten", "Zusammenführung der Datensätze"))
st.write(dataset_name)

def get_dataset(dataset_name):
    if dataset_name == "Sollfahrtdaten":
        csv = df1

    elif dataset_name == "Istfahrtdaten":
        csv = df2

    else:
        csv = result
    return csv
df = get_dataset(dataset_name)

df.sort_values('Date', ascending = True, inplace = True) #chronologische Reihenfolge
df1['Date'] = df1['Date'].str.strip()
df2['Date'] = df2['Date'].str.strip()
result['Date'] = result['Date'].str.strip()
df.set_index(['Date'], drop = True, inplace = True) # Set date as index

st.dataframe(df, 500, 500)

#Allgemeine Analyse
st.header('Allgemeine Informationen über die Datensätze')
st.text("Unsere Fallstudie bezieht sich auf zwei Datensätze: die Soll- und Istfahrtdaten. ")

#Reihen- und Kolonnenanzahl
st.text("Reihen- und Kolonnenanzahl der Sollfahrtdaten")
df1.shape
st.text("Reihen- und Kolonnenanzahl der Istfahrtdaten")
df2.shape
st.text("Reihen- und Kolonnenanzahl der Datenzusammenführung")
result.shape

#Datensätzereinigung
st.text("Kolonnen mit üner 90% 'nan'-Wert entfernen")
def drop_col(df, cutoff=0.1):
    n = len(df)
    cnt = df.count()
    cnt = cnt / n
    
    return df.loc[:, cnt[cnt >= cutoff].index]
st.text("Sollfahrtdaten nach Reinigung")
df1_cut = drop_col(df1)
df1_cut.shape
st.text("Istfahrtdaten nach Reinigung")
df2_cut = drop_col(df2)
df2_cut.shape
st.text("Datenzusammenführung nach Reinigung")
result_cut = drop_col(result)
result_cut.shape

#Headerinfos
st.text("Welche Kolonnen gibt es?")
df1.columns
df2.columns
result.columns

#value_counts
st.text("Value Counts nach EventType und nodeId")
st.dataframe(result.groupby(['TripType'])['EventType'].value_counts())
st.dataframe(result.groupby(['TripType'])['EventType.1'].value_counts())
st.dataframe(result.groupby(['TripType'])['EventType.2'].value_counts())
st.dataframe(result.groupby(['TripType'])['nodeId'].value_counts())
st.dataframe(result.groupby(['TripType'])['nodeId.1'].value_counts())
st.dataframe(result.groupby(['TripType'])['nodeId.2'].value_counts())

#Wie viele Haltstelle gibt es?

#Was ist die Standart Route von dem Zug 592M? (nur Ansatz)
st.dataframe(result.groupby(['TripType'])['EventType'].value_counts().idxmax())
st.dataframe(result.groupby(['TripType'])['nodeId'].value_counts().idxmax())

#Welche Daten sind Wochenende?
df1['eventTime'] = pd.to_datetime(df1['eventTime'], format = '%Y-%m %H:%M:&S' )
st.dataframe(df1['eventTime'])
#Aufteilung nach Jahreszeiten