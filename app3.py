# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 12:16:58 2023

@author: sangeetha
"""

#import libraries
import streamlit as st
import os
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas

# Defining folder paths
glb_root = r"C:\Users\sangeetha\OneDrive\DSM_projects\18_data_apps\Microprojects\project2"
glb_01_input = os.path.join(glb_root, "01_input")
glb_02_master = os.path.join(glb_root, "02_master")
glb_03_output = os.path.join(glb_root, "03_output")
glb_04_temp_input = os.path.join(glb_root, "04_temp_input")
glb_masterfile = os.path.join(glb_02_master, "dummy_master.csv")

# Create working directories if not existing
for folder in [glb_root, glb_01_input, glb_03_output, glb_04_temp_input]:
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass


# Streamlit app
def main():
    st.title("File Upload and Report Generation")

    # File upload section
    uploaded_file = st.file_uploader("Upload a genome file here", type=["csv","txt"])

    if uploaded_file is not None:
        # Check if the file is uploaded
        st.success("File uploaded successfully")

        # Save the uploaded file to the input directory
        file_path = os.path.join(glb_01_input, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
            
        # Display a button to generate the report
        if st.button("Generate Report"):
            st.info("Generating the Report...")
            generate_and_display_report(file_path)

def generate_and_display_report(client_csv_path):
    # Load the data from the uploaded file and the master file
    client_data = pd.read_csv(client_csv_path)
    master_data = pd.read_csv(glb_masterfile)
    
    # Merge the dataframes on the 'ID' column
    merged_data = pd.merge(client_data, master_data, on='ID')

    # Group by the client and sum their transaction amounts
    total_spent = merged_data.groupby('Name')['Amount'].sum().reset_index()

    # Generate the report and save in the output path
    report_file_path = os.path.join(glb_03_output,"client_report.pdf")
    generate_report(total_spent, report_file_path)

    # Display the generated report
    st.success("Report generated successfully!")
    st.write("You can download the report from the following link:")
   
    # Create a link to download the report
    with open(report_file_path, "rb") as f:
        bytes_data = f.read()
        st.download_button("Download Report", data=bytes_data, key="report")
    
def generate_report(dataframe,output_file):
    # Create a new PDF with Reportlab
    c = canvas.Canvas(output_file, pagesize=landscape(letter))
    width, height = landscape(letter)
    
    # Set up some constants for padding
    top_margin = 50
    left_margin = 50
    row_height = 25
    current_height = height - top_margin
    
    # Title for the report
    c.setFont("Helvetica-Bold", 20)
    c.drawString(left_margin, current_height, "Total Amount Spent by Each Client")
    current_height -= (1.5 * row_height)
    
    # Write the header row
    headers = ["Name", "Amount"]
    col_widths = [300, 300]
    
    c.setFont("Helvetica-Bold", 14)
    for idx, header in enumerate(headers):
        c.drawString(left_margin + sum(col_widths[:idx]), current_height, header)
    
    current_height -= row_height
    
    # Write the data rows
    c.setFont("Helvetica", 12)
    for _, row in dataframe.iterrows():
        for idx, item in enumerate(row):
            c.drawString(left_margin + sum(col_widths[:idx]), current_height, str(item))
        current_height -= row_height
        
    c.save()


if __name__ == "__main__":
    main()


