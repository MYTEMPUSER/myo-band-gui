from multiprocessing import Process, Manager
import time;

def f(d):

    d[1] += '1'
    while True:
        d['2'] += 2
        time. sleep (1);



if __name__ == '__main__':
    manager = Manager()

    d = manager.dict()
    d[1] = '1'
    d['2'] = 2


    p1 = Process(target=f, args=(d,))
#    p2 = Process(target=f, args=(d,))
    p1.start()
#    p2.start()
    p1.join()
#    p2.join()

    print (d);
