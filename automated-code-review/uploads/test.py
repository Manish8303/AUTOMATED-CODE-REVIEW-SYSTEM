# test_ok.py - valid Python but full of bad practices

import os

def calc(x, y):
  z = x + y
  print("Result:", z)
  if z > 10:
    os.system("echo Big number!")  # security issue
  else:
    print("Small number")
  a = 5  # unused variable

calc(5, 6)
