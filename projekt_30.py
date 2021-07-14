import streamlit as st       
import pandas as pd  
import numpy as np  
from datetime import datetime

#create sections with containers
header = st.beta_container()
data_display = st.beta_container()

#read the files and conbine the datasets
df_exp = pd.read_csv('592M_expected.csv', sep=";")
df_act = pd.read_csv('592M_actual.csv', sep=";")
cd = [df_exp, df_act] #cd = combine datasets
df_cd = pd.concat(cd)
#read the files with lesser data
df_exp_30 = pd.read_csv('592M_expected_30.csv', sep=";")
df_act_30 = pd.read_csv('592M_actual_30.csv', sep=";")
cd_30 = [df_exp, df_act]
df_cd_30 = pd.concat(cd)

with header:
    st.title("Algorithmus-Design zur Aufbereitung und Analyse von Zugfahrtdaten")

    st.markdown("Die Schlusspräsentation von **_Tom_ Lobry** und **_Haoyang_ Sun**")
    st.text("Hier kommt die Gliederung hin.") 
    st.text("Unsere Fallstudie bezieht sich auf zwei Datensätze: die Soll- und Istfahrtdaten. ")

with data_display:
    dataset_name = st.selectbox("Datensätze selektieren", ("Sollfahrtdaten", "Istfahrtdaten", "Zusammenführung der Datensätze"))

    def get_dataset(dataset_name):
        if dataset_name == "Sollfahrtdaten":
            csv = df_exp

        elif dataset_name == "Istfahrtdaten":
            csv = df_act

        else:
            csv = df_cd
        return csv
    df = get_dataset(dataset_name)

    df.sort_values('Date', ascending = True, inplace = True) #chronologische Reihenfolge
    df['Date'] = df['Date'].str.strip()
    df.set_index(['Date'], drop = True, inplace = True) # Set date as index

    st.dataframe(df)
    basic = "Der Datensatz '" + str(dataset_name) + "' hat " + str(df.shape[0]) + " Reihen und " + str(df.shape[1]) + " Spalten, und insgeamt gibt es " + str(df.size) + " Elementen inklusiv die NaN-Werte."
    st.write(basic)

#Allgemeine Analyse
st.header('Allgemeine Informationen über die Datensätze')

st.subheader("**I.** Datensatz kennenlernen")
#create columns sections
soll_col, ist_col, cd_col = st.beta_columns(3)
#Reihen- und Kolonnenanzahl
soll_col.text("1. Sollfahrtdaten")
soll_col.write(df_exp.shape)
ist_col.text("2. Istfahrtdaten")
ist_col.write(df_act.shape)
cd_col.text("3. Datasatz der Zusammenführung")
cd_col.write(df_cd.shape)

#Datensätzereinigung
st.subheader("**II.** Datenreinigung: Spalten mit üner 90% 'nan'-Wert entfernen")
def drop_col(df, cutoff=0.1):
    n = len(df)
    cnt = df.count()
    cnt = cnt / n
    
    return df.loc[:, cnt[cnt >= cutoff].index]
soll_col_2, ist_col_2, cd_col_2 = st.beta_columns(3)
soll_col_2.text("1. Sollfahrtdaten")
df_exp_cut = drop_col(df_exp)
soll_col_2.write(df_exp_cut.shape)
ist_col_2.text("2. Istfahrtdaten")
df_act_cut = drop_col(df_act)
ist_col_2.write(df_act_cut.shape)
cd_col_2.text("3. Datasatz der Zusammenführung")
df_cd_cut = drop_col(df_cd)
cd_col_2.write(df_cd_cut.shape)

exp_cut = df_exp.shape[1] - df_exp_cut.shape[1]
act_cut = df_act.shape[1] - df_act_cut.shape[1]
cd_cut = df_cd.shape[1] - df_cd_cut.shape[1]
cut_exp = "Bei Sollfahrtdaten werden " + str(exp_cut) + " Spalten, bzw. " + str(exp_cut * df_exp_cut.shape[0]) + " Elementen und fehlende Werten ausgeschloßen."
st.write(cut_exp)
cut_act = "Bei Istfahrtdaten werden " + str(act_cut) + " Spalten, bzw. " + str(act_cut * df_act_cut.shape[0]) + " Elementen und fehlende Werten ausgeschloßen."
st.write(cut_act)
cut_cd = "Bei dem Datensatz der Zusammenführung werden " + str(cd_cut) + " Spalten, bzw. " + str(cd_cut * df_cd_cut.shape[0]) + " Elementen und fehlende Werten ausgeschloßen."
st.write(cut_cd)

