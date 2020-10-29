from fastai.text import *
import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import shutil
import re
import urllib


def main():
    st.title('Arabic Sentiment Analysis') # title
    st.subheader("Abed Khooli - @akhooli")
    # Render the readme as markdown using st.markdown.
    readme_text = st.markdown(get_file_content_as_string("README.md"))
    #with st.spinner('Loading something ...'):
    #       time.sleep(2)
 

  # Once we have the dependencies, add a selector for the app mode on the sidebar.
    st.sidebar.title("Main Menu")
    app_mode = st.sidebar.selectbox("Select an option",
        ["Show background info", "Run the app", "Show the source code"])
    if app_mode == "Show background info":
        st.sidebar.success('To continue select "Run the app".')
    elif app_mode == "Show the source code":
        readme_text.empty()
        st.code(get_file_content_as_string("app.py"))
    elif app_mode == "Run the app":
        readme_text.empty()
        run_the_app()
    # run the app 
    #run_the_app()
  
  
def run_the_app():
    st.text("app ran successfully.")
    return 'success'


# Download a single file and make its content available as a string. https://raw.githubusercontent.com/abufadl/asa/master/
@st.cache(show_spinner=False)
def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/abufadl/asa/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")



# main statup
if __name__ == "__main__":
    main()
