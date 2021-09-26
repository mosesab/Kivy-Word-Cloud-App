"""
 fileName : Main.py
 Author: Moses Bankole
 Github Username : mosesab
 Contact : thedevmosesb@gmail.com
 Run Main.py to view the GUI
 Use the requirements.txt file to install the required dependencies.
Code written with python 3.8.3
Tested on Windows

 """
import os
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty

from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.theming import ThemableBehavior

from kivymd.uix.list import OneLineIconListItem, TwoLineIconListItem, MDList
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.button import MDFlatButton

from kivymd.uix.dialog import MDDialog
from kivy.factory import Factory
from kivy.uix.popup import Popup

# import's the WordCloudGenerator class
from My_Word_Cloud import WordCloudGenerator

from kivy.garden.matplotlib.backend_kivy import FigureCanvas

# KV = open("nlp.kv.txt",encoding="utf-8").read()


class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class DrawerList(MDList):
    pass


class WordCloudList(TwoLineIconListItem):
    icon = StringProperty()

class SettingsList(TwoLineIconListItem):
    icon = StringProperty()


class WordCloudGeneratorExtended(WordCloudGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        # self.m_cloud_text = None
        # self.m_image_name = None
        self.m_image_name = "cloud2.png"
        self.hue = 236
        self.m_cloud_text = str(_text_)
    # how wordCloud_parameters dict overloading is done
    # self.wordCloud_parameters['background_color'] = 'black'


# def change_settings:


class Container(BoxLayout, Screen):
    box_display = ObjectProperty()

    def __init__(self, *args, **kwargs):
        global canvas
        super(Container, self).__init__(**kwargs)
        plt.clf()  # Clear the current figure
        plt.imshow(cloud.word_cloud_image_array, interpolation="bilinear")
        plt.axis("off")

        canvas = FigureCanvas(plt.gcf())
        self.box_display.add_widget(canvas)
        canvas.draw()

    def add_one(self, value):
        plt.clf()  # Clear the current figure
        plt.imshow(cloud.word_cloud_image_array, interpolation="bilinear")
        plt.axis("off")
        # plt.colorbar()
        canvas.draw()


class LoadDialog(BoxLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(BoxLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SetDrawerScreen(Screen, ThemableBehavior):
    """The kivy root class """
    screen_manager = ObjectProperty(None)
    nav_drawer = ObjectProperty(None)
    display_time = ObjectProperty(None)
    progress_bar = ObjectProperty(None)
    text_input = ObjectProperty(None)
    count = 0
    settings_count = 0
    dialog = None

    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)

    def set_screen_item(self, instance_item):
        '''called when a nav drawer item is clicked'''
        # handle screen changing
        self.screen_manager.current = instance_item.text
        self.nav_drawer.set_state("close")

    def open_another_screen(self):
        if (self.screen_manager.has_screen("another_screen")):
            self.screen_manager.current = "another_screen"
        else:
            self.dialog = MDDialog(
                title="First use Generate Word Cloud",
                text="You have to first generate the word cloud before you can view it.",
                type="custom",
                #buttons=[MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color), ],
                # size_hint=(.45, None),
                # auto_dismiss=True,
            )
            self.dialog.open()

    def set_wordCloud_settingsGUI(self):
        '''called when the Word Cloud Screen
		MDBottomNavigationItem for cloud settings is clicked,
		it draws the GUI for all the settings widgets on the screen,
		it should only be called once.
        '''
        self.count += 1
        if (self.count > 1):
            return
        wordCloud_icons_item = {
            "home": "Width",
            "altimeter": "Height",
            "face": "Background Color",
            "cookie": "Stop Words",
            "help-circle": "Maximum Words",
            "paw": "Repeat",
            "airbag": "Minimum Word Length",
            "airport": "Minimum Font Size",
            "alarm": "Include Numbers",
            "album": "Outline Width",
            "apple": "Outline Color",
            "file": "Custom Mask",
            "api": "Scale"
        }
        icons_item_secondary_text = {
            "home": "The width of the word cloud",
            "altimeter": "The height of the word cloud",
            "face": "Color of the word cloud ",
            "cookie": "Words to be omitted from the word cloud",
            "help-circle": "Maximum Words the word cloud can contain",
            "paw": " repeat the same words",
            "airbag": " 'be' = 2 , 'can' = 3 e.t.c.",
            "airport": "smaller font size for less readable words ",
            "alarm": " Do you hate your 123s",
            "album": " The outline is the shape of the cloud",
            "apple": " I like black more",
            "file": " Mask the cloud to form other shapes",
            "api": "Larger scales for bigger screeens "
        }
        for list_item in wordCloud_icons_item.keys():
            self.ids.wordCloud_md_list.add_widget(
                WordCloudList(icon=list_item,
                              text=wordCloud_icons_item[list_item],
                              secondary_text=icons_item_secondary_text[list_item]
                              )
            )

    def set_wordCloud_settings(self, options_item):
        list_options_item = [
            "Width",
            "Height",
            "Background Color",
            "Stop Words",
            "Maximum Words",
            "Repeat",
            "Minimum Word Length",
            "Minimum Font Size",
            "Include Numbers",
            "Outline Width",
            "Outline Color",
            "Custom Mask",
            "Scale"
        ]
        for item in list_options_item:
            if options_item.text == item:
                print(item, " found !!!")
        self.dialog = MDDialog(
            title=options_item.text,
            text="You clicked me",
            type="custom",
            #buttons=[MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color), ],
            # size_hint=(.45, None),
            # auto_dismiss=True,
        )
        self.dialog.open()
        print("called by ", options_item.text)

    def set_settingsGUI(self):
        """ called when the settings tab in navigation drawer is clicked."""
        self.settings_count += 1
        if (self.settings_count > 1):
            return
        settings_icons_item = {
            "brush": "Theme",
            "exit-to-app": "Exit App"
        }
        settings_icons_item_secondary_text = {
            "brush": "If you could say it all in words, there would be no reason to paint",
            "exit-to-app": "It is so hard to leave, until you leave "
        }
        for list_item in settings_icons_item.keys():
            self.ids.settings_md_list.add_widget(
                SettingsList(icon=list_item,
                             text=settings_icons_item[list_item],
                             secondary_text=settings_icons_item_secondary_text[list_item]
                             )
            )


    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        try:
            with open(os.path.join(path, filename[0])) as stream:
                self.text_input.text = stream.read()
            self.dismiss_popup()
        except:
            self.dialog = MDDialog(
                title="Something Went Wrong",
                text="An error occurred try again with a different file",
                type="custom",
                #buttons=[MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color), ],
                # size_hint=(.45, None),
                # auto_dismiss=True,
            )
            self.dialog.open()

    def save(self, path, filename):
        try:
            with open(os.path.join(path, filename), 'w') as stream:
                stream.write(self.text_input.text)
            self.dismiss_popup()
        except:
            self.dialog = MDDialog(
                title="FATAL ERROR !!!",
                text="The Operation completed successfully :) ",
                type="custom",
                #buttons=[MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color), ],
                # size_hint=(.45, None),
                # auto_dismiss=True,
            )
            self.dialog.open()


class MyApp(MDApp):
    about_text = str(open(os.path.join("Binary Engine", "Text Files", "about.txt")).read()).format()
    help_text = str(open(os.path.join("Binary Engine", "Text Files", "help.txt")).read()).format()
    myStopwords_text = str(open(os.path.join("Binary Engine", "Text Files", "editedStopwords.txt")).read())
    main_screen = None

    def build(self):
        return Builder.load_file('design.kv')  # ,WordCloudResultScreen()

    def on_start(self):
        self.fps_monitor_start()

        icons_item = {
            "home": "Home",
            # making Word Cloud the default screen sometimes causes a weak refrence error
            "altimeter": "Word Cloud",
            "stop": "Stop Words",
            "heart-settings": "Settings",
            "paw": "About"

        }
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )

        # self.root.screen_manager.current = "Word Cloud"

        # Activates the dark theme
        self.title = "Word Cloud Generator"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.accent_palette = "BlueGray"
        self.theme_cls.primary_palette = "Purple"

    def set_settings(self, settings_item):
        list_settings_item = ["Theme", "Exit App"]
        for item in list_settings_item:
            if settings_item.text == "Theme":
                self.show_theme_picker()
            if settings_item.text == "Exit App":
                self.stop()

    def show_theme_picker(self):
        '''called when theme button item is clicked in settings'''
        # handle theme changing
        picker = MDThemePicker()
        picker.open()

    def progressBar_state(self, instance, value):
        {
            "start": self.root.ids.progress_bar.start,
            "stop": self.root.ids.progress_bar.stop,
        }.get(value)()

    def saveStopwords(self):
        with open(os.path.join("Binary Engine", "Text Files", "editedStopwords.txt"), 'w', encoding='utf-8') as f:
            f.write(self.root.ids.stopwords_input.text)
            f.close()
        self.root.ids.stopwords_md_label.text = self.root.ids.stopwords_input.text

        self.myStopwords_text = str(open(os.path.join("Binary Engine", "Text Files", "editedStopwords.txt")).read())

    def resetStopWordsToDefault(self):
        with open(os.path.join("Binary Engine", "Text Files", "editedStopwords.txt"), 'w', encoding='utf-8') as f:
            f.write(str(open(os.path.join("Binary Engine", "Text Files", "defaultStopwords.txt")).read()))
            f.close
        self.myStopwords_text = str(open(os.path.join("Binary Engine", "Text Files", "editedStopwords.txt")).read())

        self.root.ids.stopwords_md_label.text = self.myStopwords_text
        self.root.ids.stopwords_input.text = self.myStopwords_text

    def clearStopWords(self):
        with open(os.path.join("Binary Engine", "Text Files", "editedStopwords.txt"), 'w', encoding='utf-8') as f:
            f.write("")
            f.close()
        self.root.ids.stopwords_md_label.text = ""
        self.root.ids.stopwords_input.text = ""

    def generate_word_cloud(self):
        self.progressBar_state = "start"

        global _text_
        _text_ = self.root.ids.text_input.text
        self.root.ids.text_input.text = " "

        global cloud
        cloud = WordCloudGeneratorExtended()
        cloud.set_stopwords()

        if (self.text_input_errorChecker(_text_) is False):
            cloud.set_wordcloud()
        else:
            return

        if (self.root.screen_manager.has_screen("another_screen")):
            self.main_screen.add_one
            self.root.screen_manager.current = "another_screen"
        else:
            self.main_screen = Container(name="another_screen")
            self.root.screen_manager.add_widget(self.main_screen)

            print("Completed the large Word Cloud generation")

        self.root.display_time.text = cloud.word_cloud_generate_time

        self.progressBar_state = "stop"

    #

    def text_input_errorChecker(self, text_input):
        # if there is error return True else return False
        # start checking if text input is None
        if (len(text_input) < 1):
            self.dialog = MDDialog(
                title="Input Text Field is Empty",
                text="Input Text Field should contain at least one word that isn't a stopword.",
                type="custom",
                #buttons=[MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color), ],
                # size_hint=(.45, None),
                # auto_dismiss=True,
            )
            self.dialog.open()
            return True
        # start  checking  if every word in text input is a stop word
        # for every word in text input if a word in text input isn't' in the stop word list
        conditional = 0
        for word in text_input.split():
            if word not in cloud.m_stopwords_list:
                conditional = 45
                break
        # after checking all the text if conditional is still 0
        if conditional == 0:
            self.dialog = MDDialog(
                title="Input Text Field is Empty",
                text="Input Text Field should contain at least one word that isn't a stopword.",
                type="custom",
                #buttons=[MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color), ],
                # size_hint=(.45, None),
                # auto_dismiss=True,
            )
            self.dialog.open()
            return True
        # start checking if text input is only numbers and include_numbers is false
        if text_input.isdigit() and cloud.wordCloud_parameters["include_numbers"] is False:
            self.dialog = MDDialog(
                title="Input Text Field Include Numbers is False",
                text="Input Text Field contains only numbers and Include Numbers option is False .",
                type="custom",
                #buttons=[MDFlatButton(text="CANCEL", text_color=self.theme_cls.primary_color), ],
            )
            self.dialog.open()
            return True


if __name__ == "__main__" :
    MyApp().run()