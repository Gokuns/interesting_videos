import os
import sys

# add current path to sys.path
MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
if MODULE_PATH not in sys.path:
    sys.path.append(MODULE_PATH)

# add upper directory to path.
UPPER_DIRECTORY = os.path.abspath(os.path.join(MODULE_PATH, "../"))
if UPPER_DIRECTORY not in sys.path:
    sys.path.append(UPPER_DIRECTORY)