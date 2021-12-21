##conexion con la interfaz grafica comando>   pyuic5 -x Interfaz_Voz.ui -o Interfaz_Voz.py
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import os
from Interfaz_Voz.Interfaz_Voz import Ui_Form
from LeeDato import *

class Ventana(QtWidgets.QWidget):


    def __init__(self,parent=None):
        super(Ventana,self).__init__(parent)
        self.ui=Ui_Form()
        self.ui.setupUi(self)

        # Microfono
        self.microfono=Microfono()
        
        # Audios
        self.audio1=None

        # Graficas
        self.fig_Frecuencias=FigureCanvas(Figure())
        self.fig_Audio=FigureCanvas(Figure())

        self.fig_Frecuencias.axes=self.fig_Frecuencias.figure.add_subplot(111)
        self.fig_Audio.axes=self.fig_Audio.figure.add_subplot(111)
        

        self.fig_Frecuencias.axes.clear()
        self.fig_Audio.axes.clear()
       

        self.fig_Frecuencias.axes.set_xlabel('eje X')
        self.fig_Frecuencias.axes.set_ylabel('eje Y')
        self.fig_Frecuencias.axes.set_title('Frecuencias')

        self.fig_Audio.axes.set_xlabel('eje X')
        self.fig_Audio.axes.set_ylabel('eje Y')
        self.fig_Audio.axes.set_title('Audio')


        self.ui.verticalLayout_Frecuencia.addWidget(self.fig_Frecuencias)
        self.ui.verticalLayout_Audio.addWidget(self.fig_Audio)
        

        self.fig_Frecuencias.draw()
        self.fig_Audio.draw()
        
        self.ui.pushButton_Audio.clicked.connect(self.capturarAudio)
        self.ui.pushButton_ReproducirAudio.clicked.connect(self.reproduceAudio)
        self.ui.pushButton_Evaluar.clicked.connect(self.evaluar)


    def capturarAudio(self):
        self.ui.label_RutaAudio.setText("Grabando...")

        ruta_audio=self.microfono.grabar() #se da por hecho que siempre se grabara un audio
        #self.ruta_audio1, selected_filter=QFileDialog.getOpenFileName(self,"seleccionar audio",self.cwd,"Text Files (*.wav)")
        self.ui.label_RutaAudio.setText(ruta_audio) #se mostrara la ruta del audio grabado
        #se procesara el audio intoducido para obtner la grafica y la secuencia
        try:
            # audio grabado
            self.fig_Audio.axes.clear()
            self.fig_Audio.axes.set_xlabel('Tiempo')
            self.fig_Audio.axes.set_ylabel('Amplitud')
            self.fig_Audio.axes.set_title('Secuencia 1')
            self.audio=Audio(ruta_audio)# ruta del audio
            
            x1,y1=self.audio.coordenadas()
            self.fig_Audio.axes.plot(x1,y1) #datos para graficar
            self.fig_Audio.draw()
        
        except Exception as e:
            self.audio=None
            self.ui.label_RutaAudio.setText("Error al grabar audio, "+str(e))

    def reproduceAudio(self):
        try:
            self.audio.reproducir()

        except Exception as e:
            print("no hay respuesta,"+str(e))

    def evaluar(self):

        self.fig_Frecuencias.axes.clear()
        self.fig_Frecuencias.axes.set_xlabel('Frecuencia')
        self.fig_Frecuencias.axes.set_ylabel('Magnitud')
        self.fig_Frecuencias.axes.set_title('Secuencia 1')
        
        x1,y1,frec_fund=self.audio.graficaFFT()#ademas se la grafica, regresa la frec fundamental


        self.fig_Frecuencias.axes.plot(x1,y1) #datos para graficar
        self.fig_Frecuencias.draw()
        print("frecuencia fundamental=",str(frec_fund))


        if self.ui.radioButton_Hombre.isChecked():
            self.hombre(frec_fund)
        elif self.ui.radioButton_Mujer.isChecked():
            self.mujer(frec_fund)
        else:
            self.ui.label_Status.setText("No se ha seleccionado ningun genero")

    def hombre(self,frec_fund):
        if(1000>=frec_fund[0] and frec_fund[0]>=750):
            print("A")
            self.ui.label_Status.setText("A")
        elif(750>frec_fund[0] and frec_fund[0]>=452):
            print("E")
            self.ui.label_Status.setText("E")
        elif(452>frec_fund[0] and frec_fund[0]>=362):
            print("O")
            self.ui.label_Status.setText("O")
        elif(362>frec_fund[0] and frec_fund[0]>=320):
            print("I")
            self.ui.label_Status.setText("I")    
        elif(298>frec_fund[0] and frec_fund[0]>=0):
            print("U")
            self.ui.label_Status.setText("U")
        else:
            self.ui.label_Status.setText("No es posible analizarlo")

    def mujer(self,frec_fund):
        pass

##*****INICIO DE TODO EL PROGRAMA
if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    myapp=Ventana()
    myapp.show()
    sys.exit(app.exec_())