st.subheader("**III.** Aus welchem Zeitraum bestehen die Datensätze")
#reset index
df_cd = df_cd.reset_index(drop = True)
st.markdown('* das Anfangsdatum: ' + df_cd['Date'].min())
st.markdown('* das Enddatum: ' + df_cd['Date'].max())
st.text('Die Datensätze befinden sich in dem Zeitraum zwischen ' + df_cd['Date'].min() + ' bis zum ' + df_cd['Date'].max())
st.markdown('* Datenunterschied zwischen Sollfahrtdaten und Istfahrtdaten')
st.text('Es wird 361 Tagen geplannt, aber nur 357 Tagen werden dokumentiert. ')
st.text('In der Istfahrtdaten beinhaltet nicht die folgende Tagen : ')
df_cd_gpby = df_cd.groupby(list(df_cd.Date))
idx = [x[0] for x in df_cd_gpby.groups.values() if len(x) == 1]
df_cd_differ = df_cd.reindex(idx)
df_cd_differ.set_index(['Date'], drop = True, inplace = True)
st.dataframe(df_cd_differ)
#delete those four rows that has no istfahrtdaten informations
df_cd_cut.drop(index = df_cd_cut[df_cd.reindex(idx)].index)
st.write(df_cd_cut.shape)


#reset index
df_cd = df_cd.reset_index(drop = True)






#value_counts
st.text("Value Counts nach EventType und nodeId")
st.dataframe(result.groupby(['TripType'])['EventType'].value_counts())
st.dataframe(result.groupby(['TripType'])['EventType.1'].value_counts())
st.dataframe(result.groupby(['TripType'])['EventType.2'].value_counts())
st.dataframe(result.groupby(['TripType'])['nodeId'].value_counts())
st.dataframe(result.groupby(['TripType'])['nodeId.1'].value_counts())
st.dataframe(result.groupby(['TripType'])['nodeId.2'].value_counts())

#Was ist die Standart Route von dem Zug 592M? Und wie viele Haltstelle durchschnittlich gibt es? (nur Ansatz) 
st.dataframe(result.groupby(['TripType'])['EventType'].value_counts().idxmax())
st.dataframe(result.groupby(['TripType'])['nodeId'].value_counts().idxmax())
st.dataframe(result.groupby(['TripType'])['nodeId.1'].value_counts().idxmax())
st.dataframe(result.groupby(['TripType'])['nodeId.2'].value_counts().idxmax())
st.dataframe(result.groupby(['TripType'])['nodeId.3'].value_counts().idxmax())
st.dataframe(result.groupby(['TripType'])['nodeId.4'].value_counts().idxmax())

#dataset_name = st.selectbox("Select Dataset", ("Sollfahrtdaten(new)", "Istfahrtdaten(new)", "Zusammenführung der Datensätze(new)"))
#st.write(dataset_name)

#def value_count(df):
    #for name, values in df.iteritems():
         #if dataset_name == "Sollfahrtdaten(new)":
         #df_value_counts = df1_cut.iteritems().value_counts().idxmax()

         #elif dataset_name == "Istfahrtdaten(new)":
             #df_value_counts = df2_cut.iteritems().value_counts().idxmax()

         #else:
             #df_value_counts = result_cut.iteritems().value_counts().idxmax()
         #return df_value_count
   
       
#df = value_count(df)

#st.write(df)







#Welche Daten sind Wochenende?
datetime.strptime('2015-12-13T16:28:54', '%Y-%m-%dT%H:%M:%S')
st.dataframe(result['eventTime'])




#Aufteilung nach Jahreszeiten
#df['Month'] = df['eventTime'].str[0:2]
#df['Month'] = df['Month'].astype('int32')
#st.dataframe(df.head())