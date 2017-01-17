#!/usr/bin/env python

import time
import can
import threading

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()
lock = threading.Lock()


bustype = 'socketcan_native'
channel = 'can0'

## activa
# adpmprototypeadcanfr01.adphmiactvndendwithreas      in 0x43 at bit 31 for 4 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr01.adphmiactvndendwithreas_ub   in 0x43 at bit 16 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 1];
# adpmprototypeadcanfr01.adphmihandoverreq            in 0x43 at bit 27 for 4 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr01.adphmihandoverreq_ub         in 0x43 at bit 17 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 1];
# adpmprototypeadcanfr01.adphmilaneoffs               in 0x43 at bit 6 for 3 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr01.adphmilaneoffs_ub            in 0x43 at bit 7 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 1];
# adpmprototypeadcanfr01.adphmilanepptygroup_ub       in 0x43 at bit 49 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 1];
# adpmprototypeadcanfr01.adphmilanepptygrouplaneid    in 0x43 at bit 63 for 4 bit is unsigned big endian multiply by 1 add 0 with range [0, 15];
# adpmprototypeadcanfr01.adphmilanepptygrouplanetyp   in 0x43 at bit 59 for 4 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr01.adphmilanepptygrouptrfcdir   in 0x43 at bit 48 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr01.adplireq_ub                  in 0x43 at bit 50 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 1];
# adpmprototypeadcanfr01.adplireqchgdrvgsidereq       in 0x43 at bit 47 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr01.adplireqchks                 in 0x43 at bit 39 for 8 bit is unsigned big endian multiply by 1 add 0 with range [0, 255];
# adpmprototypeadcanfr01.adplireqcntr                 in 0x43 at bit 43 for 4 bit is unsigned big endian multiply by 1 add 0 with range [0, 15];
# adpmprototypeadcanfr01.adplireqfoglifrntreq         in 0x43 at bit 46 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr01.adplireqfoglirereq           in 0x43 at bit 45 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr01.adplireqhzrdliactvnreq       in 0x43 at bit 44 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr01.adplireqhzrdlideactnreq      in 0x43 at bit 53 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr01.adplireqincrlirireq          in 0x43 at bit 52 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr01.adplireqindcrlereq           in 0x43 at bit 51 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr01.adplireqlistreq              in 0x43 at bit 55 for 2 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr01.adpmodsafegroup_ub           in 0x43 at bit 18 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 1];
# adpmprototypeadcanfr01.adpmodsafegroupavl           in 0x43 at bit 20 for 2 bit is unsigned big endian multiply by 1 add 0 with range [0, 2];
# adpmprototypeadcanfr01.adpmodsafegroupchks          in 0x43 at bit 15 for 8 bit is unsigned big endian multiply by 1 add 0 with range [0, 255];
# adpmprototypeadcanfr01.adpmodsafegroupcntr          in 0x43 at bit 3 for 4 bit is unsigned big endian multiply by 1 add 0 with range [0, 15];
# adpmprototypeadcanfr01.adpmodsafegroupmod           in 0x43 at bit 23 for 3 bit is unsigned big endian multiply by 1 add 0 with range [0, 1];


## steering
# adpmprototypeadcanfr08.adpasylatctrlmodreqgroup_ub      in 0x32 at bit 40 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 1];
# adpmprototypeadcanfr08.adpasylatctrlmodreqgroupasylatct in 0x32 at bit 55 for 4 bit is unsigned big endian multiply by 1 add 0 with range [0, 1];
# adpmprototypeadcanfr08.adpasylatctrlmodreqgroupasylatre in 0x32 at bit 63 for 8 bit is unsigned big endian multiply by 1 add 0 with range [0, 255];
# adpmprototypeadcanfr08.adpasylatctrlmodreqgroupasy_0000 in 0x32 at bit 51 for 4 bit is unsigned big endian multiply by 1 add 0 with range [0, 15];
# adpmprototypeadcanfr08.adpasypinionagreq                in 0x32 at bit 6 for 15 bit is signed big endian multiply by 0.0009765625 add 0 with range [-14.5, 14.5];
# adpmprototypeadcanfr08.adpasypinionagreq_ub             in 0x32 at bit 7 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 1];
# adpmprototypeadcanfr08.adpcllsnfwdwarnreq               in 0x32 at bit 22 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr08.adpcllsnfwdwarnreq_ub            in 0x32 at bit 23 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 1];
# adpmprototypeadcanfr08.adpcllsnthreat                   in 0x32 at bit 42 for 2 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr08.adpcllsnthreat_ub                in 0x32 at bit 43 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 1];
# adpmprototypeadcanfr08.adpsftydecelgroupsafe_ub         in 0x32 at bit 21 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 1];
# adpmprototypeadcanfr08.adpsftydecelgroupsafeasysftydece in 0x32 at bit 39 for 8 bit is unsigned big endian multiply by 0.1 add 0 with range [0, 15];
# adpmprototypeadcanfr08.adpsftydecelgroupsafeasysftyenad in 0x32 at bit 20 for 1 bit is unsigned big endian multiply by 1 add 0 with range [0, 0];
# adpmprototypeadcanfr08.adpsftydecelgroupsafesftydecelgr in 0x32 at bit 31 for 8 bit is unsigned big endian multiply by 1 add 0 with range [0, 255];
# adpmprototypeadcanfr08.adpsftydecelgroupsafesftyde_0000 in 0x32 at bit 19 for 4 bit is unsigned big endian multiply by 1 add 0 with range [0, 15];


bitpos = 0
finished = False

def Input_Thread():
    global bitpos, lock, finished
    try:
        while not finished:
            input = getch()
            print(">" + input)
            # print("Deine Eingabe-> %s" % ord(input))
            if input == "q" or ord(input) == 3:
                print("quit")
                finished = True

            if input == 'w':
                bitpos+=1
                if bitpos > 7:
                    bitpos = 0
                print("Bitpos: " + str(bitpos))
    except (KeyboardInterrupt, SystemExit):
        finished = True


thread2 = threading.Thread(target=Input_Thread)
thread2.start()



def producer():
    bus = can.interface.Bus(channel, bustype=bustype)
    i=0
    data=[0x80,0x40,0x20,0x10,0x08,0x04,0x02,0x00]

    while True:
        msg = can.Message(arbitration_id=0x43, data=[i, 0, 0x34, 0, 0, 0, 0, 0], extended_id=False)
        #print(i)
        #print(msg)
        bus.send(msg)
        msg = can.Message(arbitration_id=0x32, data=[0x80, data[bitpos], 0, 0, 0, 0x01, 0x10, 0], extended_id=False)
        bus.send(msg)
        time.sleep(0.02)
        i+=1
        if i>14:
            i=0

producer()