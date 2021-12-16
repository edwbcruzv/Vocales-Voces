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
        try:
            self.fig_Frecuencias.axes.clear()
            self.fig_Frecuencias.axes.set_xlabel('Frecuencia')
            self.fig_Frecuencias.axes.set_ylabel('Magnitud')
            self.fig_Frecuencias.axes.set_title('Secuencia 1')
            
            x1,y1,frec_fund=self.audio.graficaFFT()
            self.fig_Frecuencias.axes.plot(x1,y1) #datos para graficar
            self.fig_Frecuencias.draw()
            print("frecuencia fundamental=",str(frec_fund))

            # La frecuencia media de la voz masculina es de 106 Hz y con un rango de 77 Hz a 482 Hz.
            
            # En cuanto a la voz femenina su frecuencia es de 193 Hz, con un rango de 137 Hz a 634 Hz. 

        except Exception as e:
            print("error en la grafica,"+str(e))

##*****INICIO DE TODO EL PROGRAMA
if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    myapp=Ventana()
    myapp.show()
    sys.exit(app.exec_())