from logging import FileHandler
from tools.loggar import get_loggar

Log = get_loggar("pyengine", handler=FileHandler("loggar.log", mode="w"))
