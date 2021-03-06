import os;
import shutil;
import datetime as dt;

import xlsxwriter as xl;

alf = ("D", "E", "F", "G", "H", "I", "J", "K");
nameWorkDir = "./datasets/";
nameDataFile = "./data.xlsx";

if os. path. exists (nameWorkDir) != True:
  os. mkdir (nameWorkDir, 0o777);

def createWorkBook ():
  dis = {
    "A1": "date time",
    "B1": "time seconds",
    "C1": "pose arm",
    "D1": "EMG1",
    "E1": "EMG2",
    "F1": "EMG3",
    "G1": "EMG4",
    "H1": "EMG5",
    "I1": "EMG6",
    "J1": "EMG7",
    "K1": "EMG8"
  }
  global count
  count = 2;
  workBook = xl.Workbook(nameWorkDir + nameDataFile);
  workSheet = workBook.add_worksheet();
  for i in dis:
    workSheet. write (i, dis [i]);
  return workBook, workSheet

workBook, workSheet = createWorkBook()

def addEmg (timeDate, timeSeconds, poseArm, emg):
  global count;
  workSheet. write ("A" + str (count), str (timeDate));
  workSheet. write (("B" + str (count)), str (timeSeconds));
  workSheet. write (("C" + str (count)), poseArm);
  for i in range (0, 8):
    workSheet. write ((alf [i] + str (count)), str (emg [i]));
  count += 1;

def saveTable(need_date = True, need_numbering = False, file_name = ""):
  global workBook
  global workSheet
  if os. path. exists (nameWorkDir) != True:
    os. mkdir (nameWorkDir, 0o777);

  newNameDataFile = ""
  if (need_date or file_name == ""):
    newNameDataFile = str (dt.datetime.now()) + ' ';
  newNameDataFile += file_name
  workBook.close();
  if need_numbering:
    file_number = "000"
    ind = 1
    while os.path.exists(nameWorkDir + newNameDataFile + ' ' + (file_number + str(ind))[-3:] + ".xlsx"):
      ind += 1
    newNameDataFile += ' ' + (file_number + str(ind))[-3:]
    
  newNameDataFile = newNameDataFile  +  ".xlsx"
  print(newNameDataFile)

  shutil.move(nameWorkDir + nameDataFile, nameWorkDir + newNameDataFile);
  workBook, workSheet = createWorkBook()
  return newNameDataFile