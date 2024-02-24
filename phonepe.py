import streamlit as st
from streamlit_option_menu import option_menu 
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json


#dataframe creation

#sql connection 

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data",
                      password="12345")

cursor=mydb.cursor()

#aggre_insurance_df

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type",
                                             "Transaction_count","Transaction_amount"))


#aggre_transaction_df

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type",
                                             "Transaction_count","Transaction_amount"))



#aggre_user_df

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("States","Years","Quarter","Brands",
                                             "Transaction_count","Percentage"))



#map_insurance_df

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

map_insurance=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts",
                                             "Transaction_count","Transaction_amount"))


#map_transaction_df

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

map_transaction=pd.DataFrame(table5,columns=("States","Years","Quarter","Districts",
                                             "Transaction_count","Transaction_amount"))

#map_user_df
 
 
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

map_user=pd.DataFrame(table6,columns=("States","Years","Quarter","Districts",
                                             "RegisteredUsers","AppOpens"))


#top_insurance_df


cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes",
                                             "Transaction_count","Transaction_amount"))

#top_transaction_df

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

top_transaction=pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes",
                                             "Transaction_count","Transaction_amount"))


#top_user_df

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

top_user=pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes",
                                             "RegisteredUsers"))






#function for chart 

def Transaction_amount_count_Y(df, year):


    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:


        fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)

    tacy=Aggre_insurance[Aggre_insurance["Years"]==2021]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    with col2:
        fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_count)
    

    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)
        states_name=[]
        for feature in data["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson=data,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                height=650,width=600)
        
        fig_india_1.update_geos(visible=False)
        
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2=px.choropleth(tacyg,geojson=data,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                                height=650,width=600)
        
        fig_india_2.update_geos(visible=False)
        
        st.plotly_chart(fig_india_2)

    return tacy



def Transaction_amount_count_Y_Q(df, quarter):
    
    tacy=df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    #return tacy
    
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{tacy['Years'].unique()[0]} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount)


    tacy=Aggre_insurance[Aggre_insurance["Years"]==2021]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)


    with col2:
        fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:    

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)
        states_name=[]
        for feature in data["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson=data,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States",title=f"{tacy['Years'].unique()} Year {quarter} QUARTER TRANSACTION AMOUNT",fitbounds="locations",
                                height=650,width=600)
        
        fig_india_1.update_geos(visible=False)
        
        st.plotly_chart(fig_india_1)

    
    with col2:

        fig_india_2=px.choropleth(tacyg,geojson=data,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="States",title=f"{tacy['Years'].unique()} Year {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations",
                                height=650,width=600)
        
        fig_india_2.update_geos(visible=False)
        
        st.plotly_chart(fig_india_2)




    
#streamlit part 

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    
    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select =="HOME":
    pass

elif select=="DATA EXPLORATION":

    tab1,tab2,tab3=st.tabs(["Aggregated analysis","Map Analysis","Top Analysis"])

    with tab1:

        method=st.radio("Select the method",["Aggregated Insurance ","Aggregated Transaction ","Aggregated User"])
        
        if method=="Aggregated Insurance ":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y= Transaction_amount_count_Y(Aggre_insurance, years)
            
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select The Quarter",Aggre_insurance["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarters)
        elif method=="Aggregated Transaction":
            pass
        elif method=="Aggregated User":
            pass
    
    with tab2:
        method_2=st.radio("Select the method",["Map Insurance","Map Transaction","Map user"])

        if method=="Map Insurance":
            pass
        elif method=="Map Transaction":
            pass
        elif method=="Map user":
            pass 

    with tab3:
        method_3=st.radio("Select the method",["Top Insurance","Top Transaction","Top user"])

        if method=="Top Insurance":
            pass
        elif method=="Top Transaction":
            pass
        elif method=="Top user":
            pass 

elif select=="TOP CHARTS":
    pass