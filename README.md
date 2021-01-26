# About this app  [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/abufadl/arsent/app.py)
# التحليل العاطفي للنصوص العربية 
يعمل هذا التطبيق على تحليل المشاعر للنصوص العربية وخاصة مراجعات وتقييمات الخدمات كالفنادق والمطاعم والكتب وشركات الطيران، ويعتمد على نموذج لغوي مبني على التعلم العميق باستخدام تقنية 
BERT للغة العربية من مختبر الذكاء الصناعي التابع للجامعة الأمريكية في بيروت.

Arabic Sentiment Analysis - App powered by [Streamlit](https://docs.streamlit.io/)  
The model behind this app was trained on around 600k positive and negative reviews (hotels, restaurants, products, movies, books and a few airlines) using the [Flair NLP](https://github.com/flairNLP/flair/) library by fine-tuning the [AraBERT base v2](https://huggingface.co/aubmindlab/bert-base-arabertv02) language model, developed by the [AUB Mind Lab](sites.aub.edu.lb/mindlab/) from Huggingface. It was not fully trained (__around 95.6% accuracy__).    
The first time you run the app, it will download around 520 MB (not to your device, but to the app server). This may take a few seconds (up to 5).  
This app is hosted on __Streamlit__ servers using a free/shared plan with minimum resources. It is not production ready.  
For more about the origins of the dataset, please see the [Arabic 100k Reviews](https://www.kaggle.com/abedkhooli/arabic-100k-reviews) on Kaggle (description section).   
If you have questions or comments, please ask via [Twitter](https://twitter.com/akhooli) or in the [LinkedIn post about this app](https://www.linkedin.com/posts/akhooli_flairnlp-streamlit-sentimentanalysis-activity-6728033724958572544-r-ap).


