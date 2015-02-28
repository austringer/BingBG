#-*- encoding: utf-8 -*-

import os
import time

def getVersionTuple(v):
  # distutils.version will be changed in future and have no enough doc.
  # So I use another simple implementation
  return tuple(map(int, v.split('.')))


def getUTCDate():
  return time.strftime('%Y-%m-%d', time.gmtime())


def getThisFileDirectory():
  upper_path = os.path.abspath(__file__)
  while True:
    upper_path = os.path.split(upper_path)[0]
    if os.path.isdir(upper_path):
      break
  return upper_path


def getLatestFile(directory):
  entry_list = [directory + os.sep + entry for entry in os.listdir(directory)]

  if not entry_list:
    return ''

  latest_file = max(entry_list, key=os.path.getctime)
  return latest_file