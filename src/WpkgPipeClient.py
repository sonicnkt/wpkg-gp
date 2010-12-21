# 
#
# Install and start WPKG-Server, and connect
# either from the same machine, or from another using the "-s" param.
#
# Currently recognized commands:
# Execute - Start WPKG execution
# Cancel - Cancel an ongoing WPKG execution

from win32pipe import *
from win32file import *
from win32event import *
import pywintypes
import win32api
import winerror
import sys, os, traceback

debug = 0
    
def runClient(server,msg,debug=False):
    try:
        pipeHandle = CreateFile("\\\\%s\\pipe\\WPKG" % server, GENERIC_READ|GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, None)
    except pywintypes.error, (n, f, e):
        print "Error when generating pipe handle: %s" % e
        return 1
    SetNamedPipeHandleState(pipeHandle, PIPE_READMODE_MESSAGE, None, None)
    WriteFile(pipeHandle, msg)
    msg = ""
    while 1:
        try:
            (hr, readmsg) = ReadFile(pipeHandle, 512)
            if debug:
                print (readmsg)
            else: #Strip 3 digit status code
                print (readmsg[4:])
        except win32api.error as exc:
            if exc.winerror == winerror.ERROR_PIPE_BUSY:
                win32api.Sleep(5000)
                continue
            break
            
        sys.stdout.flush()
    
    sys.stdout.flush()
    print "1"
    sys.stdout.flush()
    return 0
    

def main():
    import sys, getopt
    server = "."
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:dl')
        for o,a in opts:
            if o=='-s':
                server = a
            if o=='-d':
                global debug
                debug = 1
        msg = " ".join(args).encode("mbcs")
    except getopt.error as msg:
        print(msg)
        my_name = os.path.split(sys.argv[0])[1]
        print("Usage: %s [-v] [-s server]" % my_name)
        print("       -d = debug")
        return
    
    return runClient(server, msg)

if __name__=='__main__':
    main()
