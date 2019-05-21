import random;
import string;
import sys;
import threading
from PyQt5.QtGui import *;
from PyQt5.QtCore import *;
from PyQt5.QtWidgets import *;
from PyQt5 import QtCore, QtGui, QtWidgets;
import writeTable

import gui;
import myo;
import time


class MyoWindow (QMainWindow, gui.Ui_MainWindow):
  statusList = ["Запись идёт", "Запись\nпреостановлена", "Подключите USB\nадаптер"]
  curentStatus = 1

  def __init__ (self):
    super().__init__();
    self.setupUi(self)
    self.startRecordingButton.clicked.connect(self.clickedStartRecording);
    self.stopRecordingButton.clicked.connect(self.clickedStopRecording)
    self.centralWidget.closeEvent = self.closeEvent
    self.statusLabel.setText(self.statusList[self.curentStatus])

    self.dongleFlag = True
    self.flagWriteData = True
    myo.poseArm = "unknow";
    

  def generate_pins (self, size=6, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size));

  def startWriting(self):
    try:
      Myo = myo.MyoRaw(sys.argv[1] if len(sys. argv) >= 2 else None);
    except:
      self.dongleFlag = False
      return
    Myo.addEmgHandler(myo.procEmg)
    Myo.addPoseHandler(myo.position)

    try:
      Myo.connect()
      while self.flagWriteData:
        Myo.run(1)
        self.handPoseLabel.setText("Положение руки:\n" + myo.poseArm)
    except KeyboardInterrupt:
      if self.flagSave:
        writeTable.saveTable()
        print("STOPED")
      return
    if myo.flagSave and not self.flagWriteData:
      writeTable.saveTable(self.dateCheckBox.isChecked(), self.numberingCheckBox.isChecked(), self.fileNameLineEdit.text())
      Myo.disconnect()
      print("Recording stopped correctly")


  def clickedStartRecording (self):
    self.clickedStopRecording()
    self.startRecordingButton.setEnabled(False)
    self.updateStatus(0)
    self.flagWriteData = True
    myoThread = threading.Thread(target=self.startWriting, args=())
    myoThread.start()
    if (not self.dongleFlag):
      self.updateStatus(2)

  def clickedStopRecording (self):
    self.startRecordingButton.setEnabled(True)
    self.updateStatus(1)
    self.flagWriteData = False
    time.sleep(0.1)

  def closeEvent(self, event):
    self.clickedStopRecording()

  def updateStatus (self, newStatus):
    self.curentStatus = newStatus
    self.statusLabel.setText(self.statusList[self.curentStatus])
    

if __name__ == '__main__':
  app = QApplication(sys. argv);
  form = MyoWindow();
  form.show();
  try:
    app.exec();
  except KeyboardInterrupt:
    print ("1");

