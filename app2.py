# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 15:42:05 2023

@author: sangeetha
"""

import streamlit as st
import os
import pandas as pd

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
    st.title("File Upload")

    # File upload section
    uploaded_file = st.file_uploader("Upload a genome file here", type=["csv","txt"])

    if uploaded_file is not None:
        # Check if the file is uploaded
        st.success("File uploaded successfully")

        # Save the uploaded file to the input directory
        file_path = os.path.join(glb_01_input, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

       
if __name__ == "__main__":
    main()
