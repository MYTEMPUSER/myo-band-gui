import enum;
import re;
import struct;
import sys;
import threading;
import time;
import common;


import serial
from serial.tools.list_ports import comports



def multichr (ords):
  return bytes (ords);


def multiord (b):
  return list (b);



class Arm (enum. Enum):

  unknown = 0;
  right = 1;
  left = 2;



class XDirection (enum. Enum):

  unknown = 0;
  xTowardWrist = 1
  xTowardElbow = 2;



class Pose (enum. Enum):

  Rest = 0;
  Fist = 1;
  waveIn = 2;
  waveOut = 3;
  fingersSpread = 4;
  thumbToPinky = 5;
  unknown = 255;



class Packet (object):


  def __init__ (self, ords):

    self. typ = ords [0];
    self. cls = ords [2];
    self. cmd = ords [3];
    self. payload = multichr (ords [4:]);


  def __repr__(self):
    return 'Packet(%02X, %02X, %02X, [%s])' % \
            (self.typ, self.cls, self.cmd,
             ' '.join('%02X' % b for b in multiord(self.payload)))



class BT (object):

  def __init__ (self, tty):
    self. ser = serial. Serial (port=tty, baudrate=9600, dsrdtr=1);
    self. buf = [];
    self. lock = threading. Lock ();
    self. handlers = [];


  def recvPacket (self, timeout = None):
    t0 = time. time ();
    self. ser. timeout = None;

    while timeout is None or time. time () < t0 + timeout:
      if timeout is not None: self.ser.timeout = t0 + timeout - time.time()
      c = self.ser.read()

      if not c: return None

      ret = self. procByte (ord (c));

      if ret:

        if ret.typ == 0x80:
          self. handleEvent (ret);

        return ret;


  def recvPackets (self, timeout = .5):
    res = [];
    t0 = time. time ();

    while time. time () < t0 + timeout:
      p = self. recvPacket (t0 + timeout - time. time ());

      if not p:
        return res;

      res. append (p);
    return res;


  def procByte (self, c):

    if not self. buf:

      if c in [0x00, 0x80, 0x08, 0x88]:
        self. buf. append (c);

      return None;

    elif len (self. buf) == 1:
      self. buf. append (c);
      self. packetLen = 4 + (self. buf [0] & 0x07) + self. buf [1];
      return None;

    else:
      self. buf. append (c);

    if self. packetLen and len (self. buf) == self. packetLen:
      p = Packet (self. buf);
      self. buf = [];
      return p;

    return None;


  def handleEvent (self, p):

    for h in self. handlers:
      h (p);


  def addHandler (self, h):

    self. handlers. append (h);


  def removeHandler (self, h):

    try: self. handlers. remove (h);

    except ValueError: pass;


  def waitEvent (self, cls, cmd):

    res = [None];

    def h (p):
      if p. cls == cls and p. cmd == cmd:
        res [0] = p;

    self. addHandler (h);

    while res [0] is None:
      self. recvPacket ();

    self. removeHandler (h);

    return res [0];


  def connect (self, addr):
    return self. sendCommand (6, 3, common. pack ('6sBHHHH', multichr (addr), 0, 6, 6, 64, 0) );


  def getConnections (self):
    return self. sendCommand (0, 6);


  def discover (self):
    return self. sendCommand (6, 2, b'\x01');


  def endScan (self):
    return self. sendCommand (6, 4);


  def disconnect (self, h):
    return self. sendCommand (3, 0, common. pack ('B', h));


  def readAttr (self, con, attr):

    self. sendCommand (4, 4, common. pack ('BH', con, attr));
    return self. waitEvent (4, 5);


  def writeAttr (self, con, attr, val):

    self. sendCommand (4, 5, common. pack ('BHB', con, attr, len (val)) + val);
    return self. waitEvent (4, 1);


  def sendCommand (self, cls, cmd, payload=b'', waitResp=True):
    s = common. pack ('4B', 0, len (payload), cls, cmd) + payload;
    self. ser. write (s);

    while True:
      p = self. recvPacket ();

      if p.typ == 0:
        return p;

      self. handleEvent (p);



