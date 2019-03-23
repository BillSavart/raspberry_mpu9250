import sys
import subprocess
import os

os.chdir("DRAW")
subprocess.call("python draw.py", shell = True)
os.chdir("../GYRO")
subprocess.call("python new_gyro.py", shell = True)
