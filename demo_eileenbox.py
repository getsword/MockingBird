import sys
from PyQt5 import QtWidgets
from eileenbox.ui import Ui_Form
import pathlib
from gen_voice import generate_wav
import time
import random
import cn2an


class MyPyQT_Form(QtWidgets.QWidget,Ui_Form):
    def __init__(self):
        super(MyPyQT_Form,self).__init__()
        self.setupUi(self)

        self.encoder_model_path="encoder/saved_models/"
        self.synthesizer_model_path="synthesizer/saved_models/"
        self.vocoder_model_path="vocoder/saved_models/"

        # 读取预训练模型
        self.encoder_model_path=pathlib.WindowsPath(self.encoder_model_path)
        self.synthesizer_model_path=pathlib.WindowsPath(self.synthesizer_model_path)
        self.vocoder_model_path=pathlib.WindowsPath(self.vocoder_model_path)

        encoders=self.encoder_model_path.rglob('*.pt')
        synthesizers=self.synthesizer_model_path.rglob('*.pt')
        vocoders=self.vocoder_model_path.rglob('*.pt')

        encoders=[i for i in encoders]
        synthesizers=[i for i in synthesizers]
        vocoders=[i for i in vocoders]

        # 将读取到的预训练模型名称添加到下拉框中
        self.encoder_i2t={}
        self.synthesizer_i2t={}
        self.vocoder_i2t={}
        for idx,i in enumerate(encoders):
            self.encoder.addItem(i.name)
            self.encoder_i2t[idx]=i

        for idx,i in enumerate(synthesizers):
            self.synthesizer.addItem(i.name)
            self.synthesizer_i2t[idx]=i

        for idx,i in enumerate(vocoders):
            self.vocoder.addItem(i.name)
            self.vocoder_i2t[idx]=i

        self.encoder.setCurrentIndex(0)
        self.synthesizer.setCurrentIndex(0)
        self.vocoder.setCurrentIndex(0)

        self.encoder_loading(0)
        self.synthesizer_loading(0)
        self.vocoder_loading(0)

        self.encoder.currentIndexChanged.connect(self.encoder_loading)
        self.synthesizer.currentIndexChanged.connect(self.synthesizer_loading)
        self.vocoder.currentIndexChanged.connect(self.vocoder_loading)

        self.save.clicked.connect(self.save_utterance)


    def encoder_loading(self,i):
        current_encoder_path=self.encoder_i2t[i]
        print(current_encoder_path)
        self.current_encoder_path=current_encoder_path


    def synthesizer_loading(self,i):
        current_synthesizer_path=self.synthesizer_i2t[i]
        print(current_synthesizer_path)
        self.current_synthesizer_path=current_synthesizer_path



    def vocoder_loading(self,i):
        current_vocoder_path=self.vocoder_i2t[i]
        print(current_vocoder_path)
        self.current_vocoder_path=current_vocoder_path


    def save_utterance(self):
        generate_wav(self.current_encoder_path,self.current_synthesizer_path,self.current_vocoder_path,'dataset/',cn2an.transform(self.utterance.toPlainText(), "an2cn"),str(time.time())[:6]+str(random.randint(1,10000)))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())