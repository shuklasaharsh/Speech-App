import kivy
kivy.require('2.0.0') # replace with your current kivy version !
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from playsound import playsound
import speech_recognition as sr
import pyttsx3
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import azure.cognitiveservices.speech as speechsdk
start=False
r=sr.Recognizer()
# m=sr.Microphone()
sm = ScreenManager()
e1=pyttsx3.init()
text=StringProperty()
import subprocess
import winsound
#TextInput height width
Builder.load_string("""
<MenuScreen>:
    GridLayout:
        cols:2
        rows:2
        Label:
            text: "TalkToMe"
            canvas.before:
                Color:
                    rgba:1.0,0.963,0.462,1
                    Rectangle:
                        pos:self.pos
                        size:self.size
                        font_size: 25
                        height: 200
                        width: 100
                        Image:
                            source:"./Back.png"
                            center_x:self.parent.center_x
                            center_y:self.parent.center_y
                            size_hint_x: None
                            size_hint_y: None
                            height: dp(800)
                            width: dp(400)
                            background_color:(255.0,255.0,255.0,0)
                            allow_stretch:True
            
    GridLayout:
        rows:4
        Button:
            text: 'Hear'
            on_press: root.manager.current = 'hear'
            background_normal: ''
            background_color: 0.33,0.019,0.019,1
            Image:
                source:"./speak.png"
                center_x:self.parent.center_x
                center_y:self.parent.center_y
                background_color:(0.33,0.019,0.019,1)
                allow_stretch:True
                Button:
                    text: 'Talk'
                    on_press: root.manager.current = 'talk'
                    background_normal: ''
                    background_color: 0.33,0.019,0.019,1
                    Image:
                        source:"./listen.png"
                        center_x:self.parent.center_x
                        center_y:self.parent.center_y
                        background_color:(0.33,0.019,0.019,1)
                        allow_stretch:True
                        Button:
                            text: 'Alarm'
                            on_press: app.alarm()
                            background_normal: ''
                            background_color: 0.33,0.019,0.019,1
                            Image:
                                source:"./alarm.png"
                                center_x:self.parent.center_x
                                center_y:self.parent.center_y
                                background_color:(0.33,0.019,0.019,1)
                                allow_stretch:True
                                Button:
                                    text:'Take notes'
                                    on_press:root.manager.current='notes'
                                    background_normal: ''
                                    background_color: 0.33,0.019,0.019,1
                                    Image:
                                        source:"./takenotes.png"
                                        center_x:self.parent.center_x
                                        center_y:self.parent.center_y
                                        background_color:(0.33,0.019,0.019,1)
                                        allow_stretch:True
                                    
<HearScreen>:
    BoxLayout:
        orientation:'vertical'
        BoxLayout:
            orientation:'horizontal'
            Button:
                text: 'Click here to talk'
                font:'Belgrano'
                font_size:25
                on_press: app.SpeechToText()
                background_normal: ''
                background_color: 0.33,0.019,0.019,1
            Image:
                source:"./clicktalk.png"
                size:self.parent.size
                stretch: True
                background_color:(0.33,0.019,0.019,1)
                allow_stretch:True
                Button:
                    text: 'Back to menu'
                    on_press: root.manager.current = 'menu'
                    background_normal: ''
                    background_color: 1.0,0.963,0.462,1
                    Image:
                        source:"./menu.png"
                        size: self.parent.size
                        stretch: True
                        background_color:(0.33,0.019,0.019,1)
                        allow_stretch:True
<TalkScreen>:
    BoxLayout:
        orientation:'vertical'
        BoxLayout:
            orientation:'horizontal'
            BoxLayout:
                TextInput:
                    id: txt1
                    multiline:True
                    text: 'Enter your Text here'
                    Button:
                        text:'Click here to Listen'
                        font:'Belgrano'
                        font_size:25
                        on_press: app.TextToSpeech(txt1.text)
                        background_normal: ''
                        background_color: 0.33,0.019,0.019,1
                        Image:
                            source:"./clicklisten.png"
                            size:self.parent.size
                            stretch: True
                            background_color:(0.33,0.019,0.019,1)
                            allow_stretch:True
    Button:
        text: 'Back to menu'
        on_press: root.manager.current = 'menu'
        background_normal: ''
        background_color: 1.0,0.963,0.462,1
        Image:
            source:"./menu.png"
            size: self.parent.size
            stretch: True
            background_color:(0.33,0.019,0.019,1)
            allow_stretch:True
<NotesScreen>:
    BoxLayout:
        orientation:'vertical'
        BoxLayout:
            orientation:'horizontal'
            Button:
                text:'Start Recording'
                on_press:app.StartRecording()
                Button:
                    text:'Stop Recording'
                    on_press:app.StopRecording()
    Button:
        text: 'Back to menu'
        on_press: root.manager.current = 'menu'
        background_normal: ''
        background_color: 1.0,0.963,0.462,1
        Image:
            source:"./menu.png"
            size: self.parent.size
            stretch: True
            background_color:(0.33,0.019,0.019,1)
            allow_stretch:True
""")

