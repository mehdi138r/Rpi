import random
import sys

import matplotlib
import folium
import io

from PyQt5.QtCore import Qt

matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QGridLayout, QWidget, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import cv2
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev



pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio2 = NRF24(GPIO, spidev.SpiDev())
radio2.begin(0, 17)

radio2.setRetries(15,15)

radio2.setPayloadSize(32)
radio2.setChannel(0x60)
radio2.setDataRate(NRF24.BR_2MBPS)
radio2.setPALevel(NRF24.PA_MIN)

radio2.setAutoAck(True)
radio2.enableDynamicPayloads()
radio2.enableAckPayload()

radio2.openWritingPipe(pipes[0])
radio2.openReadingPipe(1, pipes[1])

radio2.startListening()
radio2.stopListening()

radio2.startListening()

#c=1
#while True:
    #akpl_buf = [c,1, 2, 3,4,5,6,7,8,9,0,1, 2, 3,4,5,6,7,8]

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        # plt.rcParams['axes.facecolor'] = 'black'
        self.axes1 = fig.add_subplot(231)
        self.axes1.set_title("temp.")
        self.axes1.set_xlim([0, 100])
        self.axes1.grid(ls="--")

        self.axes2 = fig.add_subplot(232)
        self.axes2.set_title("Hum.")
        self.axes2.set_xlim([0, 100])
        self.axes2.grid(ls="--")

        self.axes3 = fig.add_subplot(233)
        self.axes3.set_title("Pressure.")
        self.axes3.set_xlim([0, 100])
        self.axes3.grid(ls="--")

        self.axes4 = fig.add_subplot(234, sharex=self.axes1)
        self.axes4.set_title("Accl_X.")
        # self.axes4.set_xlim([0, 100])
        self.axes4.grid(ls="--")

        self.axes5 = fig.add_subplot(235, sharex=self.axes2)
        self.axes5.set_title("Accl_Y.")
        # self.axes5.set_xlim([0, 100])
        self.axes5.grid(ls="--")

        self.axes6 = fig.add_subplot(236, sharex=self.axes3)
        self.axes6.set_title("Accl_Z.")
        # self.axes6.set_xlim([0, 100])
        self.axes6.grid(ls="--")

        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon('DATISSAT(1).png'))
        #self.image = QtGui.QImage()
        # self.image.loadFromData('DATISSAT.png')
        self.image_icon_label = QLabel()
        self.image_icon_label.setPixmap(QtGui.QPixmap('DATISSAT(1).png'))
        self.image_icon_label.resize(50, 50)
        # self.vid = cv2.VideoCapture(0)

        self.image = QLabel()

        self.setWindowTitle("Datis Sat")
        self.mainLayout = QGridLayout()
        self._coordinate = (36.35452817757624, 59.519327235623834)
        m = folium.Map(
            tiles='OpenStreetMap',
            zoom_start=13,
            location=self._coordinate
        )
        folium.Marker(self._coordinate, popup="current location").add_to(m)
        self._data = io.BytesIO()
        m.save(self._data, close_file=False)

        self._webView = QWebEngineView()
        self._webView.setHtml(self._data.getvalue().decode())
        self.canvas = MplCanvas(self, width=10, height=6, dpi=100)
        self.mainLayout.addWidget(self.canvas, 0, 0)
        self.mainLayout.addWidget(self.image_icon_label, 0, 1)
        self.mainLayout.addWidget(self._webView, 1, 0)
        self.mainLayout.addWidget(self.image, 1, 1)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        # self.vertical_layout = QVBoxLayout()
        # self.vertical_layout.addWidget(self.canvas)
        # self.empty = False
        #self.frame = []
        self.central_widget.setLayout(self.mainLayout)
        self.incode = ""

        # self.setLayout(self.mainLayout)
        # self.setStyleSheet("background-color: yellow;")

        n_data = 100
        self.xdata = np.array(range(n_data))
        self.ydata1 = [0 for i in range(n_data)]
        self.ydata2 = [0 for i in range(n_data)]
        self.ydata3 = [0 for i in range(n_data)]
        self.ydata4 = [0 for i in range(n_data)]
        self.ydata5 = [0 for i in range(n_data)]
        self.ydata6 = [0 for i in range(n_data)]
        self.update_plot()

        self.showMaximized()
        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        # self.timer2 = QtCore.QTimer()
        # self.timer2.setInterval(500)
        # self.timer2.timeout.connect(self.Print)
        # self.timer2.start()

    def Print(self):
        print("okay")

    def update_plot(self):
        # if self.vid.isOpened():
        #     empty, frame = self.vid.read()
        #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     h, w, ch = frame.shape
        #     bytes_per_line = ch * w
        #     convert_to_Qt_format = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        #     p = convert_to_Qt_format.scaled(450, 450, Qt.KeepAspectRatio)
        #     #img = cv2.resize(frame, (450, 450))
        # self.image.setPixmap(QtGui.QPixmap(p))
        self.canvas.axes6.cla()  # Clear the canvas.
        self.canvas.axes5.cla()  # Clear the canvas.
        self.canvas.axes4.cla()  # Clear the canvas.
        self.canvas.axes3.cla()  # Clear the canvas.
        self.canvas.axes2.cla()  # Clear the canvas.
        self.canvas.axes1.cla()  # Clear the canvas.

        # Drop off the first y element, append a new one.
        self.ydata1 = self.ydata1[1:] + [random.randint(3100, 3326) / 100]
        self.canvas.axes1.set_title("temp.")
        self.canvas.axes1.grid(ls="--")
        self.canvas.axes1.plot(self.xdata, self.ydata1, "r")

        self.ydata2 = self.ydata2[1:] + [random.randint(35, 42)]
        self.canvas.axes2.set_title("Hum.")
        self.canvas.axes2.grid(ls="--")
        self.canvas.axes2.plot(self.xdata, self.ydata2, "g")

        self.ydata3 = self.ydata3[1:] + [random.randint(100, 115)]
        self.canvas.axes3.set_title("Pressure.")
        self.canvas.axes3.grid(ls="--")
        self.canvas.axes3.plot(self.xdata, self.ydata3, "b")

        self.ydata4 = self.ydata4[1:] + [random.randint(996, 1020)]
        self.canvas.axes4.set_title("Accl_X.")
        self.canvas.axes4.grid(ls="--")
        self.canvas.axes4.plot(self.xdata, self.ydata4,"y")

        self.ydata5 = self.ydata4[1:] + [random.randint(996, 1020)]
        self.canvas.axes5.set_title("Accl_Y.")
        self.canvas.axes5.grid(ls="--")
        self.canvas.axes5.plot(self.xdata, self.ydata4, "m")

        self.ydata6 = self.ydata4[1:] + [random.randint(996, 1020)]
        self.canvas.axes6.set_title("Accl_Z.")
        self.canvas.axes6.grid(ls="--")
        self.canvas.axes6.plot(self.xdata, self.ydata4, "c")

        self.canvas.draw()
    def update_image(self):
        while not radio2.available([0]):
            time.sleep(10000 / 1000000.0)
        recv_buffer = []
        radio2.read(recv_buffer, radio2.getDynamicPayloadSize())
        if("done" not in "".join(chr(i) for i in recv_buffer) ):

            self.incode += "".join(chr(i) for i in recv_buffer)
        else:
            nparr = np.fromstring(self.incode, np.uint8)
            newFrame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            h, w, ch = newFrame.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QtGui.QImage(newFrame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(450, 450, Qt.KeepAspectRatio)
            # img = cv2.resize(frame, (450, 450))
            self.image.setPixmap(QtGui.QPixmap(p))



app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
