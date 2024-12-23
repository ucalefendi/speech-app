from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QVBoxLayout,QTextEdit,QFileDialog
from PyQt5.QtCore import Qt
import speech_recognition as sr
from textblob import TextBlob
from PyQt5.QtGui import QFont



class Speech(QWidget):
    def __init__(self):
        super().__init__()
        self.recognize_text = ""
        self.settings()
        self.initUI()
        self.connects()


    def initUI(self):
        title = QLabel("Guest Speaker")
        title.setFont(QFont("Myanmar MN",35))


        self.output_box = QTextEdit()
        self.sentiment_text = QLabel("Sentiment:")

        self.submit = QPushButton("Speak Now")
        self.save = QPushButton("Save Note")

        master = QVBoxLayout()
        master.addWidget(title,alignment=Qt.AlignCenter)
        master.addWidget(self.output_box,alignment=Qt.AlignCenter)
        master.addWidget(self.sentiment_text,alignment=Qt.AlignCenter)
        master.addWidget(self.submit,alignment=Qt.AlignCenter)
        master.addWidget(self.save,alignment=Qt.AlignCenter)
        self.setLayout(master)


        self.sentiment_text.setObjectName("sentimentlabel")


    def settings(self):
        self.setWindowTitle("Guest Speaker")
        self.setGeometry(250,250,300,500)


    def connects(self):
        self.submit.clicked.connect(self.button_clicked)
        self.save.clicked.connect(self.save_clicked)


    def get_speech(self):
        listener = sr.Recognizer()  
        text = ""
        with sr.Microphone() as source:
            try:
                audio =listener.listen(source,timeout=2)
                text = listener.recognize_google(audio)
                print(text)
            except sr.UnknownValueError:
                print("cannot understand audio")  
            except sr.RequestError as e:
                print(f"Cannot request results from Google: {e}") 
            except Exception as e:
                print(f"error : {e}")  

        self.recognize_text = text  
        return text             


    def get_sentiment(self,text):
        if text:
            try:
                res = TextBlob(text)
            except Exception as e:
                print(f"Error: {e}") 

            if res.sentiment.polarity > 0.3:    
                return "positive"

            elif res.sentiment.polarity < -0.3:
                return "negative"       
            
            else:
                return 'Neutral'
        

        return None    



    def button_clicked(self):
        res = self.get_speech()
        sentiment = self.get_sentiment(res)
        if res and sentiment is not None:
            self.output_box.setPlainText(res)
            self.sentiment_text.setText("Sentimen:" + str(sentiment))



    def save_clicked(self):
        content = self.output_box.toPlainText()
        file_path , _ = QFileDialog.getSaveFileName(self, 'Save Note', '', 'Text Files (*.txt);;All Files (*)')

        if file_path:
            with open(file_path,"w") as file:
                file.write(content)



if __name__ in '__main__':
    app = QApplication([]) 
    main = Speech()
    main.show()
    app.exec_()   