class MyoRaw (object):

  def __init__ (self, tty = None):

    if tty is None:
      tty = self. detectTty ();

    if tty is None:
      raise ValueError ('Error! Dongle for Myo not found!');

    self. bt = BT (tty);
    self. conn = None;
    self. emgHandlers = [];
    self. imuHandlers = [];
    self. armHandlers = [];
    self. poseHandlers = [];


  def detectTty (self):

    for p in comports ():
      if re. search (r'PID=2458:0*1', p[2]):
        print ('using device MyoArmband:', p [0]);
        return p [0];

    return None;


  def run (self, timeout = None):

    self. bt. recvPacket (timeout);


  def connect (self):

    self. bt. endScan ();
    self. bt. disconnect (0);
    self. bt. disconnect (1);
    self. bt. disconnect (2);

    print ('scanning MyoArmband');

    self. bt. discover ();

    while True:
      p = self. bt. recvPacket ();
      print ('scan response MyoArmBand:', p);

      if p. payload. endswith (b'\x06\x42\x48\x12\x4A\x7F\x2C\x48\x47\xB9\xDE\x04\xA9\x01\x00\x06\xD5'):
        addr = list (multiord (p. payload [2:8]));
        break;

    self. bt. endScan ();


    connPkt = self. bt. connect (addr);
    self. conn = multiord (connPkt. payload) [-1];
    self. bt. waitEvent (3, 0);


    fw = self. readAttr (0x17);
    _, _, _, _, v0, v1, v2, v3 = common. unpack ('BHBBHHHH', fw. payload);
    print ('firmware version MyoArmband: %d.%d.%d.%d' % (v0, v1, v2, v3));

    self. old = (v0 == 0);

    if self. old:
      self. writeAttr (0x19, b'\x01\x02\x00\x00');
      self. writeAttr (0x2f, b'\x01\x00');
      self. writeAttr (0x2c, b'\x01\x00');
      self. writeAttr (0x32, b'\x01\x00');
      self. writeAttr (0x35, b'\x01\x00');

      self. writeAttr (0x28, b'\x01\x00');
      self. writeAttr (0x1d, b'\x01\x00');

      C = 1000;
      emgHz = 50;

      emgSmooth = 100;

      imuHz = 50;

      self. writeAttr (0x19, common. pack ('BBBBHBBBBB', 2, 9, 2, 1, C, emgSmooth, C // emgHz, imuHz, 0, 0));

    else:
      name = self. readAttr (0x03);
      print ('device name MyoArmband: %s' % name. payload);

      self. writeAttr (0x1d, b'\x01\x00');
      self. writeAttr (0x24, b'\x02\x00');

            # self.write_attr(0x19, b'\x01\x03\x00\x01\x01')
      self. startRaw ();


    def handleData (p):
      if (p. cls, p. cmd) != (4, 5): return

      c, attr, typ = common. unpack ('BHB', p. payload [:4]);
      pay = p. payload [5:];

      if attr == 0x27:
        vals = common. unpack ('8HB', pay);
        emg = vals [:8];
        moving = vals [8];
        self. onEmg (emg, moving);

      elif attr == 0x1c:
        vals = common. unpack ('10h', pay);
        quat = vals [:4];
        acc = vals [4:7];
        gyro = vals [7:10];
        self. onImu (quat, acc, gyro);

      elif attr == 0x23:
        typ, val, xdir, _,_,_ = common. unpack ('6B', pay);

        if typ == 1:
          self. onArm (Arm (val), XDirection (xdir));

        elif typ == 2:
          self. onArm (Arm. unknown, XDirection. unknown);

        elif typ == 3:
          self. onPose (Pose (val));

      else:
        print ('data with unknown attr: %02X %s' % (attr, p));

    self. bt. addHandler (handleData);


  def writeAttr (self, attr, val):
    if self. conn is not None:
      self. bt. writeAttr (self. conn, attr, val);


  def readAttr (self, attr):
    if self. conn is not None:
      return self. bt. readAttr (self. conn, attr);

    return None;


  def disconnect (self):
    if self. conn is not None:
      self. bt. disconnect (self. conn);


  def startRaw (self):
    self. writeAttr (0x28, b'\x01\x00');
    #self.write_attr(0x19, b'\x01\x03\x01\x01\x00')
    self. writeAttr (0x19, b'\x01\x03\x01\x01\x01');


  def mcStartCollection (self):
    self. writeAttr (0x28, b'\x01\x00');
    elf. writeAttr (0x1d, b'\x01\x00');
    self. writeAttr (0x24, b'\x02\x00');
    self. writeAttr (0x19, b'\x01\x03\x01\x01\x01');
    self. writeAttr (0x28, b'\x01\x00');
    self. writeAttr (0x1d, b'\x01\x00');
    self. writeAttr (0x19, b'\x09\x01\x01\x00\x00');
    self. writeAttr (0x1d, b'\x01\x00');
    self. writeAttr (0x19, b'\x01\x03\x00\x01\x00');
    self. writeAttr (0x28, b'\x01\x00');
    self. writeAttr (0x1d, b'\x01\x00');
    self. writeAttr (0x19, b'\x01\x03\x01\x01\x00');


  def mcEndCollection (self):
    self. writeAttr (0x28, b'\x01\x00');
    self. writeAttr (0x1d, b'\x01\x00');
    self. writeAttr (0x24, b'\x02\x00');
    self. writeAttr (0x19, b'\x01\x03\x01\x01\x01');
    self. writeAttr (0x19, b'\x09\x01\x00\x00\x00');
    self. writeAttr (0x1d, b'\x01\x00');
    self. writeAttr (0x24, b'\x02\x00');
    self. writeAttr (0x19, b'\x01\x03\x00\x01\x01');
    self. writeAttr (0x28, b'\x01\x00');
    self. writeAttr (0x1d, b'\x01\x00');
    self. writeAttr (0x24, b'\x02\x00');
    self. writeAttr (0x19, b'\x01\x03\x01\x01\x01');


  def vibrate (self, length):
    if length in xrange (1, 4):
       self. writeAttr (0x19, common. pack ('3B', 3, 1, length));


  def addEmgHandler (self, h):
    self. emgHandlers. append (h);


  def addImuHandler (self, h):
    self. imuHandlers. append (h);


  def addPoseHandler (self, h):
    self. poseHandlers. append (h);


  def addArmHandler (self, h):
    self. armHandlers. append (h);


  def onEmg (self, emg, moving):
    for h in self. emgHandlers:
      h (emg, moving);


  def onImu (self, quat, acc, gyro):
    for h in self. imuHandlers:
      h (quat, acc, gyro);


  def onPose (self, p):
    for h in self. poseHandlers:
      h (p);


  def onArm (self, arm, xdir):
    for h in self. armHandlers:
      h (arm, xdir);



if __name__ == '__main__':

  def procEmg (emg, moving, times = []):
    print (emg);

  myo = MyoRaw (sys. argv [1] if len (sys. argv) >= 2 else None);
#  myo. addEmgHandler (procEmg);

#  myo. addArmHandler (lambda arm, xdir: print ('arm', arm, 'xdir', xdir));
  myo. addPoseHandler (lambda pose: print ('pose', pose));

  myo. connect()

  while True:
    myo. run (1);
