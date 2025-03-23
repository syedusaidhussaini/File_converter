import streamlit as st
import os
import pandas as pd
from io import BytesIO


st.set_page_config(page_title="Work Cleaner", page_icon="🧹", layout="wide")
st.title("Work Cleaner & Data Analysis")
st.write("This app is designed to help you clean your work files and analyze your data. You can upload your files and clean them using the tools provided. You can also analyze your data using the data analysis tools provided. The app is designed to be user-friendly and easy to use. Enjoy!")

files = st.file_uploader("Upload your files here",type=["csv","xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
        
        st.subheader(f"Data from {file.name} - Preview")
        st.dataframe(df.head())
        
        if st.checkbox(f"Fill missing values in {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(),inplace=True)
            st.success("Missing values filled successfully!")
            st.dataframe(df.head())
            
        selected_columns = st.multiselect(f"Select columns to drop - {file.name}",df.columns,default= df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())
        
        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])
            
        format_choices = st.radio(f"Convert {file.name} to",["csv","xlsx"], key = file.name)
        
        if st.button(f"Download {file.name} as {format_choices}"):
            output = BytesIO()
            if format_choices == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")
            output.seek(0)
            st.download_button(f"Download file", file_name = new_name,data=output,mime=mime)
            
            st.success(f"{file.name} cleaned and downloaded successfully!")