import numpy as np
import sounddevice as sd
from datetime import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import signal
import scipy.io.wavfile as waves
import scipy.fftpack as fourier
from time import *
import os

class Microfono:

    def __init__(self) -> bool:
        pass

    def grabar(self):
        fs=44100
        duration = 4  # seconds
        print("Grabando...")
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()
        print("Listo...")
        nombre_grabacion="rec"+datetime.today().strftime('%Y-%m-%d_%H:%M')+".wav"
        waves.write(nombre_grabacion,fs,myrecording)

        #return os.path.abspath(nombre_grabacion)
        return nombre_grabacion


class Audio():

    def __init__(self,ruta) -> None:
        self.frecuencia,self.datos=waves.read(ruta)
        #la frecuencia esta dado en un entero
        #los datos estan en un arreglo, dependiendo si es mono o estereo
        #vendra un arreglo,cada elemento es un vector 
        print("Frecuencia:",self.frecuencia,"Tam_Arreglo",len(self.datos)) #el tamalo de los datos es el shape[0]
        print(f"Numero de canales = {self.datos.shape[1]}") # si es estereo o mono
        self.length = self.datos.shape[0] / self.frecuencia,# cantidad de datos sobre la frecuencia, da el tiempo que dura la pista
        print(f"tamaño de audio = {self.length}s")

        self.izq=self.datos[:, 0]
        self.der=self.datos[:, 1]

    #se lee el audio y se muestra en una grafica
    def mostrarGrafica(self):

        self.time = np.linspace(0., self.length, self.datos.shape[0])
        plt.plot(self.time,self.izq, label="Left channel")
        plt.plot(self.time,self.der, label="Right channel")
        plt.legend()
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()

    def reproducir(self):
        fs=44100
        sd.play(self.datos,fs)
        sd.wait()
    
    def coordenadas(self):
        x = np.arange(0,len(self.der))/44100
        y = self.der
        return x,y

    def graficaFFT(self):
        y=np.abs(fourier.fft(self.der)) #magnitud 
        #x=self.der
        x=44100*np.arange(0,len(self.der))/len(self.der)

        index=np.where(y==np.max(y)) #se busca la frec mas alta
        frec_fund=x[index]

        


        return x,y,frec_fund

if __name__=='__main__':
    entrada=Microfono()
    dato=Audio(entrada.grabar())
    dato.mostrarGrafica()
    dato.reproducir()


