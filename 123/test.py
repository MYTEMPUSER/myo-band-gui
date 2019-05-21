import threading

def app (x, eventForApp, eventForSet):

  for i in range(1):

    eventForApp. wait ();
    eventForApp. clear ();

    if x == 0:

      print ("hello");


    if x == 1:

      print ("fuck");


    eventForSet. set ();



e1 = threading. Event ();
e2 = threading. Event ();


t1 = threading. Thread (target=app, args=(0, e1, e2));
t2 = threading. Thread (target=app, args=(1, e2, e1));


t1. start ();
t2. start ();


e1. set ();


t1. join ();
t2. join ();

