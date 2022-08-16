from os import device_encoding
import sys
from PyQt6.QtWidgets import (
    QApplication, 
    QComboBox, 
    QWidget, 
    QLabel, 
    QLineEdit, 
    QPlainTextEdit,
    QPushButton, 
    QTextEdit, 
    QVBoxLayout,
)

from PyQt6.QtCore import QObject, pyqtSignal
# from PyQt6.QtGui import QIcon
# from PyQt6.QtBluetooth import QBluetooth

import asyncio
from bleak import BleakScanner

import qasync

names = ['jackson', 'james', 'lisa', 'mia']

# create application
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello App")
        # size of app
        self.resize(500, 500)

        # layout class
        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- widgets ---
        buttonScan = QPushButton('Scan for Devices', clicked=self.startScan)
        # title        
        self.titleDevices = QLabel("List of devices")
        self.deviceList = QComboBox()
        self.deviceList.addItems(names)
        self.deviceList.activated.connect(self.indexShow)
        # button
        buttonConnect = QPushButton('Connect', clicked=self.connectBLE)
        self.inputField = QLineEdit()
        # button = QPushButton('&Say Hello', clicked=self.sayHello)
        self.title_Console = QLabel("Console")
        self.console = QPlainTextEdit()

        # add widgets to the layout 
        layout.addWidget(buttonScan)
        layout.addWidget(self.titleDevices)
        layout.addWidget(self.deviceList)
        layout.addWidget(buttonConnect)
        layout.addWidget(self.inputField)
        # layout.addWidget(button)
        layout.addWidget(self.title_Console)
        layout.addWidget(self.console)

    # def consolePrint(self, text):
    #     inputText = self.inputField.text()
    #     self.output.setText('Hello {0}'.format(inputText))

    def connectBLE(self):
        print(f'selected item is ')
    
    def indexShow(self, index):
        print("activated index: ", index)

    # scan for bluetooth devices
    @qasync.asyncSlot()
    async def startScan(self):
        print("scan started")
        self.console.appendPlainText("scan started")
        deviceList = await BleakScanner.discover()
        for d in deviceList:
            print(d)
            self.console.appendPlainText(d)
        self.console.appendPlainText("Scan Finished")
        if len(deviceList) == 0:
            print("No devices found")
            self.console.appendPlainText("No devices found")
    
class BluetoothDevice(QObject):
    def __post__init__(self):
        super().__init__()
    
    @qasync.asyncSlot()
    async def handle_scan(self):
        self.log_edit.appendPlainText("Started scanner")
        self.devices.clear()
        self.console.appendPlainText('Scan Started')
        devices = await BleakScanner.discover()
        print(devices)
        self.devices.extend(devices)
        self.devices_combobox.clear()
        for i, device in enumerate(self.devices):
            self.devices_combobox.insertItem(i, device.name, device)
        self.log_edit.appendPlainText("Finish scanner")

def main():
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    # style sheet
    app.setStyleSheet( '''
        QWidget {
            font-size: 25px;
        }
        QPushButton {
            font-size: 20px;
        }
    ''')


    # windows app from app class
    window = MyApp()
    # display
    window.show()
    with loop:
        loop.run_forever()

    app.exec()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()