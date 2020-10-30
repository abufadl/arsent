from flair.data import Sentence
from flair.models import TextClassifier
import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import shutil
import re
import urllib
import asyncio
import aiohttp
from pathlib import Path
import torch


def main():
st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
	page_title=None,  # String or None. Strings get appended with "• Streamlit". 
	page_icon=None,  # String, anything supported by st.image, or None.
)
    st.title('Arabic Sentiment Analysis') # title
    st.subheader("Abed Khooli - @akhooli")
    # Render the readme as markdown using st.markdown.
    readme_text = st.markdown(get_file_content_as_string("README.md"))
    #with st.spinner('Loading something ...'):
    #       time.sleep(2)
  
    
    #debug
    #st.write(f'we think the path is: { path} while data path is {data_path} and path_t is {path_t}') 
    #st.write(f'path_t contents: {path_t.ls()}')
    #st.write(f'path contents: {path.ls()}')    

    

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
    
# download the pickle file 
def download_file(url , dest):
	if  dest.exists(): return
	file_warning, progress_bar = None, None
	try:
		file_warning = st.warning(f"Downloading {url}")
		progress_bar = st.progress(0)
		with open(dest, "wb") as output_file:
			with urllib.request.urlopen(url) as response:
				length = int(response.info()["Content-Length"])
				counter = 0.0
				MEGABYTES = 2.0 ** 20.0
				while True:
					data = response.read(8192)
					if not data:
						break
					counter += len(data)
					output_file.write(data)

					# We perform animation by overwriting the elements.
					file_warning.warning(f"Downloading ... {counter}/{length} MB")
					progress_bar.progress(min(counter / length, 1.0))

	# Finally, we remove these visual elements by calling .empty().
	finally:
		if file_warning is not None:
			file_warning.empty()
		if progress_bar is not None:
			progress_bar.empty()
            
  
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

def run_the_app():

	export_file_url = 'https://www.googleapis.com/drive/v3/files/1fsOISLHSk7qp_fZ8_bGwl0uRi2mZujbR?alt=media&key=AIzaSyArnAhtI95SoFCexh97Xyi0JHI03ghd-_0'
	export_file_name = 'arsent_bmc3.pt'

	classes = ['Negative', 'Positive']
	#defaults.device = torch.device('cpu')

	accents = re.compile(r'[\u064b-\u0652\u0640]') # harakaat and tatweel (kashida) to remove  
	arabic_punc = re.compile(r'[\u0621-\u063A\u0641-\u064A\u061b\u061f\u060c\u003A\u003D\u002E\u002F\u007C]+') # to keep 
	def clean_text(x):
		return ' '.join(arabic_punc.findall(accents.sub('',x)))
	path = Path('.')
	download_file(export_file_url, path/export_file_name)
	classifier = TextClassifier.load('arsent_bmc3.pt')
	
	text_data = st.text_input('Review (Press ENTER to apply)', 'استمتعت بالإقامة في الفندق الفخم وكان الطعام جيدا.', max_chars=250)
	sentence = Sentence(clean_text(text_data.strip()))
	classifier.predict(sentence)
	#st.text("app ran successfully.")
	st.write(sentence.labels[0])

	
# Download a single file and make its content available as a string. https://raw.githubusercontent.com/abufadl/asa/master/
@st.cache(show_spinner=False)
def get_file_content_as_string(path2):
    url = 'https://raw.githubusercontent.com/abufadl/asa/master/' + path2
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")



# main statup
if __name__ == "__main__":
    main()
