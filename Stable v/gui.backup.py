from PyQt5 import QtCore, QtGui, QtWidgets;




class Ui_MainWindow (object):


  def setupUi (self, MainWindow):

    MainWindow. setObjectName ("MainWindow");
    MainWindow. resize (469, 292);


    self. centralWidget = QtWidgets. QWidget (MainWindow);
    self. centralWidget. setObjectName ("centralWidget");
    self. pushButton = QtWidgets. QPushButton (self. centralWidget);
    self. pushButton. setGeometry (QtCore. QRect (30, 90, 111, 51));
    self. pushButton. setObjectName ("pushButton");
    self. textEdit = QtWidgets. QTextEdit (self. centralWidget);
    self. textEdit. setGeometry (QtCore. QRect (200, 40, 221, 181));
    self. textEdit. setObjectName ("textEdit");


    MainWindow. setCentralWidget (self. centralWidget);


    self. menuBar = QtWidgets. QMenuBar (MainWindow);
    self. menuBar. setGeometry (QtCore. QRect (0, 0, 469, 21));
    self. menuBar. setObjectName ("menuBar");


    MainWindow. setMenuBar (self. menuBar);


    self. mainToolBar = QtWidgets. QToolBar (MainWindow);
    self. mainToolBar. setObjectName ("mainToolBar");


    MainWindow. addToolBar (QtCore. Qt. TopToolBarArea, self. mainToolBar);


    self. statusBar = QtWidgets. QStatusBar (MainWindow);
    self. statusBar. setObjectName ("statusBar");


    MainWindow. setStatusBar (self. statusBar);


    self. retranslateUi (MainWindow);


    QtCore. QMetaObject. connectSlotsByName (MainWindow);



  def retranslateUi (self, MainWindow):

    self. _translate = QtCore. QCoreApplication. translate;


    MainWindow. setWindowTitle (self. _translate ("MainWindow", "Myo toolkit"));


    self. pushButton. setText (self. _translate ("MainWindow", "начать запись"));


    self. flagUpdateNameButton = 0;



  def updateNameButton (self):

    if self. flagUpdateNameButton == 1:

      self. pushButton. setText (self. _translate ("MainWindow", "начать запись"));
      self. flagUpdateNameButton = 0;


      return True


    self. pushButton. setText (self. _translate ("MainWindow", "Остановить запись"));
    self. flagUpdateNameButton = 1;


    return False;
