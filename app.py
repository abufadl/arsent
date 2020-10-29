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
  with st.spinner('Loading something ...'):
    time.sleep(2)
    
  slot1 = st.empty()
  # run the app 
  run_the_app()
  
  
def run_the_app():
  #slot1.text('run executed')
  return 'success'


# Download a single file and make its content available as a string.
@st.cache(show_spinner=False)
def get_file_content_as_string(path):
  url = 'https://raw.githubusercontent.com/abufadl/asa/' + path
  response = urllib.request.urlopen(url)
  return response.read().decode("utf-8")



# main statup
if __name__ == "__main__":
    main()
