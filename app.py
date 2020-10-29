from fastai.text import *
import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import shutil
import re
import urllib
import asyncio


def main():
    st.title('Arabic Sentiment Analysis') # title
    st.subheader("Abed Khooli - @akhooli")
    # Render the readme as markdown using st.markdown.
    readme_text = st.markdown(get_file_content_as_string("README.md"))
    #with st.spinner('Loading something ...'):
    #       time.sleep(2)
    #!mkdir -p /root/.fastai/data/arwiki/corpus2_100/tmp/
    data_path = Config.data_path()
    name = f'arwiki/corpus2_100/tmp/'
    path_t = data_path/name
    path_t.mkdir(exist_ok=True, parents=True)
    shutil.copy('./models/spm.model', path_t)

    path = Path(__file__).parent

    export_file_url = 'https://www.googleapis.com/drive/v3/files/11IWumpzKAtw3axw_mBaiwZ-abLL9QZBV?alt=media&key=AIzaSyArnAhtI95SoFCexh97Xyi0JHI03ghd-_0'
    export_file_name = 'ar_classifier_reviews_sp15_multifit_nows_2fp_exp.pkl'
    
    classes = ['Mixed', 'Negative', 'Positive']
    defaults.device = torch.device('cpu')

        #
    async  def  download_file ( url , dest ):
        if  dest . exists (): return
        async  with  aiohttp . ClientSession () as  session :
            async  with  session . get ( url ) as  response :
                data  =  await  response . read ()
                with  open ( dest , 'wb' ) as  f :
                    f . write ( data )


    accents = re.compile(r'[\u064b-\u0652\u0640]') # harakaat and tatweel (kashida) to remove  
    arabic_punc = re.compile(r'[\u0621-\u063A\u0641-\u064A\u061b\u061f\u060c\u003A\u003D\u002E\u002F\u007C]+') # to keep 
    def clean_text(x):
        return ' '.join(arabic_punc.findall(accents.sub('',x)))


    def predict_sentiment(txt):
        if not txt or len(txt.strip()) < 5:
            return JSONResponse({"prediction": "Invalid Entry", "scores": "None", "key": "1 = positive, -1 = negative"})
        txt_clean = clean_text(txt)
        if len(txt_clean.split()) < 2:
            return JSONResponse({"prediction": "Invalid Entry", "scores": "None", "key": "1 = positive, -1 = negative"})
        pred_class, pred_idx, losses = learn.predict(txt_clean)
        print(pred_class)
        print({"prediction": str(pred_class), "scores": sorted(zip(learn.data.classes, map(float, losses)), key=lambda p: p[1], reverse=True)})
        return JSONResponse({"prediction": str(pred_class), "scores": sorted(zip(learn.data.classes, map(float, losses)), key=lambda p: p[1], reverse=True), "key": "1 = positive, -1 = negative"})


    async def setup_learner():
        await download_file(export_file_url, path/export_file_name)
        try:
            learn = load_learner(path, export_file_name)
            return learn
        except RuntimeError as e:
            raise

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
