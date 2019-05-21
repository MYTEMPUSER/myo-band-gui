import random;
import string;
import threading;
import time;
import sys;
from multiprocessing import Process;
from PyQt5.QtGui import *;
from PyQt5.QtCore import *;
from PyQt5.QtWidgets import *;

import gui;
import myo;





l = [1, 2];
def appM (x, delay):


  try:

    myo. initialize (l);
    myo. start (l);


  except KeyboardInterrupt:

    print ("Process myo killed");






class MyoWindow (QMainWindow, gui. Ui_MainWindow):

  def __init__ (self):

    super (). __init__ ();


    self. setupUi (self)
    self. pushButton. clicked. connect (self. buttonClicked);
    self. pushButton2. clicked. connect (self. buttonClicked2);


  def buttonClicked2 (self):

    print ("trrt");


    processMyo = Process (target=appM, args=("a", 0.5));

    processMyo. start ();




  def buttonClicked (self):

    self. textEdit. append ("fuck");
    self. updateNameButton ();
    l. append (6);




if __name__ == '__main__':

  app = QApplication (sys. argv);


  form = MyoWindow ();
  form. show ();


  try:

    app. exec ();

  except KeyboardInterrupt:

    print ("1");
