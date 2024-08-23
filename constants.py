# Importing the Path class from the pathlib module
from pathlib import Path

# Getting the parent directory of the current file and assigning it to the BASE_DIR variable
BASE_DIR = Path(__file__).parent

# Creating a Path object by joining the BASE_DIR path with the 'data' directory
ASSETS = BASE_DIR / 'data'

# Creating a Path object by joining the BASE_DIR path with the 'ready' directory
READY = BASE_DIR / 'ready'