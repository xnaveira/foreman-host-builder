"""
imports.py: Module with imports for foreman-host-builder.py and its modules
"""

import sys
import subprocess
import json
import urllib
import getopt
import re

from fabric.colors import red,green,yellow,white,cyan
from config import *
from foreman.client import Foreman, ForemanException
