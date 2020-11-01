from flair.data import Sentence
from flair.models import TextClassifier
import streamlit as st
import re
import urllib
from pathlib import Path
from PIL import Image
import random

st.beta_set_page_config( # Alternate names: setup_page, page, layout
	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
	page_title="Arabic Sentiment Analysis",  # String or None. Strings get appended with "• Streamlit". 
	page_icon=None,  # String, anything supported by st.image, or None.
	)

def main():	
	st.title('Arabic Sentiment Analysis: Service Reviews') # title
	st.subheader("By Abed Khooli - Twitter: @akhooli, LinkedIn: /in/akhooli")
	display_image('sent_pn.png')	
	# Render the readme as markdown using st.markdown.
	readme_text = st.markdown(get_file_content_as_string("README.md"))

	# Once we have the dependencies, add a selector for the app mode on the sidebar.
	st.sidebar.title("Main Menu")
	app_mode = st.sidebar.selectbox("Select an option",
				["Show background info", "Run the app", "Show the source code"])
	if app_mode == "Show background info":
		st.sidebar.success('To run this app select "Run the app" from the drop down list.')
	elif app_mode == "Show the source code":
		readme_text.empty()
		st.code(get_file_content_as_string("app.py"))
	elif app_mode == "Run the app":
		readme_text.empty()
		st.sidebar.info("Note: the app ignores non-Arabic text as well as diacritics.")
		run_the_app()
    
# display image 
def display_image(fn):
	image = Image.open(fn)
	st.image(image, caption=None, width=None, use_column_width=False)

# download the pt file 
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
					file_warning.warning(f"Downloading model ... {counter/MEGABYTES}/{length/MEGABYTES} MB")
					progress_bar.progress(min(counter / length, 1.0))

	# Finally, we remove these visual elements by calling .empty().
	finally:
		if file_warning is not None:
			file_warning.empty()
		if progress_bar is not None:
			progress_bar.empty()
            
RNADOM_REVIEWS = [
	"لا تأخذ منك قرأت توفيق الحكيم غير يوم واحد .. لأن لغته سهبة جدا و حوارية. عصا الحكيم تحاوره في قسمين الأول و هو الأكبر في الدنيا الثاني في الآخره لا ريب في أن الحكيم يعيد بعض أفكاره",
	"غير مرضي . مكان الغرفه وتعامل الموظفين. خداع في حجز الغرف",
	"استثنائي. كل شيء جميل سواء قربه من الحرم او الاسواق وموقعه جدا مناسب بين مصلى الرجال والنساء ، المطعم لذيذ ايضا ، لي عوده ان شالله لهذا الفندق",
	"نجمتان لأنه ألهمني كثيرا ببعض الأفكار والتصاوير الجميلة الخيالية حول الأنا والآخر. وليست خمس نجمات لأنه سطحي وساذج أحيانا ومكرر إلى حد ما زز وملاحظة أخيرة. حاول تجنب منشورات هذه الدار",
	"سي و لا أنصح فيه . لا شي. تعامل موظفين الاستقبال سيء و أسلوبه أسلوب الف و الدوران",
	"أكثر طبق مميز عندهم هو البطاطس المشوي و الذي يتم وضع تشكيلة من السلطة بداخله قد تكفي لوحدها كوجبة رئيسية و سعرها جيد مقارنة بالطعم",
	"سعر في البوكنج مختلف عن الواقع . لا شئ أعجبني. قيمة الحجز في البوكنج لليلتين كانت ريال وعندما ذهبت الى هناك تفاجئت بسعر مختلف ريال لليلة الواحده",
	"كتاب بسيط وجميل ، يلهمك بأن تعاود قراءته مرة واثتان وثلات ... وهو عبارة عن مجموعة من قصص النجاح لأناس بدأو من الصفر",
	"جيد جدا. موقع الفندق قريب من الفعاليات والانشطه الموجوده في جزيره ياس وكبر مساحه الغرف والهدوء والمناظر التي تمتاز بها بعض الغرف التي تطل على ملعب الغولف والبحر وحوض السباحه ولا انسى الاستقبال والترحاب من الموظفين سواء في الاستقبال او عند استلام",
	"أجمل ما في روايات رضوى عاشور أنها تضع التاريخ بين يديك. لا يهمك اثناء قرائتك لروايه لها ان تعرف ماذا حدث لهذا او ذاك. ستصب اهتمامك كله على احداث تاريخيه املا في ان تتغير ولكن هيهات ذاك زمان ولى واندثر ",
	"أثر فيني الفيلم جدا وكنت متحمسة للرواية.. تحمل تفاصيل غير ضرورية ومملة",
	"إن كان هناك أقل من نجمه فهو بالتأكييد من نصيب هذه الروايه وعن جداره نصف نجمه أو ربع نجمه على اقصى تقدير .... أخيرا انتهيت منها دون أن أنجلط أو اكتئب . بصراحه كنت قد نويت ان أسكت ولا أقول شيئا عن هذه الروايه إذا صح تسميتها",	
]

