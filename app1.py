# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 11:36:58 2023

@author: sangeetha
"""

# Step 1: Import necessary libraries
import pandas as pd
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Step 2: Build a Streamlit app
st.title('Allele1 Summary and PDF Generation')
    
# Step 3: Upload the gene data file
uploaded_file = st.file_uploader("Upload your gene data here (CSV format)", type=["csv"])


# Step 4: Load and preprocess the uploaded data
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
    # Replace 'your_raw_data.csv' with the actual filename or path
        raw_data = pd.read_csv(uploaded_file)
    #raw_data = pd.read_csv('input25rows.csv')
        return raw_data
    return None

data = load_data(uploaded_file)

# Step 5: Display the raw data if available
if data is not None:
    st.subheader('Raw Data')
    st.dataframe(data)


    # Step 6: Perform summarization based on 'allele1'
    def summarize_data(data):
        summary = data.groupby('allele1')['rsid'].count().reset_index()
        summary.columns = ['allele1', 'count']
        return summary


    summary = summarize_data(data)

    # Step 7: Show the summary
    st.subheader('Summary based on Allele1')
    st.dataframe(summary)
        
    # Step 8: Create a PDF report
    
    if st.button('Generate PDF'):
        def create_pdf(summary):
            c = canvas.Canvas('allele1_summary.pdf', pagesize=letter)
            c.drawString(100, 750, 'Summary of Allele1')
    
            table_data = [list(summary.columns)] + summary.values.tolist()
    
            for i, row in enumerate(table_data):
                for j, val in enumerate(row):
                    c.drawString(50 + j * 100, 720 - i * 20, str(val))

            c.save()

        create_pdf(summary)
        st.success('PDF report generated successfully as allele1_summary.pdf')
        
        
        # Step 9: Provide a link for the client to download the PDF
        st.subheader('Download PDF Report')
        pdf_link = f'<a href="allele1_summary.pdf" download>Click here to download the PDF</a>'
        st.markdown(pdf_link, unsafe_allow_html=True)
else:
    st.warning('Please upload a CSV file to begin.')





