from multiprocessing import Process
import time

import myo



l = [1, 2];

def app (x, delay):

  try:

    myo. initialize (l);
    print ("master {}". format (l));
    l. append (4);
    myo. start (l);
    print ("master {}". format (l));
    time.sleep(delay)


  except KeyboardInterrupt:

    print ("Yes");



l. append (6);
if __name__ == '__main__':

  l. append (7);
  process1 = Process (target=app, args=("a", 0.5));
  l. append (9);

  process1. start ();
#  process1. join (l);
  l. append (10);


#  while True:
#    l. append (8);
#    time. sleep (5);

  print('Done.')

