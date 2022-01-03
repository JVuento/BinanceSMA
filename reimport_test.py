import tsl_settings
import time
import importlib
import sys


for i in range(1,20):
  importlib.reload(sys.modules['tsl_settings'])
  from tsl_settings import *
  print(COINS)
  time.sleep(10)
  
