#-*- encoding: utf-8 -*-

import os
import platform
import subprocess

from utils import *

def getGnomeVersion():
  p = subprocess.Popen(['gnome-session', '--version'], stdout=subprocess.PIPE)
  out = p.stdout.readline()
  if type(out) is not str:
      out = out.decode('utf-8')
  version = getVersionTuple(out.split(' ')[1])
  if version > getVersionTuple('3'):
    return 3
  elif version > getVersionTuple('2'):
    return 2
  return -1


def setWallpaperOnGnome3(image_path):
  print('Set image file %s as gnome 3 background.' % image_path)

  image_path_uri = 'file://' + image_path
  subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', image_path_uri])


def setWallpaperOnWindows(image_path):
  import ctypes

  print('Set image file %s as Windows background.' % image_path)

  SPI_SETDESKWALLPAPER = 0x0014
  ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image_path.encode('ISO-8859-1'), 0)
  # occurs some strange problems
  # ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path.encode('UTF-16LE'), 0)

def setWallpaper(image_path):
  image_path = os.path.abspath(image_path)
  system = platform.system()
  if system == 'Windows':
    setWallpaperOnWindows(image_path)
  elif system == 'Darwin':
    pass
  elif system == 'Linux':
    desktop_session = os.environ.get('DESKTOP_SESSION')
    if desktop_session == 'unity' or (desktop_session == 'gnome' and getGnomeVersion() == 3):
      setWallpaperOnGnome3(image_path)