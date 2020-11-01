# About this app 
# التحليل العاطفي للنصوص العربية 
يعمل هذا التطبيق على تحليل المشاعر للنصوص العربية وخاصة مراجعات وتقييمات الخدمات كالفنادق والمطاعم والكتب وشركات الطيران، ويعتمد على نموذج لغوي مبني على التعلم العميق.

Arabic Sentiment Analysis - App powered by [Streamlit](https://docs.streamlit.io/)  
The model behind this app was trained on 200k positive and negative reviews (hotels, restaurants, products, movies, books and a few airlines) using the [Flair NLP](https://github.com/flairNLP/flair/) library by fine-tuning the [bert-base-multilingual-cased](https://huggingface.co/bert-base-multilingual-cased) language model from Huggingface. It was not fully trained (__around 90% accuracy__).    
The first time you run the app, it will download around 700 MB (not to your device, but to the app server). This may take a few seconds (up to 5).  
This app is hosted on __Streamlit__ servers using a free/shared plan with minimum resources. It is not production ready.  
For more about the origins of the dataset, please see the [Arabic 100k Reviews](https://www.kaggle.com/abedkhooli/arabic-100k-reviews) on Kaggle.   
If you have questions or comments, please ask via Twitter or in the [LinkedIn post about this app](https://www.linkedin.com/posts/akhooli_flairnlp-streamlit-sentimentanalysis-activity-6728033724958572544-r-ap).


