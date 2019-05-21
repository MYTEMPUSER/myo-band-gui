from PyQt5 import QtCore, QtGui, QtWidgets;

class Ui_MainWindow (object):
  buttonsWidth = 150
  buttonsHeight = 70

  def setupUi (self, MainWindow):
    MainWindow.setObjectName("MainWindow");
    MainWindow.resize(210, 350);

    self.centralWidget = QtWidgets.QWidget(MainWindow);
    self.centralWidget.setObjectName("centralWidget");

    self.startRecordingButton = QtWidgets.QPushButton(self. centralWidget);
    self.startRecordingButton.setGeometry(QtCore.QRect (30, 30, self.buttonsWidth, self.buttonsHeight));
    self.startRecordingButton.setObjectName("startRecordingButton");

    self.stopRecordingButton = QtWidgets.QPushButton (self. centralWidget);
    self.stopRecordingButton.setGeometry(QtCore.QRect (30, 30 + self.buttonsHeight + 5, self.buttonsWidth, self.buttonsHeight));
    self.stopRecordingButton.setObjectName("stopRecordingButton");

    self.statusLabel = QtWidgets.QLabel(self)
    self.statusLabel.setGeometry(QtCore.QRect(35, 30 + 2 * (self.buttonsHeight + 5), self.buttonsWidth + 50, self.buttonsHeight))
    self.statusLabel.setObjectName("statusLabel")

    self.handPoseLabel = QtWidgets.QLabel(self)
    self.handPoseLabel.setGeometry(QtCore.QRect(35, 30 + 3 * (self.buttonsHeight + 5), self.buttonsWidth + 50, self.buttonsHeight))
    self.handPoseLabel.setObjectName("handPoseLabel")


    MainWindow. setCentralWidget (self. centralWidget);
    self. retranslateUi (MainWindow);
    QtCore. QMetaObject. connectSlotsByName (MainWindow);


  def retranslateUi (self, MainWindow):
    self._translate = QtCore.QCoreApplication.translate;
    MainWindow.setWindowTitle(self._translate("MainWindow", "Myo toolkit"));
    self.startRecordingButton.setText(self._translate ("MainWindow", "Начать запись"));
    self.stopRecordingButton.setText (self._translate ("MainWindow", "Остановить запись"));
    self.flagUpdateNameButton = 0;