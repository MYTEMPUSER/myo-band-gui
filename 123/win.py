import random;
import string;
import sys;
import threading
from PyQt5.QtGui import *;
from PyQt5.QtCore import *;
from PyQt5.QtWidgets import *;
from PyQt5 import QtCore, QtGui, QtWidgets;

import gui;
import myo;
import time


class MyoWindow (QMainWindow, gui. Ui_MainWindow):
  statusList = ["Запись идёт", "Запись\nпреостановлена", "Подключите USB\nадаптер"]
  curentStatus = 1
  ExitFlag = False
  def __init__ (self):
    super().__init__();
    self.setupUi(self)
    self.startRecordingButton.clicked.connect(self.clickedStartRecording);
    self.stopRecordingButton.clicked.connect(self.clickedStopRecording)
    self.centralWidget.closeEvent = self.closeEvent
    self.statusLabel.setText(self.statusList[self.curentStatus])
    self.statusLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
    self.handPoseLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
    updateHandPoseThread = threading.Thread(target=self.updateCurentHandPose, args=())
    updateHandPoseThread.start()

    self.dongleFlag = True
    self.flagWriteData = True
    myo.poseArm = "unknow";
    try:
      myo = myo.MyoRaw(sys.argv[1] if len(sys. argv) >= 2 else None);
    except:
      self.dongleFlag = False
      return

    myo.addEmgHandler(myo.procEmg);
    myo.addPoseHandler(myo.position);

  def updateStatus (self, newStatus):
    self.curentStatus = newStatus
    self.statusLabel.setText(self.statusList[self.curentStatus])

  def generate_pins (self, size=6, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size));

  def startWriting:
    try:
      myo.connect()
      while self.flagWriteData:
        myo.run(1)
    except KeyboardInterrupt:
      if self.flagSave:
        writeTable.saveTable()
        print("STOPED")
      return
    if myo.flagSave and not self.flagWriteData:
      writeTable.saveTable()
      print("Recording stopped correctly")


  def clickedStartRecording (self):
    self.clickedStopRecording()
    self.updateStatus(0)
    myoThread = threading.Thread(target=myo.initialize, args=())
    myoThread.start()
    time.sleep(0.1)
    if (not self.dongleFlag):
      self.updateStatus(2)

  def clickedStopRecording (self):
    self.updateStatus(1)
    myo.stopWrite()
    time.sleep(1)

  def closeEvent(self, event):
    self.clickedStopRecording()
    self.ExitFlag = True
    time.sleep(1)

  def updateCurentHandPose(self):
    while not self.ExitFlag:
      time.sleep(1)
      self.handPoseLabel.setText(myo.poseArm)
    

if __name__ == '__main__':
  app = QApplication(sys. argv);
  form = MyoWindow();
  form.show();
  try:
    app.exec();
  except KeyboardInterrupt:
    print ("1");

  


def stopWrite ():
  global flagWriteData
  flagWriteData = False
