from modulefinder import Module
from logzero import logger, logfile, setup_logger
import logging

try:
    from colorama import init, Fore, Back, Style
except ModuleNotFoundError:
    pass

from io import StringIO


class Logger:

    def __init__(self , logfile , name = "logger" , maxMB = 1 , backupCount = 0 , level=logging.DEBUG , usePrint = True):

        
        """
        logfile = path to log file
        name = name of the logger object
        maxMB = max size of log file in mega bytes
        backupCount = how many backups of log files to keep
        level = logging level
        usePrint = whether to print log to console or not
        """
        init(convert=True)

        # setup logger
        self.logger_obj = setup_logger(
            logfile=logfile,
            disableStderrLogger = True,
            name=name,
            json=True,
            maxBytes=maxMB * 1000 * 1000,
            backupCount=backupCount,
            level=level
            )

        # color dict for different levels
        self.colorDict = {
        "info" : Fore.CYAN,
        "debug" : Fore.GREEN,
        "warning" : Fore.YELLOW,
        "error" : Fore.MAGENTA,
        "exception" : Fore.RED,
        "critical" : Fore.RED,
        }

        self.usePrint = usePrint

        if(usePrint):
            # add stringIO stream handler
            self.streamIO = StringIO()
            self.stream_handler = logging.StreamHandler(self.streamIO)
            self.stream_handler_formatter = logging.Formatter('%(levelname)s: %(message)s , line = %(lineno)s , func = %(funcName)s() , %(filename)s , %(asctime)s')
            self.stream_handler.setFormatter(self.stream_handler_formatter)
            self.logger_obj.addHandler(self.stream_handler)
        



    # print info to consol
    def print_log(self):

        if(self.usePrint):
            # get log from stream handler
            self.streamIO.flush()
            value = self.streamIO.getvalue()

            # determine log level
            valueList = value.split(":")
            level = valueList[0].lower()

            # if error , check for traceback and check if error is exception
            if(level == "error"):
                if(value.find("Traceback") != -1):
                    level = "exception"

            # reset stream io
            self.streamIO.seek(0)
            self.streamIO.truncate(0)

            # set color according to level
            color =  self.colorDict.get(level , Fore.WHITE)
            reset = Fore.RESET

            # print line if the level 
            if((level == "exception") or (level == "critical")):
                print(color + f'{value}' + reset , end="\n")

            else:
                print(color + f'{value}' + reset , end="")









        




def __test():
    def raiseException():
        raise RuntimeError

    obj = Logger("testLogs.log")

    # change log level
    obj.logger_obj.setLevel(logging.DEBUG)

    obj.logger_obj.debug("this is debug")
    obj.print_log()
    obj.logger_obj.info("this is info")
    obj.print_log()
    obj.logger_obj.warning("this is warning")
    obj.print_log()
    obj.logger_obj.error("this is error")
    obj.print_log()

    try:
        raiseException()
    except RuntimeError:
        obj.logger_obj.exception("this is exception")
        obj.print_log()


    try:
        raiseException()
    except RuntimeError:
        obj.logger_obj.fatal("this is fatal error" , exc_info=True)
        obj.print_log()









def __test2():

    obj = Logger("testLogs.log")

    obj.logger_obj.setLevel(logging.WARNING)

    obj.logger_obj.debug("this is debug")
    obj.print_log()
    obj.logger_obj.info("this is info")
    obj.print_log()
    obj.logger_obj.warning("this is warning")
    obj.print_log()
    obj.logger_obj.error("this is error")
    obj.print_log()

    try:
        def raiseException():
            raise RuntimeError

        raiseException()
    except RuntimeError:
        obj.logger_obj.exception("this is exception")
        obj.print_log()


    try:
        def raiseException():
            raise RuntimeError

        raiseException()
    except RuntimeError:
        obj.logger_obj.fatal("this is fatal error" , exc_info=True)
        obj.print_log()


if __name__ == "__main__":
    __test()
    __test2()