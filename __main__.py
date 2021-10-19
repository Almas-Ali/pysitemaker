from core.management import exec_from_command_line
import os
from sys import argv
from config import *

__name__ = f['name']
__version__ = f['version']

exec_from_command_line(argv)
