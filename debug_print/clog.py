FORE_RED = 31
FORE_GREEN = 32
FORE_YELLOW = 33
FORE_WHITE = 37

def colorPrint(msg, color):
    fore = 37
    if (color == "red"):
        fore = FORE_RED
    elif (color == "green"):
        fore = FORE_GREEN
    elif (color == "yellow"):
        fore = FORE_YELLOW
    elif (color == "white"):
        fore = FORE_WHITE
    else:
        print "Don't supprrot %s, use white as default" % color                
    type = "\x1B[%d;%dm" % (0, fore)
    orig = "\x1B[0m"
    print "%s%s%s" % (type, msg, orig)


class clog:
    CLOG_LEVEL_VERSE = 1
    CLOG_LEVEL_DEBUG = 1 << 1
    CLOG_LEVEL_WARNING = 1 << 2
    CLOG_LEVEL_ERROR = 1 << 3
    CLOG_LEVEL_CRITICAL = 1 << 4
    CLOG_LEVEL = 1
    @staticmethod
    def v(str):
        if clog.CLOG_LEVEL & clog.CLOG_LEVEL_VERSE != 0:
            colorPrint(str, "white")
    @staticmethod
    def d(str):
        if clog.CLOG_LEVEL & clog.CLOG_LEVEL_DEBUG != 0:
            colorPrint(str, "green")
    @staticmethod
    def w(str):
        if clog.CLOG_LEVEL & clog.CLOG_LEVEL_WARNING != 0:
            colorPrint(str, "yellow")
    @staticmethod
    def e(str):
        if clog.CLOG_LEVEL & clog.CLOG_LEVEL_ERROR != 0:
           colorPrint(str, "red")
    @staticmethod
    def c(str):
        if clog.CLOG_LEVEL & clog.CLOG_LEVEL_CRITICAL != 0:
            colorPrint(str, "red")
    @staticmethod
    def setLevel(str):
        args = str.strip().split("|")
        for arg in args:
            if arg == "v":
                clog.CLOG_LEVEL |= clog.CLOG_LEVEL_VERSE
            elif arg == "d":
                clog.CLOG_LEVEL |= clog.CLOG_LEVEL_DEBUG
            elif arg == "w":
                clog.CLOG_LEVEL |= clog.CLOG_LEVEL_WARNING
            elif arg == "e":
                clog.CLOG_LEVEL |= clog.CLOG_LEVEL_ERROR
            elif arg == "c":
                clog.CLOG_LEVEL |= clog.CLOG_LEVEL_CRITICAL
            else:
                print arg + "is not supported"
                
        
   
    
                