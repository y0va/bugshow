#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
A Data Show about sound gathered from grain weevils
combined with some Audiomonitoring capabilities for use on an raspi with dsiplay.
copy left by yova@student.uni-kassel.de with many thanks to: 
SWHarden: http://www.swharden.com/wp/2016-07-31-real-time-audio-monitor-with-pyqt/
and
boylea: https://gist.github.com/boylea

"""


from PyQt4 import QtGui,QtCore

import sys
import ui_main
import numpy as np
import pyqtgraph as pg
import time
import datetime
import signal
import alsaaudio
import datetime
import csv
import subprocess

from threading import Thread
from scipy.signal import welch
from random import randint

"""todo: implement another getfft class in SWHear.py -> np.rfft"""

FS = 8000 #Samplerate should be somehow compatible with alsaaudio
CHUNKSZ = 2**9 #FFT over how many samples? Should be smaller than FS/2
FCUT=200 #  From which Frequency on should we take fft values into account?
OVERLAP=1.01 # Overlap for mean FFT see update_fft()
SHOW_LENGTH=11
SHOW_L_CUTOFF=0
SHOW_H_CUTOFF=1500
SHOW_FREQS=3499
AUDIO_DEVICE='default'
#AUDIO_DEVICE='plug:front:1'

BASE_DIR='/home/yova/coding/bugshow/'
#For raspi: /home/pi/audiomon


DISPLAY_SPECTOGRAM=False
DISPLAY_GRFFT=False
DISPLAY_GRPCM=False
DISPLAY_SHOW=True
DISPLAY_TSIGNAL=False


SHOW_RFREQS=SHOW_FREQS-SHOW_H_CUTOFF-SHOW_L_CUTOFF + 1


def stop_all(a,b) :
    print ( "ciao, perhaps we have to wait for the fft to terminate...")
    quit()


signal.signal(signal.SIGINT, stop_all)



class MicrophoneRecorder():
    def __init__(self,signal):
        self.chunk_size=CHUNKSZ
        self.rate=FS
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, AUDIO_DEVICE)

        #set attributes: Mono
        self.inp.setchannels(1)
        self.inp.setrate(self.rate)
        self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.inp.setperiodsize(1024)

        self.data_buffer=np.ndarray(shape=(1,1),dtype='int16')
        self.wdata=np.ndarray(shape=(1,1),dtype='int16')
        self.fft=np.ndarray
        self.psd_mean=np.array([])
        self.win=np.hanning(self.chunk_size)

        self.datax=np.arange(self.chunk_size)/float(self.rate)

        self.stopping_time=datetime.datetime.now() + datetime.timedelta(minutes=.1)
        self.wfft_signal = signal


    def calc_fft(self):
        self.fft=np.fft.rfft(self.data*self.win) /  self.chunk_size


    def calc_wfft(self, wdata):   ##### experimental!!
        b=[(ele/2**8.)*2-1 for ele in wdata]

        nperseg = 256

        #estimate power spectrum density
        f,wfft = welch(b, nperseg = nperseg, nfft=self.rate/100, axis=0)

        self.wfft_signal.emit(wfft)


    def record(self):

        while self.data_buffer.shape[0] < self.chunk_size:
            # Read data from device
            try:
                self.data_buffer=np.append(self.data_buffer,np.fromstring(self.inp.read()[1],'int16'))
            except Exception as E:
                print(" -- exception {}! terminating...").format(E)

        self.data = self.data_buffer[:self.chunk_size]
        self.data_buffer = self.data_buffer[self.chunk_size:]
   
        t = Thread(target=self.calc_fft)
        t.daemon = True
        t.start()
        self.new_record_thread()


    def new_record_thread(self):
        t = Thread(target=self.record)
        t.daemon = True
        t.start()
   


class MonPi(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    calculated_wfft = QtCore.pyqtSignal(np.ndarray)
    
            
    def __init__(self, parent=None):

        pg.setConfigOption('background', 'w') #before loading widget
        super(MonPi, self).__init__(parent)
        self.calculated_wfft.connect(self.update_wfft)
        
                
        if not hasattr(self, 'ear') : 
            self.ear = MicrophoneRecorder(self.calculated_wfft)
            self.ear.record()
        
        self.chunk_size=CHUNKSZ 

        self.setupUi(self)
        
   
        
        
        if not DISPLAY_TSIGNAL : self.pbLevel.hide()
        self.img_kk.hide()
        self.logo_it.hide()
        self.nextView.clicked.connect(self.handleNextView)
        
        # calculate points to cut off from fft for noise
        self.fft_cut=FCUT/(FS/CHUNKSZ)
        
        if DISPLAY_SPECTOGRAM : self.setup_spectogram()
            
        if DISPLAY_GRPCM: self.setup_grpcm()
        
        if DISPLAY_GRFFT: self.setup_grfft()
        
        #show
        self.data_kk = np.ndarray([200,SHOW_FREQS])
        self.data_gk = np.ndarray([200,SHOW_FREQS])
        self.sum_data_gk = np.zeros(shape=[SHOW_FREQS,])
        self.sum_data_kk = np.zeros(shape=[SHOW_FREQS,])
        self.number_tc=0
        self.timedelta=datetime.timedelta(seconds=SHOW_LENGTH)
        
       
        if DISPLAY_SHOW: self.setup_show()
        
        self.fftMax=0
        self.maxPCM=0
        self.pcmpen=pg.mkPen(color='b')
        self.lastTime = pg.ptime.time()
        self.fps=0
        self.a=0
        self.b=0
        self.c=0
        
        # Beat detection
        self.average_mag=0
        self.beat_min=0
        
        
    def setup_spectogram(self):
        #setup spectogramm
        
        if not DISPLAY_TSIGNAL : self.pbLevel.hide()
        self.label_top.setText('Spectogram')
        self.grFFT_long.img = pg.ImageItem()
        self.grFFT_long.addItem(self.grFFT_long.img)
        
        self.img_array = np.zeros((600, int(self.chunk_size/2+1)-self.fft_cut))
                # bipolar colormap
        pos = np.array([0., 1., 0.5, 0.25, 0.75])
        color = np.array([[0,255,255,255], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
        cmap = pg.ColorMap(pos, color)
        lut = cmap.getLookupTable(0.0, 1.0, 256)
                # set colormap
        self.grFFT_long.img.setLookupTable(lut)
        self.grFFT_long.img.setLevels([-50,40])
        
                # setup the correct scaling for y-axis  
                
        freq = np.arange((self.chunk_size/2)+1)/(float(self.chunk_size)/FS)
        yscale = 1.0/(self.img_array.shape[1]/freq[-1])
        
        self.grFFT_long.img.scale((1./FS)*self.chunk_size, yscale)
        self.grFFT_long.setLabel('left', 'Frequency', units='Hz')
        
        self.grFFT_long.win = np.hanning(self.chunk_size)
        

    def setup_grpcm(self):
        self.label_top.setText('Raw Data PCM')
        self.grFFT_long.plotItem.showGrid(True, True, 0.7)
        

    def setup_grfft(self):
        if not DISPLAY_TSIGNAL : self.pbLevel.hide()
        self.label_top.setText('Mean FFT. Overlapfactor: '+ str(OVERLAP))
        
        self.grFFT_long.plotItem.showGrid(True, True, 0.7)
        self.grFFT_long.plotItem.setLabel('bottom', 'Frequency', units='Hz')
        self.grFFT_long.plotItem.getAxis('bottom').setTicks([[(0,FCUT),(CHUNKSZ/8-self.fft_cut,(CHUNKSZ/8)*FS/CHUNKSZ),(CHUNKSZ/4-self.fft_cut,(CHUNKSZ/4)*FS/CHUNKSZ),(3*CHUNKSZ/8-self.fft_cut,(3*CHUNKSZ/8)*FS/CHUNKSZ)]])
        

    def setup_show(self):
        
        self.bl_display_gk=True
        self.bl_display_kk=False
        self.bl_display_both=False
        self.nr_dataset=0.
        
        
        data_kk = np.ndarray([200,SHOW_FREQS])
        data_gk = np.ndarray([200,SHOW_FREQS])
        
        self.pbLevel.hide()
        self.grFFT_long.plotItem.showGrid(True, True, 0.7)
        self.grFFT_long.plotItem.setLabel('bottom', 'Frequency (Hz)')
        
        #self.grFFT_long.plotItem.getAxis('bottom').setTicks([[(0,SHOW_L_CUTOFF),(SHOW_RFREQS/4,(SHOW_RFREQS/4+SHOW_L_CUTOFF)),(SHOW_RFREQS/2,SHOW_RFREQS/2+SHOW_L_CUTOFF),(3*SHOW_RFREQS/4,3*SHOW_RFREQS/4+SHOW_L_CUTOFF)]])
        self.grFFT_long.plotItem.getAxis('bottom').setTicks([[(0,SHOW_L_CUTOFF),(500-SHOW_L_CUTOFF,500),(1000-SHOW_L_CUTOFF,1000),(1500-SHOW_L_CUTOFF,1500)]])
        
        
        
        
        if self.number_tc > 190: # We already did that
            self.img_gk.hide()
            self.img_kk.hide()
            return
            
            
        # LOAD DATA
        
        with open(BASE_DIR + 'kornkaefer.csv', 'rb') as f:
            max_kk=0
            reader = csv.reader(f,delimiter=';')
            
            for row in reader:
                row2=map(lambda x: str.replace(x, ',','.'), row)
                self.data_kk[self.number_tc]=map(float,row2)
                self.number_tc+=1
         
        self.number_tc=0
        with open(BASE_DIR + 'Getreidekapuziner.csv', 'rb') as f:
            reader = csv.reader(f,delimiter=';')
            
            for row in reader:
                row2=map(lambda x: str.replace(x, ',','.'), row)
                self.data_gk[self.number_tc]=map(float,row2)
                self.number_tc+=1
        
        self.start_time=datetime.datetime.now()
      
    
    def handleNextView(self):
        global DISPLAY_SPECTOGRAM
        global DISPLAY_GRFFT
        global DISPLAY_GRPCM
        global DISPLAY_SHOW
            
        print ("PUNCH!")
        
        self.setupUi(self)
        self.nextView.clicked.connect(self.handleNextView)
        
        
        if DISPLAY_SPECTOGRAM : 
            # Now display Mean fft graph
            DISPLAY_SPECTOGRAM = False
            DISPLAY_GRFFT=True
            
            self.frame_4.hide()
            self.setup_grfft()
            return
                       
        if DISPLAY_GRFFT :
            # now display Show or RAW PCM graph
            DISPLAY_GRFFT = False
            
            if not DISPLAY_TSIGNAL : 
                DISPLAY_SHOW = True
                
                self.setup_show()
            else :
                DISPLAY_GRPCM = True
                self.setup_grpcm()
            return
            
        if DISPLAY_GRPCM :
            # Now display Show
            DISPLAY_GRPCM = False
            DISPLAY_SHOW = True
            
            
            
            self.setup_show()
            return
           
        if DISPLAY_SHOW:
            # Display Spectogram again
            DISPLAY_SHOW = False
            DISPLAY_SPECTOGRAM = True
            self.frame_4.hide()
            self.setup_spectogram()
            return
           
            
    def update_spectogram(self,psd):
                
        # convert to dB scale
        psd = 20 * np.log10(psd)

        # roll down one and replace leading edge with new data
        self.img_array = np.roll(self.img_array, -1, 0)

        self.img_array[-1:] = psd
        #print (self.img_array.shape)
        self.grFFT_long.img.setImage(self.img_array, autoLevels=False)
        

    def update_fft(self,psd):
        ### MEAN FFT
        
        #get mean of fft
        if (self.ear.psd_mean.size == 0) : self.ear.psd_mean=psd
        else : self.ear.psd_mean=(psd + self.ear.psd_mean/OVERLAP)
        
        afft=self.ear.psd_mean
        
        fftMax=np.max(afft)
                
        if self.fftMax < fftMax : 
            self.grFFT_long.plotItem.setRange(yRange=[0,fftMax],xRange=[0,afft.shape[0]])
            self.fftMax=fftMax
        
        if self.a<245:
            self.a+=10
        else:
            self.grFFT_long.plotItem.clear()
            self.fftMax=0
            self.a=0
            self.b+=10
        if self.b > 255:
            self.c+=10
            self.b=0
        if self.c > 255:
            self.c=0
          
        pen=pg.mkPen(color=(self.a,self.b,self.c), width=3)
        


        # BEAT DETECTION     WIP
        
        BHERTZ=20
        THERTZ=120
        
        # substract it from the noise
        bfft_cut_top = THERTZ/(FS/CHUNKSZ) - self.fft_cut
        bfft_cut_bottom = BHERTZ/(FS/CHUNKSZ) - self.fft_cut
        area=psd[bfft_cut_bottom:bfft_cut_top]
        bass=np.mean(area)
        
        if bass >  self.average_mag + 25: 
            self.grFFT_long.plot(afft,pen=pg.mkPen('y', width=3, style=QtCore.Qt.DashLine) ,clear=True,autoLevels=False)
            print ("BEAT! @ " + str(np.max(area)))
            #self.grFFT_long.getViewBox().setBackgroundColor('black')
        else : self.grFFT_long.plot(afft,pen=pen,clear=True,autoLevels=False)
            #self.grFFT_long.getViewBox().setBackgroundColor('white')

        
        self.average_mag = (self.average_mag+bass)/2
        

    def update_levelmeter(self,pcmMax):
        self.pbLevel.setValue(1000*pcmMax/self.maxPCM)
        

    def update_pcm(self):
        self.grFFT_long.plot(self.ear.datax,self.ear.data,pen=self.pcmpen,clear=True)


    def update_wfft(self,wfft): # defunct
        print (wfft)
        pen=pg.mkPen(color='b')
        self.grFFT_long.plot( range(0,221),abs(wfft), pen=pen,clear=True)


    def display_kk(self):
        self.sum_data_kk = self.sum_data_kk + self.data_kk[int(self.nr_dataset)]
        mean_data_kk = self.sum_data_kk / self.nr_dataset
        
        self.maximum=max(mean_data_kk[SHOW_L_CUTOFF:-SHOW_H_CUTOFF])
        
        display_data_kk =  map (lambda x: x/self.maximum, mean_data_kk) 
        
        self.grFFT_long.plot(display_data_kk[SHOW_L_CUTOFF:-SHOW_H_CUTOFF],pen=pg.mkPen('b', width=3, style=QtCore.Qt.DashLine), clear=False)
        

    def display_gk(self):
        self.sum_data_gk = self.sum_data_gk + self.data_gk[int(self.nr_dataset)]
        mean_data_gk = [x/self.nr_dataset for x in self.sum_data_gk]
        
        self.maximum=max(self.maximum,max(mean_data_gk[SHOW_L_CUTOFF:-SHOW_H_CUTOFF]))
        
        display_data_gk =  map (lambda x: x/self.maximum, mean_data_gk)
        
        self.grFFT_long.plot(display_data_gk[SHOW_L_CUTOFF:-SHOW_H_CUTOFF],pen=pg.mkPen('g', width=3, style=QtCore.Qt.DashLine), clear=False)
        
        
    def update_show(self):
        self.maximum=0.
        
        self.grFFT_long.clear()
        
        # SHOW PROGRAM
        
        # 10 sec show & play KK
        # 10 sec show & play GK
        # 10 sec show & play both
        
        
        if datetime.datetime.now() > self.start_time + self.timedelta :
            if self.bl_display_gk:
                # NOW KK
                self.bl_display_gk = False
                self.bl_display_kk = True
                self.img_gk.hide()
                self.logo_it.hide()
                self.img_kk.show()
                
                subprocess.Popen(['/usr/bin/aplay','-D',AUDIO_DEVICE,BASE_DIR + 'wav/kk.wav'])

            elif self.bl_display_kk:
                # NOW BOTH
                self.bl_display_kk = False
                self.bl_display_both = True
                self.img_gk.hide()
                self.img_kk.hide()
                self.logo_it.show()
                
            elif self.bl_display_both:
                # NOW GK
                self.bl_display_both = False
                self.bl_display_gk = True
                self.img_gk.show()
                self.img_kk.hide()
                self.logo_it.hide()
                
                subprocess.Popen(['/usr/bin/aplay','-D',AUDIO_DEVICE,BASE_DIR + 'wav/gk.wav'])
            
            self.start_time = datetime.datetime.now()
                
        if self.bl_display_gk :
            self.label_top.setText('Aufnahmenr: '+ str(self.nr_dataset)+' Getreidekapuziner.')
            self.display_gk()
        elif self.bl_display_kk:
            self.label_top.setText("Aufnahmenr: "+ str(self.nr_dataset)+u" Kornkäfer." )
            self.display_kk()
        elif self.bl_display_both:
            self.label_top.setText('Aufnahmenr: '+ str(self.nr_dataset)+u" Getreidekapuziner (blau) & Kornkäfer (grün)")
            self.display_gk()
            self.display_kk()
        
        self.nr_dataset+=1.
        if self.nr_dataset==195 : 
            self.nr_dataset=1.
            self.sum_data_kk=np.zeros(shape=[SHOW_FREQS,])
            self.sum_data_gk=np.zeros(shape=[SHOW_FREQS,])
        
        
    def update(self):
        if not self.ear.data is None and not self.ear.fft is None:
            
            #FREQUENCE SIGNAL
            if DISPLAY_GRFFT or DISPLAY_SPECTOGRAM :
                # get magnitude
                psd = np.abs(self.ear.fft)

                # cutoff low noise
                psd=psd[self.fft_cut:]
            
            if DISPLAY_GRFFT : self.update_fft(psd)
            if DISPLAY_SPECTOGRAM : self.update_spectogram(psd)
 
            # TIME SIGNAL
            if DISPLAY_TSIGNAL:
                pcmMax=np.max(np.abs(self.ear.data))

                if pcmMax>self.maxPCM:
                    self.maxPCM=pcmMax
                    if DISPLAY_GRPCM : self.grFFT_long.plotItem.setRange(yRange=[-pcmMax,pcmMax])

                self.update_levelmeter(pcmMax)
                if DISPLAY_GRPCM : self.update_pcm()
            
            #   SHOW
            if DISPLAY_SHOW : 
                self.update_show()
                
            #Display fps
            now = pg.ptime.time()
            dt = now - self.lastTime
            self.lastTime = now

            if self.fps is None:
                self.fps = 1.0/dt
            else:
                s = np.clip(dt*3., 0, 1)
                self.fps = self.fps * (1-s) + (1.0/dt) * s

            fps_text="FPS: {:.2F}".format(self.fps)
            self.label_fps.setText(fps_text)

        QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat


if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = MonPi()
    #form.show()
    form.showFullScreen()
    form.update()

    app.exec_()
    print("DONE")
