"""
 fileName : My_Word_Cloud.py
 Author: Moses Bankole
 Contact: thedevmosesb@gmail.com
 Run Main.py to view the GUI
 Use the requirements.txt file to install the required dependencies.
Code written with python 3.8.3
Tested on Windows

 """
import os
import time

import numpy as np
from PIL import Image as PIL_Image
from wordcloud import WordCloud


class WordCloudGenerator(object):
    """The class Generates a word cloud based on the settings of the word cloud parameters
		set up in the init constructor
	"""
    # Class Variables
    # text used to generate the word cloud(Type:str)
    m_cloud_text = None
    # file path to text file containing words to not be included in the word cloud(Type:str)
    m_stopwords_file = None
    #  text in m_stopwords_file converted to a list(Type:list)
    m_stopwords_list = None

    # name of the image (e.g:"cloud2.png") in m_image_path, m_image_name can  be left as None (Type:str)
    m_image_name = None
    # file path to the image used to form a custom mask for the word cloud, m_image_path can  be left as None(Type:str)
    m_image_path = None
    # the image in m_image_path  with  m_image_name is converted to numpy array and stored here(Type: numpy array (image))
    m_custom_mask = None
    # the generated word cloud is stored as a numpy array of colors here(Type: numpy array (image))
    word_cloud_image_array = None
    # The word cloud object is constructed using the pre-defined parameters and stored here(Type: object)
    word_cloud = None
    # sets up the parameters for the word cloud in a dictionary(Type:dict)
    wordCloud_parameters = None
    # The time in seconds it takes to generate the word cloud(Type:str)
    word_cloud_generate_time = None
    # hue value is the color value for text in the word cloud and has a range of 0-360 (Type:int)
    hue = 45
    # (60, 120)You could change the lightness range to make the word cloud text brighter.(Type:int)
    # lightness_low and lightness_high are left unchanged through out the class
    lightness_low = 60
    lightness_high = 120

    def __init__(self, *args, **kwargs):
        """This method(constructor) is called immediately after the object has been created.
		The one special constraint on constructors is that no value may be returned"""
        # Variables can be overloaded from the constructor

        # these variables may require overloading
        # self.m_cloud_text = None
        self.m_cloud_text = " The text used to generate a word cloud "
        self.m_image_name = None
        # self.m_image_name = "cloud2.png"
        self.hue = 45
        # how wordCloud_parameters dict overloading is done
        # self.wordCloud_parameters['background_color'] = 'black'

        self.wordCloud_parameters = {
            "width": 1000,
            "height": 1000,
            "background_color": 'white',
            "max_words": 1500,
            "min_font_size": 4,
            "min_word_length": 0,
            "include_numbers": False,
            "repeat": False,  # slow
            "font_step": 1,
            "scale": 1,  # float
            "contour_width": 1,  # float
            "contour_color": "black"
        }
        # these variables may not require overloading
        self.m_stopwords_list = []
        self.m_stopwords_file = open(os.path.join("Binary Engine", "Text Files", "defaultStopwords.txt")).read().format()
        if self.m_image_name is not None:
            self.m_image_path = os.path.join("Binary Engine", "WordCloud Masks", self.m_image_name)
            self.m_custom_mask = np.array(PIL_Image.open(self.m_image_path))
        else:
            self.m_image_path = None
            self.m_custom_mask = None

    def set_stopwords(self):
        for words in self.m_stopwords_file.split():
            self.m_stopwords_list.append(words)

    def set_wordcloud(self):
        def my_color_func(random_state=None):
            # word_cloud color_func uses HSL stands for hue, saturation, lightness
            hue = int(360.0 * self.hue / 255.0)
            saturation = int(100.0 * 255.0 / 255.0)
            lightness = int(100.0 * float(random_state.randint(self.lightness_low, self.lightness_high)) / 255.0)
            return "HSL({}, {}%, {}%)".format(hue, saturation, lightness)

        _start_time = time.monotonic()
        self.word_cloud = WordCloud(mask=self.m_custom_mask,
                                    stopwords=self.m_stopwords_list,
                                    color_func=my_color_func,
                                    width=self.wordCloud_parameters["width"],
                                    height=self.wordCloud_parameters["height"],
                                    background_color=self.wordCloud_parameters["background_color"],
                                    max_words=self.wordCloud_parameters["max_words"],
                                    min_font_size=self.wordCloud_parameters["min_font_size"],
                                    min_word_length=self.wordCloud_parameters["min_word_length"],
                                    include_numbers=self.wordCloud_parameters["include_numbers"],
                                    font_step=self.wordCloud_parameters["font_step"],
                                    repeat=self.wordCloud_parameters["repeat"],
                                    scale=self.wordCloud_parameters["scale"],  # float
                                    contour_width=self.wordCloud_parameters["contour_width"],  # float
                                    contour_color=self.wordCloud_parameters["contour_color"]
                                    )
        """The self.word_cloud.generate method is the slowest method in the class because the word cloud image
			is generated using the pre-defined parameters here. avg time = 30 secs , worst time = 1min.
			#Generates a numpy array (image)
		"""
        self.word_cloud_image_array = self.word_cloud.generate(str(self.m_cloud_text))

        _end_time = time.monotonic() - _start_time

        self.word_cloud_generate_time = "Word Cloud generation took: {:.2f}s".format(_end_time)
