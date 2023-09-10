import logging

_log = logging.getLogger(__name__)

info_formatter = logging.Formatter('\033[38;2;0;100;128mINFO    \033[0m\033[38;2;120;0;80m%(name)s\033[0m : %(message)s')
warn_formatter = logging.Formatter('\033[38;2;0;100;128mWARNING \033[0m\033[38;2;120;0;80m%(name)s\033[0m : %(message)s')

info_handler = logging.StreamHandler()
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(info_formatter)

warn_handler = logging.StreamHandler()
warn_handler.setLevel(logging.WARNING)
warn_handler.setFormatter(warn_formatter)

_log.addHandler(info_handler)
_log.addHandler(warn_handler)

__version__ = '1.0'

from .gateway import *
from .session import *
from .console import *
from .client  import *
from .events  import *