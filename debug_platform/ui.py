import sys

from connection_manager import client_connection_manager
from remote_control import remote_control
#from PyQt6.QtCore import *
#from PyQt6.QtGui import *
#from PyQt6.QtWidgets import *

from PyQt6 import QtCore, QtGui, QtWidgets

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QKeyEvent


keyboard_keys = ["w", "a", "s", "d"]

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)



        self.conn_mann = client_connection_manager()
        self.conn_mann.connect_callback_assign(self.connection_state_ui)
        self.conn_mann.recieved_packet_callback_assign(self.recieved_state_ui)



        self.connect_button.clicked.connect(self.connect_button_handler)
        self.rov_img.setPixmap(QtGui.QPixmap("rover.png"))

        self.rem_conn = remote_control()
        self.comboBox.addItem("k")
        self.comboBox.currentIndexChanged.connect(self.control_dev_change)
        self.rem_conn.register_controller_connected_callback(self.controller_connected_handler)
        self.rem_conn.register_controller_disconnected_callback(self.controller_disconnected_handler)

        self.rem_conn.register_motor_data_ready_callback(self.send_motor_data)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(802, 444)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 181, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.connection_status_label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connection_status_label.sizePolicy().hasHeightForWidth())
        self.connection_status_label.setSizePolicy(sizePolicy)
        self.connection_status_label.setObjectName("connection_status_label")
        self.verticalLayout.addWidget(self.connection_status_label)
        self.age_lebel = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.age_lebel.setObjectName("age_lebel")
        self.verticalLayout.addWidget(self.age_lebel)
        self.mag_label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.mag_label.setObjectName("mag_label")
        self.verticalLayout.addWidget(self.mag_label)
        self.name_label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.name_label.setObjectName("name_label")
        self.verticalLayout.addWidget(self.name_label)
        self.comboBox = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.connect_button = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.connect_button.setObjectName("connect_button")
        self.verticalLayout.addWidget(self.connect_button)
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(530, 80, 160, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.slider_left = QtWidgets.QSlider(parent=self.horizontalLayoutWidget)
        self.slider_left.setMaximum(510)
        self.slider_left.setSliderPosition(255)
        self.slider_left.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.slider_left.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBothSides)
        self.slider_left.setTickInterval(10)
        self.slider_left.setObjectName("slider_left")
        self.horizontalLayout.addWidget(self.slider_left)
        self.rov_img = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        self.rov_img.setObjectName("rov_img")
        self.horizontalLayout.addWidget(self.rov_img)
        self.slider_right = QtWidgets.QSlider(parent=self.horizontalLayoutWidget)
        self.slider_right.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.slider_right.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBothSides)
        self.slider_right.setTickInterval(10)
        self.slider_right.setObjectName("slider_right")
        self.horizontalLayout.addWidget(self.slider_right)
        self.tableView = QtWidgets.QTableView(parent=self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(240, 100, 256, 192))
        self.tableView.setObjectName("tableView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.connection_status_label.setText(_translate("MainWindow", "Not Connected"))
        self.age_lebel.setText(_translate("MainWindow", "TextLabel"))
        self.mag_label.setText(_translate("MainWindow", "TextLabel"))
        self.name_label.setText(_translate("MainWindow", "TextLabel"))
        self.connect_button.setText(_translate("MainWindow", "PushButton"))
        self.rov_img.setText(_translate("MainWindow", "TextLabel"))



    def controller_connected_handler(self):
        self.comboBox.addItem("c0")

    def controller_disconnected_handler(self):
        self.comboBox.clear()
        self.comboBox.addItem("k")

    def control_dev_change(self):
        self.rem_conn.mode = self.comboBox.currentText()

    def connect_button_handler(self):
        print("GGGGGGGGGGGGGGGGGGGGG")
        self.conn_mann.connect(("wifi102.local", 1883))


    def connection_state_ui(self):
        self.connection_status_label.setText("Connected");
        self.connect_button.setText("Disconnect")


    def recieved_state_ui(self, type, data):
        if type == 3:
            self.age_lebel.setText(str(int.from_bytes(data, byteorder="little")))
        elif type == 4:
            self.mag_label.setText("Mag: " + (str(int(data[0]))))
        elif type == 5:
            self.name_label.setText(data.decode("utf-8"))

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        if ((self.rem_conn.last_keyboard_key == a0.text())):
            self.rem_conn.last_keyboard_key = ""

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if (self.rem_conn.last_keyboard_key == "") and (a0.text() in keyboard_keys):
            self.rem_conn.last_keyboard_key = a0.text()

    def send_motor_data(self, data):
        if self.conn_mann.connection_state:
            self.conn_mann.send_packet(1, bytearray(data))




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()

