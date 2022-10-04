#!/usr/bin/env python


#from operator import index
import pandas as pd
import numpy as np
import joblib
import streamlit as st


Anomaly_Model = joblib.load("Anaomaly_Model_joblib")

input_data = ("10:45","3BLTE",11.642,	1.393,0.37,	0.041,15.655,0.644,1.114,1.025,4,3,7)
input_dataframe = {"Time": "10:45", "CellName": "3BLTE", "PRBUsageUL": 11.642, "PRBUsageDL": 1.393, "meanThr_DL": 0.37, "meanThr_UL": 0.041, "maxThr_DL":15.655,"maxThr_UL":0.644,"meanUE_DL":1.114,"meanUE_UL":1.025,"maxUE_DL":4,	"maxUE_UL":3,"maxUE_UL+DL":7}


# Preprocess data (Getting Test Dataset in the same format as training dataset)
def Anomaly_Prediction(df):
    #Data Manipulation
    key = ["Time","CellName","PRBUsageUL","PRBUsageDL","meanThr_DL","meanThr_UL","maxThr_DL","maxThr_UL","meanUE_DL","meanUE_UL","maxUE_DL","maxUE_UL","maxUE_UL+DL"]
    df =  dict(zip(key,df))
    df = pd.DataFrame([df])

    #Parse TimeStamp
    # df.Time = pd.to_datetime(df.Time.str.lower(), format="%H:%M")
    df.Time = pd.to_datetime(df.Time, format="%H:%M")

    #Convert Unusual Column to Object Data Type
    # df.Unusual = df.Unusual.astype('object')
    
    #Convert maxUE_DL Column to Object Data Type
    df.maxUE_DL = df.maxUE_DL.astype('object')

    #Convert maxUE_UL Column to Object Data Type
    df.maxUE_UL = df.maxUE_UL.astype('object')

    #Convert maxUE_UL+DL Column to Object Data Type
    df['maxUE_UL+DL'] = df['maxUE_UL+DL'].astype('object')
    
    #Convert Object Data Type to Category
    for label, content in df.items():
        if pd.api.types.is_string_dtype(content):
            df[label] = content.astype("category").cat.as_ordered()
            
     #Fill in Numerical Columns with the median
            if pd.api.types.is_float_dtype(content):
                 if pd.isnull(content).sum():
                    df[label] = content.fillna(content.median())
                    
     
      #Fill in Categorical Columns with the mode
            if pd.api.types.is_categorical_dtype(content):
                if pd.isnull(content).sum():
                    print(label)
                    df[label] = content.fillna(content.value_counts().index[0]) 
                    
    
        # Feature Enginering on Date Column             
    df['Year'] = df.Time.dt.year
    df['Month'] = df.Time.dt.month
    df['Day'] = df.Time.dt.day        
    df['Hour'] = df.Time.dt.hour
    df['Min'] = df.Time.dt.minute
    df['Seconds'] = df.Time.dt.second
        
        # Drop Year, Month, Day and Second Column
    df.drop('Year', axis = 1,inplace = True)
    df.drop('Month', axis = 1, inplace = True)
    df.drop('Day', axis = 1, inplace = True)
    df.drop('Seconds', axis = 1, inplace = True)
    df.drop('Time',axis = 1, inplace = True)      
          
        # Encoding Categorical Columns    
    for label, content in df.items():
        if not pd.api.types.is_numeric_dtype(content):
                # We add the +1 because pandas encodes missing categories as -1
            df[label] = pd.Categorical(content).codes+1    
                
    prediction = Anomaly_Model.predict(df)
    result = ''
    if prediction[0] == 1:
        return "This is an Anomaly"
        #print("This is an Anomaly")
    else:
        return "This is normal"
    

def main():
    # Page Title
    st.title("Cell Tower Anomaly Detection Web App")
    
    # getting the input data from the user
    Time = st.text_input("Time(HH:MM)")	
    CellName = st.text_input("CellName")	
    PRBUsageUL = st.text_input("PRBUsageUL")	
    PRBUsageDL = st.text_input("PRBUsageDL")	
    meanThr_DL = st.text_input("meanThr_DL")	
    meanThr_UL = st.text_input("meanThr_UL")	
    maxThr_DL = st.text_input("maxThr_DL")	
    maxThr_UL = st.text_input("maxThr_UL")	
    meanUE_DL = st.text_input("meanUE_DL")	
    meanUE_UL = st.text_input("meanUE_UL")	
    maxUE_DL = st.text_input("maxUE_DL")	
    maxUE_UL = st.text_input("maxUE_UL")	
    maxUE_UL_DL = st.text_input("maxUE_UL_DL")

    # Code for prediction
    result = ""
    
    #Creating button fro prediction
    if st.button("Train"):
        result = Anomaly_Prediction([Time,CellName,PRBUsageUL,PRBUsageDL,meanThr_DL,meanThr_UL,maxThr_DL,maxThr_UL,meanUE_DL,meanUE_UL,maxUE_DL,maxUE_UL,maxUE_UL_DL])

    st.success(result)

if __name__=="__main__":
    main()
