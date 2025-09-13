import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import guardrails
from agent import DataCollector, DataCleaner, DataAnalyst
import os
from io import StringIO, BytesIO
import PyPDF2

# Streamlit page config
st.set_page_config(page_title="BI/Data Analysis Agent", page_icon="📊", layout="wide")
st.title("Business Intelligence Agent")

# --- Step 1: User Input ---
user_input = st.text_input("Enter your query or instructions for analysis:")

# --- Step 2: File upload ---
st.subheader("Upload your data files (CSV, Excel, TXT, PDF)")
uploaded_files = st.file_uploader("Choose files", type=["csv","xlsx","xls","txt","pdf"], accept_multiple_files=True)

# Function to read uploaded file
def read_file(file):
    name = file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file)
    elif name.endswith(".xls") or name.endswith(".xlsx"):
        return pd.read_excel(file)
    elif name.endswith(".txt"):
        return pd.DataFrame({"text": file.getvalue().decode("utf-8").splitlines()})
    elif name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file)
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        return pd.DataFrame({"text": text.splitlines()})
    else:
        return None

# --- Step 3: Run Analysis ---
if st.button("Run Analysis"):

    # Check guardrails for user input
    if not guardrails.check_input(user_input):
        st.error("Blocked: sensitive input detected")
    else:
        # Collect data
        collector = DataCollector()
        raw_data = collector.run(user_input)

        # Include uploaded files
        file_dfs = []
        for file in uploaded_files:
            df = read_file(file)
            if df is not None:
                file_dfs.append(df)

        if file_dfs:
            uploaded_df = pd.concat(file_dfs, ignore_index=True)
            st.subheader("Uploaded Data Preview")
            st.dataframe(uploaded_df.head())
        else:
            uploaded_df = pd.DataFrame()

        # Merge collected data and uploaded files if both exist
        if isinstance(raw_data, dict):
            raw_df = pd.DataFrame(raw_data)
        else:
            raw_df = pd.DataFrame(raw_data)

        if not uploaded_df.empty and not raw_df.empty:
            combined_data = pd.concat([raw_df, uploaded_df], ignore_index=True)
        elif not uploaded_df.empty:
            combined_data = uploaded_df
        else:
            combined_data = raw_df

        # Clean data
        cleaner = DataCleaner()
        cleaned_data = cleaner.run(combined_data)

        # Analyze data
        analyst = DataAnalyst()
        report = analyst.run(cleaned_data)

        # Check guardrails for output
        if not guardrails.check_output(report):
            st.error("Blocked: sensitive output detected")
        else:
            st.success("Analysis completed!")
            st.subheader("Analysis Report")
            st.write(report)

            # Display cleaned data
            st.subheader("Cleaned Data")
            if isinstance(cleaned_data, pd.DataFrame):
                st.dataframe(cleaned_data)
            else:
                st.write(cleaned_data)

            # --- Matplotlib example ---
            st.subheader("Matplotlib Chart Example")
            fig, ax = plt.subplots()
            if isinstance(cleaned_data, pd.DataFrame) and not cleaned_data.empty:
                ax.bar(cleaned_data.index, range(len(cleaned_data)))
            st.pyplot(fig)

            # --- Plotly example ---
            st.subheader("Plotly Chart Example")
            if isinstance(cleaned_data, pd.DataFrame) and not cleaned_data.empty:
                fig2 = px.bar(cleaned_data, x=cleaned_data.columns[0], y=range(len(cleaned_data)))
                st.plotly_chart(fig2)
