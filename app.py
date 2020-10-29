import streamlit as st
import pandas as pd
import numpy as np
import time

def main():
  st.title('Arabic Sentiment Analysis') # title
  st.subheader("Abed Khooli - @akhooli")

  with st.spinner('Loading something ...'):
    time.sleep(2)
    
  slot1 = st.empty()
  # run the app 
  run_the_app()
  
  
def run_the_app():
  slot1.text('run executed')
  return 'success'
# main statup
if __name__ == "__main__":
    main()
