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

# Step 2: Load and preprocess the raw file data
@st.cache
def load_data():
    # Replace 'your_raw_data.csv' with the actual filename or path
    raw_data = pd.read_csv('input25rows.csv')
    return raw_data

# Step 3: Perform summarization based on 'allele1'
def summarize_data(data):
    summary = data.groupby('allele1')['rsid'].count().reset_index()
    summary.columns = ['allele1', 'count']
    return summary

# Step 4: Create a PDF report
def create_pdf(summary):
    c = canvas.Canvas('allele1_summary.pdf', pagesize=letter)
    c.drawString(100, 750, 'Summary of Allele1')
    
    table_data = [list(summary.columns)] + summary.values.tolist()
    
    table = st.table(table_data)
    
    c.save()

# Step 5: Build a Streamlit app
def main():
    st.title('Allele1 Summary and PDF Generation')

    # Load data
    data = load_data()

    # Show the raw data
    st.subheader('Raw Data')
    st.dataframe(data)

    # Perform summarization based on 'allele1'
    summary = summarize_data(data)

    # Show the summary
    st.subheader('Summary based on Allele1')
    st.dataframe(summary)

    # Generate PDF
    if st.button('Generate PDF'):
        create_pdf(summary)
        st.success('PDF report generated successfully as allele1_summary.pdf')

if __name__ == "__main__":
    main()
