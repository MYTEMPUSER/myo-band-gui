from PyQt5 import QtCore, QtGui, QtWidgets;

class Ui_MainWindow (object):
  buttonsWidth = 170
  buttonsHeight = 70
  offset = 20
  padding = 35

  def setupUi (self, MainWindow):
    MainWindow.setObjectName("MainWindow");
    MainWindow.resize(self.padding * 2 + 1 * self.offset + 2 * self.buttonsWidth, 350);

    self.centralWidget = QtWidgets.QWidget(MainWindow);
    self.centralWidget.setObjectName("centralWidget");

    self.startRecordingButton = QtWidgets.QPushButton(self. centralWidget);
    self.startRecordingButton.setGeometry(QtCore.QRect (self.padding , self.padding , self.buttonsWidth, self.buttonsHeight));
    self.startRecordingButton.setObjectName("startRecordingButton");

    self.stopRecordingButton = QtWidgets.QPushButton (self. centralWidget);
    self.stopRecordingButton.setGeometry(QtCore.QRect (self.padding , self.padding  + self.buttonsHeight + 5, self.buttonsWidth, self.buttonsHeight));
    self.stopRecordingButton.setObjectName("stopRecordingButton");

    self.statusLabel = QtWidgets.QLabel(self)
    self.statusLabel.setGeometry(QtCore.QRect(self.padding , self.padding  + 2 * (self.buttonsHeight + 5), self.buttonsWidth + 50, self.buttonsHeight))
    self.statusLabel.setObjectName("statusLabel")

    self.handPoseLabel = QtWidgets.QLabel(self)
    self.handPoseLabel.setGeometry(QtCore.QRect(self.padding , self.padding  + 3 * (self.buttonsHeight + 5), self.buttonsWidth + 50, self.buttonsHeight))
    self.handPoseLabel.setObjectName("handPoseLabel")

    self.InfoLabel = QtWidgets.QLabel(self)
    self.InfoLabel.setGeometry(QtCore.QRect(self.padding  + self.buttonsWidth + self.offset, self.padding, self.buttonsWidth, self.buttonsHeight // 2))
    self.InfoLabel.setObjectName("InfoLabel")
    self.InfoLabel.setText("Имя файла")

    self.fileNameLineEdit = QtWidgets.QLineEdit(self)
    self.fileNameLineEdit.setGeometry(QtCore.QRect(self.padding  + self.buttonsWidth + self.offset, self.padding + self.buttonsHeight // 2, self.buttonsWidth, self.buttonsHeight // 2))
    self.fileNameLineEdit.setObjectName("fileNameLineEdit")  

    self.dateCheckBox = QtWidgets.QCheckBox('Добавить дату к файлу', self)
    self.dateCheckBox.setGeometry(QtCore.QRect(self.padding  + self.buttonsWidth + self.offset, self.padding + (self.buttonsHeight + 5), self.buttonsWidth, self.buttonsHeight // 2))
    self.dateCheckBox.setObjectName("dateCheckBox")
    self.dateCheckBox.setChecked(False) 

    self.numberingCheckBox = QtWidgets.QCheckBox('Автоматическая нумерация', self)
    self.numberingCheckBox.setGeometry(QtCore.QRect(self.padding  + self.buttonsWidth + self.offset, self.padding + (self.buttonsHeight + 5) + self.buttonsHeight // 2, self.buttonsWidth + 50, self.buttonsHeight // 2))
    self.numberingCheckBox.setObjectName("dateCheckBox")
    self.numberingCheckBox.setChecked(False) 

    self.showPlotButton = QtWidgets.QPushButton(self. centralWidget);
    self.showPlotButton.setGeometry(QtCore.QRect(self.padding  + self.buttonsWidth + self.offset, self.padding + 2 * (self.buttonsHeight + 5), self.buttonsWidth, self.buttonsHeight))
    self.showPlotButton.setObjectName("showPlotButton");

    self.timer = QtCore.QTimer()

    self.fileNameLineEdit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
    self.statusLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
    self.handPoseLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
    self.InfoLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))  

    MainWindow. setCentralWidget (self. centralWidget);
    self. retranslateUi (MainWindow);
    QtCore. QMetaObject. connectSlotsByName (MainWindow);


  def retranslateUi (self, MainWindow):
    self._translate = QtCore.QCoreApplication.translate;
    MainWindow.setWindowTitle(self._translate("MainWindow", "Myo toolkit"));
    self.startRecordingButton.setText(self._translate ("MainWindow", "Начать запись"));
    self.stopRecordingButton.setText (self._translate ("MainWindow", "Остановить запись"));
    self.showPlotButton.setText (self._translate ("MainWindow", "Графики"));
    self.flagUpdateNameButton = 0;