class MenuScreen(Screen):pass
class HearScreen(Screen):global text
class TalkScreen(Screen):pass
class NotesScreen(Screen):pass
# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(HearScreen(name='hear'))
sm.add_widget(TalkScreen(name='talk'))
sm.add_widget(NotesScreen(name='notes'))
class TalkToMeApp(App):
    start=False
    def build(self):
        return sm
    def SpeechToText(self):
        #MICROSOFT API
        speech_key,service_region="4f14c7d68c1b4637b45be4b9e5bda3d7","Westus"
        speech_config=speechsdk.SpeechConfig(subscription=speech_key,region=service_region)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
        result=speech_recognizer.recognize_once()
        if result.reason==speechsdk.ResultReason.RecognizedSpeech:
            text=result.text
        elif result.reason==speechsdk.ResultReason.NoMatch:
            text="No Speech"
        elif result.reason==speechsdk.ResultReason.Canceled:
            text="Cancelled"
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
        content=Button(text=text)
        p1=Popup(title="Result",content=content, auto_dismiss=False)
        content.bind(on_press=p1.dismiss)
        p1.open()
        '''#GOOGLE API
        global text
        self.text1=StringProperty()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            pop1=Popup(title="Say Something",content=Label(text="Say Something!"),size=(10,10))
            audio=r.listen(source,timeout=3, phrase_time_limit=3)
            try:
                text=r.recognize_google(audio)
            except sr.UnknownValueError:
                    text="Google Search Speech Recognition could not understand audio"
            except sr.RequestError as s:
                        text="Could not request results from google Speech Recogniton service"
            content=Button(text=text)
            p1=Popup(title="Result",content=content, auto_dismiss=False)
            content.bind(on_press=p1.dismiss)
            p1.open()
            #self.text1=text
            #text2=self.text1'''
        return
    def TextToSpeech(self,value):
        text=value
        '''tts = gTTS(text, lang='en')
        f=TemporaryFile()
        tts.write_to_fp(f)
        playsound(f)'''
        en_voice_id ="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ENUS_ZIRA_11.0"
        e1.setProperty('voice', en_voice_id)
        e1.setProperty('rate',150)
        e1.setProperty('volume', 0.9)
        e1.say(text)
        e1.runAndWait()
    def StartRecording(self):
        global start
        start=True
        Recording()
        '''r=sr.Recognizer()
        self.text1=StringProperty()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
        pop1=Popup(title="Say Something",content=Label(text="Say Something!"),size=(10,10))
        audio=r.listen(source,timeout=3, phrase_time_limit=3)
        try:
            text=r.recognize_google(audio)
            except sr.UnknownValueError:
                text="Google Search Speech Recognition could not understand audio"
            except sr.RequestError as s:
                    text="Could not request results from google Speech Recogniton service"
            content=Button(text=text)
            p1=Popup(title="Result",content=content, auto_dismiss=False)
            content.bind(on_press=p1.dismiss)
            p1.open()'''
    def StopRecording(self):
        global start
        start=False
        Recording()
    def alarm(self):
        winsound.Beep(100,5000)
def Recording():
    while(start):
        speech_key,service_region="4f14c7d68c1b4637b45be4b9e5bda3d7","Westus"
        speech_config=speechsdk.SpeechConfig(subscription=speech_key,region=service_region)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
        result=speech_recognizer.recognize_once()
        if result.reason==speechsdk.ResultReason.RecognizedSpeech:
            text=result.text
            text1="A"
        elif result.reason==speechsdk.ResultReason.NoMatch:
            text1="No Speech"
        elif result.reason==speechsdk.ResultReason.Canceled:
            text1="Cancelled"
        print("hi")
if __name__ == '__main__':
    TalkToMeApp().run()



                    


