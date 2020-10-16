from typing import List
import logging
import json
import datetime
import sys
import inspect


NONE = "none"
DEBUG = "debug"
TRACE = "trace"
INFO = "info"
WARNING = "warning"
ERROR = "error"


class _Formatter(logging.Formatter):
    """_Formatter class implements the functionality to format all logger
    output in JSON format.
    """

    def __init__(self, **kwargs):
        super(_Formatter, self).__init__(**kwargs)

    def format(self, record):
        """format proceeds to format logging output as JSON format.
        """
        if not isinstance(record.msg, dict):
            record.msg = {record.levelname.capitalize(): record.msg}
        record.msg["timestamp"] = str(datetime.datetime.fromtimestamp(record.created))
        record.msg["logging"] = record.name
        if "file-name" not in record.msg:
            record.msg["file-name"] = record.filename
        if "lineno" not in record.msg:
            record.msg["lineno"] = record.lineno
        if "func-name" not in record.msg:
            record.msg["func-name"] = record.funcName
        return json.dumps(record.msg)


def loggable(f):
    """loggable is a decorator to be used in all internal log methods.
    """

    def _loggable(self):
        pframe = inspect.stack()[1]
        self.dicta["file-name"] = pframe.filename
        self.dicta["lineno"] = pframe.lineno
        self.dicta["func-name"] = pframe.function
        self.dicta["level"] = DEBUG
        f(self)
        self.dicta = {}

    return _loggable


class _Logging(logging.Logger):
    """_Logging class implements a custom logging that output information in
    JSON format and it allows to define attribute/value pairs on the fly
    using method calls.
    """

    def __init__(self, *args):
        super(_Logging, self).__init__(*args)
        self.dicta = {}

    def _log_runner(self, attr: str):
        """log_runner adds to the logger attribute and arguments passed in any
        called method.
        """

        def _inner_log_runner(*args):
            if len(args) == 0:
                self.dicta[attr] = ""
            elif isinstance(args[0], dict):
                self.dicta[attr] = args
            else:
                self.dicta[attr] = "{}".format(args[0])
            return self

        return _inner_log_runner

    def __getattr__(self, attr):
        try:
            return self.__getattribute__(attr)
        except Exception:
            return self._log_runner(attr)

    def __update_dict(self):
        """___update_dict update the dictionary to be log.
        """
        pframe = inspect.stack()[3]
        self.dicta["file-name"] = pframe.filename
        self.dicta["lineno"] = pframe.lineno
        self.dicta["func-name"] = pframe.function

    # @loggable
    def debug(self):
        self.dicta["level"] = DEBUG
        super(_Logging, self).debug(self.dicta)

    # @loggable
    def trace(self):
        self.dicta["level"] = TRACE
        super(_Logging, self).debug(self.dicta)

    # @loggable
    def info(self):
        self.dicta["level"] = INFO
        super(_Logging, self).info(self.dicta)

    # @loggable
    def warning(self):
        self.dicta["level"] = WARNING
        super(_Logging, self).warning(self.dicta)

    # @loggable
    def error(self):
        self.dicta["level"] = ERROR
        super(_Logging, self).error(self.dicta)

    @loggable
    def call(self, level=INFO):
        """call should be called when implementing attribute/value pairs using
        method calls.
        """
        # pframe = inspect.stack()[1]
        # self.dicta["file-name"] = pframe.filename
        # self.dicta["lineno"] = pframe.lineno
        # self.dicta["func-name"] = pframe.function
        self.dicta["level"] = level
        if level == NONE:
            pass
        elif level == DEBUG:
            # self.debug(self.dicta)
            self.debug()
        elif level == INFO:
            # self.info(self.dicta)
            self.info()
        elif level == WARNING:
            # self.warning(self.dicta)
            self.warning()
        elif level == ERROR:
            # self.error(self.dicta)
            self.error()
        else:
            pass
        # self.dicta = {}


loggars = {}


def get_loggar(name, handler=None):
    """get_loggar retrieves a given custom logger for the given
    module.
    """
    if name not in loggars:
        _loggar = _Logging(name)
        _fmt = _Formatter()
        if not handler:
            handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(_fmt)
        _loggar.addHandler(handler)
        loggars[name] = _loggar
    return loggars[name]


class LoggarProc:
    def __init__(self, filename: str = "loggar.log"):
        self.log_data: List[str] = []
        with open(filename, "r") as fd:
            line = fd.readline()
            while line:
                self.log_data.append(json.loads(line))
                line = fd.readline()

    def tag(self, tagname: str):
        if tagname:
            result: List[str] = []
            for data in self.log_data:
                tagdata = data.get(tagname, None)
                if tagdata:
                    result.append(tagdata)
            return "\n".join(result)
        else:
            return json.dumps(self.log_data, indent=4)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Logger tool")
    parser.add_argument("--noserver", action="store_true", help="Launch Server")
    parser.add_argument(
        "-f",
        "--filename",
        nargs="?",
        default="loggar.log",
        help="Loggar filename (default: loggar.log)",
    )
    parser.add_argument("-t", "--tag", nargs="?", default="", help="Tag name")
    args = parser.parse_args()
    print(LoggarProc(args.filename).tag(args.tag))