RNADOM_REVIEW = random.choice(RNADOM_REVIEWS)
def run_the_app():

	#export_file_url = 'https://www.googleapis.com/drive/v3/files/1fsOISLHSk7qp_fZ8_bGwl0uRi2mZujbR?alt=media&key=AIzaSyArnAhtI95SoFCexh97Xyi0JHI03ghd-_0'
	export_file_url = 'https://www.googleapis.com/drive/v3/files/1bBaOkwb1magmG-Ref2IK30BwwBP6Y5pY?alt=media&key=AIzaSyArnAhtI95SoFCexh97Xyi0JHI03ghd-_0' 
	#export_file_name = 'arsent_bmc3.pt'
	export_file_name = 'arsent200k.pt'

	accents = re.compile(r'[\u064b-\u0652\u0640]') # harakaat and tatweel (kashida) to remove  
	arabic_punc = re.compile(r'[\u0621-\u063A\u0641-\u064A\u061b\u061f\u060c\u003A\u003D\u002E\u002F\u007C]+') # to keep 
	  
	def check_entry(txt):
		if not txt or len(txt.strip()) < 5:
			return False
		txt_clean = clean_text(txt)
		if len(txt_clean.split()) < 2:
			return False
		return txt_clean

	def clean_text(x):
		return ' '.join(arabic_punc.findall(accents.sub('',x)))
	path = Path('.')
	download_file(export_file_url, path/export_file_name)
	#classifier = TextClassifier.load('arsent_bmc3.pt')
	classifier = TextClassifier.load(export_file_name)
	
	#random_review = random.choice(RNADOM_REVIEWS)
	text_data = st.text_area('Text to analyze: Type or paste an Arabic review. Press the Analyze button.', "مقبول بالنسبة للقيمة . مقبول بالنسبة لقيمة الايجار. عند استلام الغرفة كان بها غبار كثيف وعند تغيرها باخرى لم تكن بمستوى النظافة المطلوبلا يوجد مواقف خاصه بالفندق", max_chars=1000)
	#text_data = st.text_input('Review (Type or paste an Arabic review. Press ENTER to apply)', 'استمتعت بالإقامة في الفندق الفخم وكان الطعام جيدا.', max_chars=250)
	button2press = st.button('Analyze Sentiment')
	if button2press:
		if (check_entry(text_data)):
			sentence = Sentence(clean_text(text_data.strip()))
			classifier.predict(sentence)
			#st.write(sentence.labels[0])
			if str(sentence.labels[0]).startswith('Positive'):
				
				display_image('sent_p.png')
				st.success(sentence.labels[0])
				
			else:
				display_image('sent_n.png')
				st.error(sentence.labels[0])
				
		else:
			st.warning('Invalid entry. Try a few Arabic words at least.')
	else:
		st.write("Thank you for trying out thid app!")
		button2press = False
	
# Download a single file and make its content available as a string. https://raw.githubusercontent.com/abufadl/asa/master/
@st.cache(show_spinner=False)
def get_file_content_as_string(path2):
    url = 'https://raw.githubusercontent.com/abufadl/asa/master/' + path2
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

# main statup
if __name__ == "__main__":
    main()
